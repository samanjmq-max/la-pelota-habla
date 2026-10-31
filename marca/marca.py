NAR, NAR2, AZUL, BL = "#F26B1D", "#D9560E", "#0E2A47", "#FFFFFF"
def icono(x, y, s):
    """Contenedor con flecha: el producto en viaje. (x,y) esquina, s escala (1 = 400px)."""
    g = f'<g transform="translate({x},{y}) scale({s})">'
    g += f'<rect x="20" y="110" width="290" height="180" rx="18" fill="{BL}"/>'
    for i in range(6):
        g += f'<rect x="{48+i*42}" y="135" width="18" height="130" rx="6" fill="{AZUL}" opacity="0.85"/>'
    g += f'<path d="M300 200 H360" stroke="{BL}" stroke-width="34" stroke-linecap="round"/>'
    g += f'<path d="M335 150 L392 200 L335 250" fill="none" stroke="{BL}" stroke-width="34" stroke-linecap="round" stroke-linejoin="round"/>'
    return g + '</g>'
logo = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800">
<rect width="800" height="800" fill="{NAR}"/><circle cx="400" cy="400" r="330" fill="{NAR2}"/>
{icono(195, 130, 1.0)}
<text x="400" y="640" text-anchor="middle" font-family="Inter" font-weight="900" font-size="150" fill="{BL}">1 MIN</text>
</svg>'''
open("logo.svg","w").write(logo)
W,H=2560,1440
banner = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" fill="{AZUL}"/>
<g stroke="#17406B" stroke-width="6" fill="none">''' + "".join(f'<line x1="{x}" y1="0" x2="{x-500}" y2="{H}"/>' for x in range(0, W+600, 160)) + f'''</g>
<rect x="0" y="{H/2-250}" width="{W}" height="500" fill="{AZUL}" opacity="0.92"/>
<rect x="520" y="560" width="300" height="300" rx="40" fill="{NAR}"/>
{icono(545, 570, 0.64)}
<text x="870" y="655" font-family="Inter" font-weight="900" font-size="112" fill="{BL}">LOGÍSTICA</text>
<text x="870" y="770" font-family="Inter" font-weight="900" font-size="112" fill="{NAR}">EN 1 MINUTO</text>
<text x="874" y="845" font-family="Inter" font-weight="500" font-size="44" fill="#FFC9A6">Comercio exterior y logística, explicados simple</text>
</svg>'''
open("banner.svg","w").write(banner)
