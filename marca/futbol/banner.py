import re
logo = open("logo-verde.svg").read()
inner = re.search(r'<rect[^>]*/>\s*<circle[^>]*/>\s*(.*)</svg>', logo, re.S).group(1)  # tail + ball, drop square bg and halo
W, H = 2560, 1440
line = "#14704A"
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<rect width="{W}" height="{H}" fill="#0B5D3B"/>
<g fill="none" stroke="{line}" stroke-width="10">
  <line x1="{W/2}" y1="0" x2="{W/2}" y2="{H}"/>
  <circle cx="{W/2}" cy="{H/2}" r="330"/>
  <rect x="-10" y="380" width="420" height="680"/>
  <rect x="{W-410}" y="380" width="420" height="680"/>
</g>
<rect x="0" y="{H/2-260}" width="{W}" height="520" fill="#0B5D3B" opacity="0.85"/>
<g transform="translate(450,490) scale(0.55)">{inner}</g>
<text x="850" y="725" font-family="Inter" font-weight="900" font-size="112" fill="#FFFFFF" letter-spacing="2">LA PELOTA HABLA</text>
<text x="854" y="805" font-family="Inter" font-weight="500" font-size="44" fill="#CFEFDF">Historias y datos del fútbol que nadie te contó</text>
</svg>'''
open("banner.svg","w").write(svg)
