"""Produce un Short vertical (1080x1920) a partir de contenido/<slug>/guion.yaml.

Uso:  python pipeline/producir.py contenido/<slug>
Salida: contenido/<slug>/salida/short.mp4 (+ subtitulos.srt)

Todo lo visual se genera acá (tipografía y formas propias): no usa fotos,
clips ni música de terceros, para no tener reclamos de derechos.
"""
import os, re, subprocess, sys, tempfile
import numpy as np
import soundfile as sf
import yaml
from PIL import Image, ImageDraw, ImageFont

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUENTES = os.path.join(RAIZ, "assets", "fuentes")
MODELOS = os.environ.get("KOKORO_DIR", os.path.join(RAIZ, "modelos"))
W, H, FPS = 1080, 1920, 30
VERDE, VERDE2, BLANCO, AMARILLO, TINTA = (11, 93, 59), (17, 128, 79), (255, 255, 255), (255, 211, 77), (17, 17, 17)


def fuente(peso, tam):
    return ImageFont.truetype(os.path.join(FUENTES, f"Inter-{peso}.otf"), tam)


def voz(texto, voz_id, velocidad):
    from kokoro_onnx import Kokoro
    if not hasattr(voz, "k"):
        voz.k = Kokoro(os.path.join(MODELOS, "kokoro-v1.0.onnx"), os.path.join(MODELOS, "voices-v1.0.bin"))
    audio, sr = voz.k.create(texto, voice=voz_id, speed=velocidad, lang="es")
    return audio, sr


def envolver(draw, texto, f, ancho):
    lineas, actual = [], ""
    for palabra in texto.split():
        prueba = (actual + " " + palabra).strip()
        if draw.textlength(prueba, font=f) <= ancho:
            actual = prueba
        else:
            lineas.append(actual)
            actual = palabra
    lineas.append(actual)
    return lineas


def placa(escena, idx, total, logo):
    """Dibuja la placa de una escena: cifra o palabra clave grande + bajada."""
    img = Image.new("RGB", (W, H), VERDE)
    d = ImageDraw.Draw(img)
    # líneas de cancha de fondo
    d.ellipse([W / 2 - 330, H / 2 - 330, W / 2 + 330, H / 2 + 330], outline=VERDE2, width=10)
    d.line([0, H / 2, W, H / 2], fill=VERDE2, width=10)
    d.rectangle([W / 2 - 300, -10, W / 2 + 300, 330], outline=VERDE2, width=10)
    d.rectangle([W / 2 - 300, H - 330, W / 2 + 300, H + 10], outline=VERDE2, width=10)
    # marca arriba
    img.paste(logo, (70, 110), logo)
    d.text((70 + logo.width + 24, 128), "LA PELOTA HABLA", font=fuente("Black", 46), fill=BLANCO)
    # barra de progreso
    d.rectangle([70, 250, W - 70, 258], fill=VERDE2)
    d.rectangle([70, 250, 70 + (W - 140) * (idx + 1) / total, 258], fill=AMARILLO)
    # texto grande
    grande = escena.get("grande", "")
    tam = 200 if len(grande) <= 8 else 150 if len(grande) <= 14 else 110
    f = fuente("Black", tam)
    lineas = envolver(d, grande, f, W - 160)
    alto = len(lineas) * tam * 1.05
    y = H * 0.40 - alto / 2
    for ln in lineas:
        d.text((W / 2, y), ln, font=f, fill=AMARILLO, anchor="ma")
        y += tam * 1.05
    chico = escena.get("chico", "")
    if chico:
        fc = fuente("Bold", 58)
        y += 30
        for ln in envolver(d, chico, fc, W - 200):
            d.text((W / 2, y), ln, font=fc, fill=BLANCO, anchor="ma")
            y += 74
    return img


def trozos(texto, n=3):
    palabras = texto.split()
    return [" ".join(palabras[i:i + n]) for i in range(0, len(palabras), n)]


def ts(seg):
    h, r = divmod(seg, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace(".", ",")


def main(carpeta):
    guion = yaml.safe_load(open(os.path.join(carpeta, "guion.yaml"), encoding="utf-8"))
    salida = os.path.join(carpeta, "salida")
    os.makedirs(salida, exist_ok=True)
    tmp = tempfile.mkdtemp()
    logo = Image.open(os.path.join(RAIZ, "marca", "logo-verde.png")).convert("RGBA").resize((96, 96))
    mascara = Image.new("L", (96, 96), 0)
    ImageDraw.Draw(mascara).ellipse([0, 0, 95, 95], fill=255)
    logo.putalpha(mascara)

    escenas = guion["escenas"]
    audios, srt, t, sr = [], [], 0.0, 24000
    clips = []
    pausa = float(guion.get("pausa", 0.25))
    for i, esc in enumerate(escenas):
        a, sr = voz(esc["narracion"], guion.get("voz", "em_alex"), float(guion.get("velocidad", 1.08)))
        a = np.concatenate([a, np.zeros(int(sr * pausa), dtype=a.dtype)])
        dur = len(a) / sr
        audios.append(a)
        # subtítulos: trozos de 3 palabras repartidos según su largo
        partes = trozos(esc["narracion"])
        largo = sum(len(p) for p in partes)
        tt = t
        for p in partes:
            dp = (dur - pausa) * len(p) / largo
            srt.append((tt, tt + dp, p))
            tt += dp
        png = os.path.join(tmp, f"p{i}.png")
        placa(esc, i, len(escenas), logo).save(png)
        mp4 = os.path.join(tmp, f"c{i}.mp4")
        frames = max(1, round(dur * FPS))
        # zoom lento para que la placa no quede quieta
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", png, "-vf",
                        f"scale={W*2}:{H*2},zoompan=z='min(1+0.0009*on,1.12)':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS}",
                        "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", mp4], check=True)
        clips.append(mp4)
        t += dur

    wav = os.path.join(tmp, "voz.wav")
    sf.write(wav, np.concatenate(audios), sr)
    lista = os.path.join(tmp, "lista.txt")
    open(lista, "w").write("".join(f"file '{c}'\n" for c in clips))
    srt_path = os.path.join(salida, "subtitulos.srt")
    with open(srt_path, "w", encoding="utf-8") as fh:
        for n, (a, b, txt) in enumerate(srt, 1):
            fh.write(f"{n}\n{ts(a)} --> {ts(b)}\n{txt}\n\n")
    estilo = ("FontName=Inter,FontSize=14,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00111111,"
              "BorderStyle=1,Outline=3,Shadow=0,Alignment=2,MarginV=72")
    final = os.path.join(salida, "short.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista, "-i", wav,
                    "-vf", f"subtitles={srt_path}:fontsdir={FUENTES}:force_style='{estilo}'",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "160k", "-shortest", final], check=True)
    print(f"Listo: {final} ({t:.1f} s)")


if __name__ == "__main__":
    main(sys.argv[1])
