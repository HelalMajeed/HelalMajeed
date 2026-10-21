#!/usr/bin/env python3
"""Generate self-contained GitHub profile SVGs. Python standard library only."""
from pathlib import Path
import math

ROOT = Path(__file__).resolve().parents[1]
PALETTES = {
    "dark": dict(bg="#080d15", panel="#101a25", ink="#f0f5ef", muted="#a7b5c1", line="#263442", accent="#c6f88b", mint="#70d7bf", faint="#15212e"),
    "light": dict(bg="#f3f6ef", panel="#e6eee1", ink="#17261e", muted="#536659", line="#ccd8cb", accent="#396819", mint="#287c68", faint="#e5ede0"),
}


def orbit(cx, cy, r, c):
    rings = []
    for radius, alpha in [(r * 1.37, .42), (r * 1.19, .65), (r, .9)]:
        rings.append(f'<circle cx="{cx}" cy="{cy}" r="{radius:.2f}" fill="none" stroke="{c["line"]}" stroke-opacity="{alpha}"/>')
    ticks = []
    for i in range(72):
        theta = i * math.pi / 36
        ra = r * 1.37
        rb = ra + (8 if i % 6 == 0 else 3)
        x1, y1 = cx + ra * math.cos(theta), cy + ra * math.sin(theta)
        x2, y2 = cx + rb * math.cos(theta), cy + rb * math.sin(theta)
        ticks.append(f'<path d="M{x1:.2f} {y1:.2f}L{x2:.2f} {y2:.2f}" stroke="{c["muted"]}" opacity=".35"/>')
    return f'''
      <circle cx="{cx}" cy="{cy}" r="{r * 1.54}" fill="url(#halo)"/>
      {''.join(rings)}{''.join(ticks)}
      <ellipse cx="{cx}" cy="{cy}" rx="{r * 1.62}" ry="{r * .53}" transform="rotate(-30 {cx} {cy})" fill="none" stroke="{c['mint']}" opacity=".42"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#planet)"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#crescent)" mask="url(#cut)"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c['accent']}" stroke-opacity=".36"/>
      <path d="M{cx-r*.68} {cy+r*.72}Q{cx+r*.12} {cy+r*.93} {cx+r*.82} {cy-r*.44}" fill="none" stroke="{c['mint']}" opacity=".16"/>
      <g class="orbit" style="transform-origin:{cx}px {cy}px">
        <circle cx="{cx}" cy="{cy-r*1.19}" r="5" fill="{c['accent']}"/>
        <circle cx="{cx}" cy="{cy-r*1.19}" r="12" fill="{c['accent']}" opacity=".1"/>
      </g>
      <g class="orbit-slow" style="transform-origin:{cx}px {cy}px">
        <circle cx="{cx-r*1.37}" cy="{cy}" r="3" fill="{c['mint']}"/>
      </g>
    '''


def hero(theme, mobile=False):
    c = PALETTES[theme]
    w, h = (640, 710) if mobile else (1200, 530)
    cx, cy, r = (453, 467, 93) if mobile else (943, 265, 125)
    if mobile:
        words = f'''
          <text x="40" y="58" class="mono" font-size="17" letter-spacing="2">HELALMAJEED / SOFTWARE &amp; AI</text>
          <text x="36" y="151" class="title" font-size="82" letter-spacing="-4">Crescent.</text>
          <text x="40" y="219" class="headline" font-size="37">Turning ideas into</text>
          <text x="40" y="266" class="headline" font-size="37">intelligent systems.</text>
          <path d="M40 309H600" stroke="{c['line']}"/>
          <text x="40" y="365" class="mono" font-size="15" letter-spacing="2">CURRENT FOCUS</text>
          <text x="40" y="412" class="headline" font-size="28">AI products.</text>
          <text x="40" y="454" class="headline" font-size="28">Useful software.</text>
          <text x="40" y="496" class="headline" font-size="28">Thoughtful design.</text>
          <path d="M40 620H600" stroke="{c['line']}"/>
          <circle cx="47" cy="660" r="4" fill="{c['accent']}"/>
          <text x="63" y="666" class="mono" font-size="15" letter-spacing="1">BUILDING FROM IRAQ</text>
          <text x="600" y="666" text-anchor="end" class="mono" font-size="15">01 / ∞</text>
        '''
    else:
        words = f'''
          <text x="48" y="59" class="mono" font-size="15" letter-spacing="2.2">HELALMAJEED / SOFTWARE &amp; AI</text>
          <circle cx="1107" cy="53" r="4" fill="{c['accent']}"/>
          <text x="1122" y="59" class="mono" font-size="15">IQ</text>
          <path d="M48 84H1152" stroke="{c['line']}"/>
          <text x="43" y="213" class="title" font-size="108" letter-spacing="-5">Crescent.</text>
          <text x="48" y="283" class="headline" font-size="43" letter-spacing="-.8">Turning ideas into</text>
          <text x="48" y="339" class="headline" font-size="43" letter-spacing="-.8">intelligent systems.</text>
          <text x="50" y="391" class="mono" font-size="15" letter-spacing="1">AI PRODUCTS · USEFUL SOFTWARE · THOUGHTFUL DESIGN</text>
          <path d="M48 451H1152" stroke="{c['line']}"/>
          <circle cx="54" cy="487" r="4" fill="{c['accent']}"/>
          <text x="70" y="493" class="mono" font-size="14" letter-spacing="1.6">BUILDING FROM IRAQ</text>
          <text x="1152" y="493" text-anchor="end" class="mono" font-size="14" letter-spacing="1">EXPLORE THE WORK BELOW ↙</text>
        '''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
      <title id="title">Crescent — turning ideas into intelligent systems</title>
      <desc id="desc">HelalMajeed. AI products, useful software and thoughtful design. Building from Iraq. A custom crescent with slowly orbiting points.</desc>
      <defs>
        <radialGradient id="halo"><stop stop-color="{c['mint']}" stop-opacity=".12"/><stop offset="1" stop-color="{c['bg']}" stop-opacity="0"/></radialGradient>
        <radialGradient id="planet" cx="23%" cy="22%" r="85%"><stop stop-color="{c['panel']}"/><stop offset="1" stop-color="{c['bg']}"/></radialGradient>
        <linearGradient id="crescent" x1=".05" y1=".1" x2=".9" y2="1" gradientUnits="objectBoundingBox"><stop stop-color="{c['accent']}"/><stop offset=".65" stop-color="{c['mint']}"/><stop offset="1" stop-color="{c['mint']}" stop-opacity=".15"/></linearGradient>
        <mask id="cut"><rect width="{w}" height="{h}" fill="white"/><circle cx="{cx+r*.38}" cy="{cy-r*.25}" r="{r*.96}" fill="black"/></mask>
        <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".7" fill="{c['muted']}" opacity=".1"/></pattern>
        <clipPath id="frame"><rect width="{w}" height="{h}" rx="20"/></clipPath>
      </defs>
      <style>
        .title{{font-family:Arial,Helvetica,sans-serif;font-weight:700;fill:{c['ink']}}}
        .headline{{font-family:Arial,Helvetica,sans-serif;font-weight:400;fill:{c['ink']}}}
        .mono{{font-family:'Courier New',monospace;fill:{c['muted']}}}
        @keyframes orbit{{to{{transform:rotate(360deg)}}}}
        .orbit{{animation:orbit 45s linear infinite}}
        .orbit-slow{{animation:orbit 80s linear infinite reverse}}
        @media(prefers-reduced-motion:reduce){{.orbit,.orbit-slow{{animation:none}}}}
      </style>
      <g clip-path="url(#frame)">
        <rect width="{w}" height="{h}" fill="{c['bg']}"/>
        <rect width="{w}" height="{h}" fill="url(#dots)"/>
        {orbit(cx,cy,r,c)}
        {words}
      </g>
      <rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="19.5" fill="none" stroke="{c['line']}"/>
    </svg>'''


def divider(theme):
    c = PALETTES[theme]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="70" viewBox="0 0 1200 70" role="img" aria-label="Build. Learn. Iterate.">
      <path d="M0 35H417M783 35H1200" stroke="{c['line']}"/>
      <text x="600" y="41" text-anchor="middle" fill="{c['muted']}" font-family="'Courier New',monospace" font-size="17" letter-spacing="3">BUILD. LEARN. ITERATE.</text>
    </svg>'''


if __name__ == '__main__':
    out = ROOT / 'assets'
    out.mkdir(exist_ok=True)
    for theme in PALETTES:
        for mobile in (False, True):
            suffix = '-mobile' if mobile else ''
            (out / f'crescent-{theme}{suffix}.svg').write_text(hero(theme,mobile))
        (out / f'divider-{theme}.svg').write_text(divider(theme))
    print('Generated six self-contained SVG assets.')
