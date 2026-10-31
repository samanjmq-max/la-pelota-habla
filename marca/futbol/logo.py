import math, sys
def pent(cx, cy, r, rot):
    return [(cx + r*math.sin(rot+2*math.pi*k/5), cy - r*math.cos(rot+2*math.pi*k/5)) for k in range(5)]
def pts(p): return " ".join(f"{x:.1f},{y:.1f}" for x,y in p)
def ball(cx, cy, R, ink):
    s = []
    s.append(f'<clipPath id="c"><circle cx="{cx}" cy="{cy}" r="{R}"/></clipPath>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#ffffff"/>')
    g = [f'<g clip-path="url(#c)" stroke="{ink}" stroke-width="{R*0.035:.1f}" stroke-linejoin="round">']
    center = pent(cx, cy, R*0.30, 0)
    g.append(f'<polygon points="{pts(center)}" fill="{ink}"/>')
    outers = []
    for k in range(5):
        a = 2*math.pi*k/5
        ox, oy = cx + 0.98*R*math.sin(a), cy - 0.98*R*math.cos(a)
        p = pent(ox, oy, R*0.30, a + math.pi)  # one vertex points to centre
        outers.append(p)
        g.append(f'<polygon points="{pts(p)}" fill="{ink}"/>')
        ix, iy = p[0]
        x0, y0 = center[k]
        g.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{ix:.1f}" y2="{iy:.1f}"/>')
    for k in range(5):
        a, b = outers[k], outers[(k+1)%5]
        # nearest pair of vertices between neighbouring outer pentagons
        best = min(((pa,pb) for pa in a for pb in b), key=lambda t:(t[0][0]-t[1][0])**2+(t[0][1]-t[1][1])**2)
        g.append(f'<line x1="{best[0][0]:.1f}" y1="{best[0][1]:.1f}" x2="{best[1][0]:.1f}" y2="{best[1][1]:.1f}"/>')
    g.append('</g>')
    s += g
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{ink}" stroke-width="{R*0.05:.1f}"/>')
    return "\n".join(s)
def logo(bg, accent, ink, name):
    cx, cy, R = 420, 380, 230
    # speech-bubble tail (drawn under the ball), pointing bottom-left
    tail = f'<polygon points="{cx-150},{cy+150} {cx-250},{cy+300} {cx-40},{cy+215}" fill="#ffffff" stroke="{ink}" stroke-width="11.5" stroke-linejoin="round"/>'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800" viewBox="0 0 800 800">
<rect width="800" height="800" fill="{bg}"/>
<circle cx="400" cy="400" r="330" fill="{accent}"/>
{tail}
{ball(cx, cy, R, ink)}
</svg>'''
    open(name+".svg","w").write(svg)
logo("#0B5D3B", "#11804F", "#111111", "logo-verde")
logo("#0E2A47", "#1F5C99", "#111111", "logo-azul")
