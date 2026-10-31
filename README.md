# Logística en 1 Minuto

Sistema de producción del canal [Logística en 1 Minuto](https://www.youtube.com/channel/UCYGlvUEFxyuPxuEhiAX9bbA): cómo se fabrica todo y cómo llega a tu casa, en español, sin rostro. (Antes: La Pelota Habla tv, canal de fútbol; el piloto quedó en `archivo/`.)

**Operación:** automatizada con Claude.

## Cómo funciona

1. **Tema y guion.** Claude investiga el tema (vidIQ, búsqueda web), verifica los datos y escribe `contenido/<nnn-tema>/guion.yaml` con sus fuentes.
2. **Producción.** `pipeline/producir.py` genera la voz (Kokoro, gratis y de uso comercial), las placas visuales, los subtítulos y el video vertical 1080×1920.
3. **Render automático.** Cada guion que se sube al repositorio se renderiza en GitHub Actions y queda como artefacto descargable por 14 días.
4. **Publicación.** Metricool publica en YouTube, TikTok, Instagram y Pinterest con los videos de la rama `videos`.

## Reglas del canal

- Solo video de stock con licencia libre (Pexels) o placas propias: nada de clips de terceros, fotos de prensa ni música con derechos.
- Todo dato del guion lleva fuente en el campo `fuentes`.
- Apto para toda la familia: sin insultos, apuestas ni violencia. El canal está marcado como "no creado para niños".
- Sin pagos, contratos ni cambios de configuración de la cuenta sin autorización del propietario.

## Estructura

| Carpeta | Contenido |
| --- | --- |
| `contenido/` | Un directorio por video: guion, fuentes y estado |
| `pipeline/` | Scripts de producción |
| `marca/` | Logo, banner y sus generadores |
| `skills/` | YouTube Agent Skill (MIT) para guiones, títulos y SEO |
| `assets/fuentes/` | Tipografía Inter (licencia SIL OFL) |

## Producir un video a mano

```bash
pip install -r requirements.txt
# modelos de voz en ./modelos (ver .github/workflows/producir.yml)
python pipeline/producir.py contenido/002-viaje-del-celular
```
