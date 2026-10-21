#!/usr/bin/env python3
"""Build original animated SVG panels and the image-led GitHub overview.

No external assets, JavaScript, network services, or runtime dependencies.
"""
from pathlib import Path
from html import escape
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'sections'
THEMES = {
    'dark': {'bg':'#090f17','surface':'#101c27','ink':'#eef4f2','muted':'#a5b6c3','line':'#273847','lime':'#c6f88b','mint':'#71d9c2','blue':'#8fbfff','gold':'#f4cf88','shadow':'#000000'},
    'light': {'bg':'#f4f7f1','surface':'#e9f0e5','ink':'#192c25','muted':'#51685c','line':'#c8d8ca','lime':'#426b20','mint':'#237d68','blue':'#326aab','gold':'#8a6020','shadow':'#486652'},
}


def text(x,y,s,size=27,cls='',fill=None,weight=None,extra=''):
    attrs=f'style="fill:{fill}"' if fill else ''
    if weight:attrs+=f' font-weight="{weight}"'
    return f'<text x="{x}" y="{y}" font-size="{size}" class="{cls}" {attrs} {extra}>{escape(s)}</text>'


def lines(x,y,ss,size=27,gap=39,cls='muted'):
    return ''.join(text(x,y+i*gap,s,size,cls) for i,s in enumerate(ss))


def rect(x,y,w,h,c,r=14,stroke=None,extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{c}" stroke="{stroke or "none"}" {extra}/>'


def pill(x,y,w,label,c,color=None):
    return rect(x,y,w,36,c['surface'],18,c['line'])+text(x+w/2,y+24,label,15,'mono',color or c['muted'],extra='text-anchor="middle"')


def arrow(x,y,c,scale=1):
    return f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{c}" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"><path d="M0 18L18 0M0 0H18V18"/></g>'


def icon(kind,c,size=180):
    """Artwork on a 180-unit canvas; nested wrappers keep motion local."""
    a,m,b=c['lime'],c['mint'],c['blue']
    base=f'<circle cx="90" cy="90" r="79" fill="{c["surface"]}" stroke="{c["line"]}"/><circle cx="90" cy="90" r="88" fill="none" stroke="{c["line"]}" stroke-dasharray="2 9"/>'
    if kind=='bot':
        art=f'''<g class="float"><path d="M90 50V36" stroke="{m}" stroke-width="3"/><circle cx="90" cy="29" r="7" fill="{a}" class="pulse"/>
          <rect x="38" y="53" width="104" height="82" rx="27" fill="{c['bg']}" stroke="{m}" stroke-width="3"/>
          <rect x="49" y="66" width="82" height="43" rx="16" fill="{c['surface']}"/>
          <g class="eyes" fill="{a}"><rect x="64" y="80" width="10" height="16" rx="5"/><rect x="106" y="80" width="10" height="16" rx="5"/></g>
          <path d="M76 118Q90 128 104 118" fill="none" stroke="{m}" stroke-width="3" stroke-linecap="round"/>
          <path d="M28 80V106M152 80V106" stroke="{m}" stroke-width="7" stroke-linecap="round"/></g>'''
    elif kind=='radiant':
        spokes=''.join(f'<path d="M90 22V43" transform="rotate({i*30} 90 90)"/>' for i in range(12))
        art=f'<g class="spin" style="transform-origin:90px 90px" stroke="{a}" stroke-width="3" stroke-linecap="round">{spokes}</g><circle cx="90" cy="90" r="35" fill="none" stroke="{m}" stroke-width="2"/><path d="M90 63L112 90L90 117L68 90Z" fill="{a}"/><circle cx="90" cy="90" r="10" fill="{c["bg"]}"/>'
    elif kind=='commerce':
        art=f'''<g class="float"><path d="M46 80L90 55L134 80V130L90 155L46 130Z" fill="{c['bg']}" stroke="{m}" stroke-width="2.5"/>
          <path d="M46 80L90 105L134 80M90 105V155M68 67L112 92" fill="none" stroke="{m}" stroke-width="2.5"/>
          <rect x="104" y="24" width="48" height="39" rx="12" fill="{a}"/><path d="M116 43L124 51L140 35" fill="none" stroke="{c['bg']}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M24 40H64M24 49H53" stroke="{c['muted']}" stroke-width="3" stroke-linecap="round"/></g>'''
    elif kind=='nodes':
        art=f'''<path d="M90 49V79H45V123M90 79H135V123" fill="none" stroke="{c['line']}" stroke-width="3"/>
          <path d="M90 49V79H45V123M90 79H135V123" class="trace" fill="none" stroke="{a}" stroke-dasharray="28 150" stroke-width="3"/>
          <g fill="{c['bg']}" stroke="{m}" stroke-width="2.5"><rect x="66" y="24" width="48" height="34" rx="10"/><rect x="21" y="121" width="48" height="34" rx="10"/><rect x="111" y="121" width="48" height="34" rx="10"/></g>
          <g fill="{a}"><circle cx="90" cy="41" r="5"/><circle cx="45" cy="138" r="5"/><circle cx="135" cy="138" r="5"/></g>'''
    elif kind=='terminal':
        art=f'''<g class="float"><rect x="28" y="42" width="124" height="99" rx="14" fill="{c['bg']}" stroke="{m}" stroke-width="2.5"/>
          <path d="M28 65H152" stroke="{c['line']}"/><g fill="{c['muted']}"><circle cx="42" cy="54" r="3"/><circle cx="53" cy="54" r="3"/><circle cx="64" cy="54" r="3"/></g>
          <path d="M49 88L62 99L49 110" fill="none" stroke="{a}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M78 110H104" class="pulse" stroke="{a}" stroke-width="4" stroke-linecap="round"/>
          <path d="M112 26L116 36L126 40L116 44L112 54L108 44L98 40L108 36Z" fill="{b}"/></g>'''
    elif kind=='chip':
        pins=''.join(f'<path d="M{p} 27V42M{p} 138V153M27 {p}H42M138 {p}H153"/>' for p in [60,80,100,120])
        art=f'<g stroke="{m}" stroke-width="3">{pins}</g><rect x="42" y="42" width="96" height="96" rx="18" fill="{c["bg"]}" stroke="{m}" stroke-width="2.5"/><rect x="59" y="59" width="62" height="62" rx="10" fill="none" stroke="{a}" stroke-dasharray="18 8" class="trace"/>'+text(90,101,'AI',30,fill=a,weight=700,extra='text-anchor="middle"')
    elif kind=='signal':
        art=f'<circle cx="90" cy="90" r="13" fill="{a}"/>'+''.join(f'<circle cx="90" cy="90" r="{r}" fill="none" stroke="{m}" opacity="{o}" class="pulse" style="animation-delay:{i*.5}s"/>' for i,(r,o) in enumerate([(31,.85),(50,.5),(68,.25)]))
    else:
        art=f'<path d="M45 100L90 52L135 100M90 52V138" fill="none" stroke="{a}" stroke-width="3"/>'
    return f'<g transform="scale({size/180})">{base}{art}</g>'


def panel(name,theme,h,body,compact=None,title='',description=''):
    c=THEMES[theme]
    css=f'''
      text{{font-family:Arial,Helvetica,sans-serif;fill:{c['ink']}}}
      .muted{{fill:{c['muted']}}}.mono{{font-family:'Courier New',monospace;letter-spacing:1.3px}}
      .compact{{display:none}}
      @keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}}
      @keyframes pulse{{0%,100%{{opacity:.45}}50%{{opacity:1}}}}
      @keyframes eyes{{0%,42%,47%,100%{{transform:scaleY(1)}}44%,45%{{transform:scaleY(.18)}}}}
      @keyframes spin{{to{{transform:rotate(360deg)}}}}
      @keyframes trace{{to{{stroke-dashoffset:-180}}}}
      @keyframes wave{{0%,100%{{transform:scaleY(.45)}}50%{{transform:scaleY(1)}}}}
      .float{{animation:float 5s ease-in-out infinite}}
      .pulse{{animation:pulse 4s ease-in-out infinite}}
      .eyes{{transform-origin:90px 88px;animation:eyes 8s ease-in-out infinite}}
      .spin{{animation:spin 35s linear infinite}}
      .trace{{animation:trace 10s linear infinite}}
      .wave{{animation:wave 1.8s ease-in-out infinite}}
      @media(max-width:600px){{.wide{{display:none}}.compact{{display:inline}}}}
      @media(prefers-reduced-motion:reduce){{.float,.pulse,.eyes,.spin,.trace,.wave{{animation:none!important}}}}
    '''
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{h}" viewBox="0 0 1000 {h}" role="img" aria-labelledby="title desc">
      <title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
      <defs><pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".65" fill="{c['muted']}" opacity=".12"/></pattern>
      <linearGradient id="edge"><stop stop-color="{c['lime']}"/><stop offset=".5" stop-color="{c['mint']}"/><stop offset="1" stop-color="{c['line']}"/></linearGradient>
      <clipPath id="frame"><rect x="1" y="1" width="998" height="{h-2}" rx="20"/></clipPath></defs>
      <style>{css}</style><g clip-path="url(#frame)">
      {rect(0,0,1000,h,c['bg'],20)}<rect width="1000" height="{h}" fill="url(#dots)"/>
      <path d="M30 1H970" stroke="url(#edge)" stroke-width="2" opacity=".7"/>
      <g class="{'wide' if compact else 'universal'}">{body}</g>{f'<g class="compact">{compact}</g>' if compact else ''}</g>
      <rect x=".5" y=".5" width="999" height="{h-1}" rx="19.5" fill="none" stroke="{c['line']}"/>
    </svg>'''
    (OUT/f'{name}-{theme}.svg').write_text(svg)


def intro(theme):
    c=THEMES[theme]
    body=text(38,43,'01 / THE BUILDER',16,'mono',c['mint'])+text(38,111,'Intelligence, made useful.',46,weight=700)
    body+=lines(38,157,['I build AI products and the software around them.','From the first interface to the systems behind it.'],23,34)
    body+=pill(38,230,180,'AI SYSTEMS',c)+pill(231,230,205,'PRODUCT DESIGN',c)+pill(449,230,183,'ENGINEERING',c)
    body+=f'<g transform="translate(772 60)">{icon("bot",c,180)}</g>'
    compact=text(38,51,'01 / THE BUILDER',26,'mono',c['mint'])+text(38,120,'Intelligence, made useful.',49,weight=700)
    compact+=lines(38,181,['AI products. Interfaces. APIs.','Built to help people do more.'],35,48)
    compact+=f'<g transform="translate(800 128)">{icon("bot",c,150)}</g>'
    panel('intro',theme,300,body,compact,'The builder','I build AI products and the software around them, from interfaces and APIs to the systems that keep them running. Useful intelligence, approachable tools, and working products.')


def flagship(theme):
    c=THEMES[theme]
    body=text(38,44,'02 / CURRENTLY BUILDING',16,'mono',c['mint'])+pill(805,21,157,'EDUCATION',c)
    body+=text(38,135,'OORR AI',80,fill=c['lime'],weight=700)+text(40,185,'Learning through conversation.',28,weight=700)
    body+=lines(40,235,['An Arabic-first AI learning platform','for Iraqi students. Ask, explore, practise,','and understand at your own pace.'],24,35)
    body+=rect(40,354,253,48,c['lime'],24)+text(63,385,'EXPLORE OORR AI',17,'mono',c['bg'],700)+arrow(258,369,c['bg'],.65)
    # Original illustration: connected chat, retrieval and voice surfaces.
    body+=f'''<path d="M572 190H617V302H710" fill="none" stroke="{c['line']}" stroke-width="2"/><path class="trace" d="M572 190H617V302H710" fill="none" stroke="{c['mint']}" stroke-width="2" stroke-dasharray="32 150"/>
      <g class="float">{rect(653,91,299,181,c['surface'],18,c['line'])}
      <circle cx="680" cy="117" r="5" fill="{c['lime']}"/>{text(697,123,'CONVERSATION',13,'mono')}
      {rect(679,145,211,36,c['bg'],10)}<path d="M694 159H844M694 169H796" stroke="{c['muted']}" stroke-width="3" stroke-linecap="round"/>
      {rect(719,197,207,50,c['bg'],10)}<path d="M735 214H898M735 229H865" stroke="{c['mint']}" stroke-width="3" stroke-linecap="round"/></g>
      {rect(712,288,240,97,c['bg'],18,c['line'])}{text(730,314,'VOICE INTERACTION',12,'mono',c['muted'])}'''
    for i,v in enumerate([10,16,29,21,37,14,24,33,18,28,36,15,20,11]):
        x=734+i*14
        body+=f'<rect x="{x}" y="{350-v/2}" width="5" height="{v}" rx="2.5" fill="{c["mint"]}" class="wave" style="transform-origin:{x}px 350px;animation-delay:{i*.13}s"/>'
    body+=f'<g transform="translate(548 58)">{icon("bot",c,100)}</g>'
    body+=f'<path d="M38 438H962" stroke="{c["line"]}"/>'
    for x,label,num in [(40,'Textbook retrieval','01'),(365,'Voice interaction','02'),(690,'Web + mobile','03')]:
        body+=text(x,480,num,15,'mono',c['mint'])+text(x+39,482,label,21)
    compact=text(38,53,'02 / CURRENTLY BUILDING',27,'mono',c['mint'])+text(38,164,'OORR AI',105,fill=c['lime'],weight=700)
    compact+=lines(40,233,['Arabic-first learning','for Iraqi students.'],43,58,cls='')
    compact+=text(40,355,'Chat · Voice · Study',34,'muted')+text(40,446,'EXPLORE OORR AI',31,'mono',c['lime'])+arrow(392,419,c['lime'],1.25)
    compact+=f'<g transform="translate(688 173)">{icon("bot",c,245)}</g>'
    panel('oorr',theme,520,body,compact,'OORR AI — learning through conversation','Currently building OORR AI, an Arabic-first learning platform for Iraqi students. Textbook retrieval, step-by-step explanations, voice interaction, and study across web and mobile. Open OORR AI.')


PROJECTS=[
    ('radiant','01','Radiant','AI products, experiments,','and developer tools.','AI / WEB / DEVELOPER EXPERIENCE','radiant','https://github.com/HelalMajeed/radiant'),
    ('freezone','02','FREEZONE','Storefront, management dashboard,','and a connected commerce API.','TYPESCRIPT / REACT / NODE.JS','commerce','https://github.com/HelalMajeed/freezone-website'),
    ('structures','03','Data structures','C and C++ implementations.','Understanding software from the foundations.','C / C++ / ALGORITHMS','nodes','https://github.com/HelalMajeed/Datastructure_Implementations'),
    ('experiments','04','Projects for fun','Web, desktop, and terminal experiments.','A place to build and learn by doing.','APPLICATIONS / GAMES / EXPERIMENTS','terminal','https://github.com/HelalMajeed/Projects4Fun'),
]


def projects(theme):
    c=THEMES[theme]
    heading=text(38,64,'03 / SELECTED WORK',26,'mono',c['mint'])+f'<path d="M418 55H900" stroke="{c["line"]}"/><circle class="pulse" cx="944" cy="55" r="5" fill="{c["lime"]}"/>'
    panel('work',theme,110,heading,title='Selected work',description='Four projects: Radiant, FREEZONE, Data structures, and Projects for fun.')
    for slug,num,title,d1,d2,tags,kind,url in PROJECTS:
        body=f'<g transform="translate(30 35)">{icon(kind,c,182)}</g>'
        body+=text(248,43,num+' / PROJECT',13,'mono',c['mint'])+text(247,98,title,43,weight=700)+arrow(925,62,c['mint'],1.1)
        body+=lines(248,141,[d1,d2],23,32)+text(248,221,tags,13,'mono',c['muted'])
        compact=f'<g transform="translate(34 61)">{icon(kind,c,154)}</g>'
        compact+=text(223,57,num+' / PROJECT',23,'mono',c['mint'])+text(221,125,title,52,weight=700)
        short={'radiant':'AI products & developer tools.','freezone':'Commerce, connected.','structures':'C · C++ · Algorithms','experiments':'Build. Explore. Learn.'}[slug]
        compact+=text(223,188,short,35,'muted')+arrow(922,76,c['mint'],1.2)
        panel(slug,theme,260,body,compact,title+' — project',f'{title}. {d1} {d2} {tags.replace(" / ",", ")}. Open the public repository.')


def tech_icon(key,x,y,c):
    color={'TS':c['blue'],'JS':c['gold'],'React':c['mint'],'Next.js':c['ink'],'Node.js':c['lime'],'Python':c['blue'],'SQL':c['mint'],'Docker':c['blue']}.get(key,c['mint'])
    s=rect(x,y,207,118,c['surface'],16,c['line'])
    if key=='React':
        s+=f'<g class="spin" style="transform-origin:{x+38}px {y+38}px" fill="none" stroke="{color}" stroke-width="1.7">'+''.join(f'<ellipse cx="{x+38}" cy="{y+38}" rx="23" ry="8" transform="rotate({a} {x+38} {y+38})"/>' for a in [0,60,120])+'</g>'+f'<circle cx="{x+38}" cy="{y+38}" r="4" fill="{color}"/>'
    elif key=='SQL':
        s+=f'<path d="M{x+20} {y+26}V{y+53}C{x+20} {y+65} {x+57} {y+65} {x+57} {y+53}V{y+26}" fill="none" stroke="{color}" stroke-width="2"/><ellipse cx="{x+38.5}" cy="{y+26}" rx="18.5" ry="8" fill="none" stroke="{color}" stroke-width="2"/>'
    else:
        symbol={'TS':'TS','JS':'JS','Next.js':'N','Node.js':'JS','Python':'Py','Docker':'▦'}.get(key,key)
        s+=rect(x+17,y+17,42,42,color,11)+text(x+38,y+45,symbol,21,fill=c['bg'],weight=700,extra='text-anchor="middle"')
    s+=text(x+18,y+94,{'TS':'TypeScript','JS':'JavaScript','SQL':'PostgreSQL'}.get(key,key),23,weight=700)
    return s


def toolkit(theme):
    c=THEMES[theme]
    body=text(38,44,'04 / TOOLKIT',16,'mono',c['mint'])+text(38,107,'Tools I build with.',46,weight=700)
    body+=f'<g transform="translate(847 24)">{icon("chip",c,99)}</g>'
    for i,key in enumerate(['TS','JS','React','Next.js','Node.js','Python','SQL','Docker']):
        body+=tech_icon(key,38+(i%4)*238,151+(i//4)*137,c)
    body+=f'<path d="M38 435H962" stroke="{c["line"]}"/>'
    body+=text(38,474,'AI SYSTEMS',13,'mono',c['mint'])+text(227,474,'RAG · LLM integration · Conversational interfaces',20)
    body+=text(38,515,'FOUNDATIONS',13,'mono',c['mint'])+text(227,515,'C · C++ · Algorithms · Linux · Git · Prisma',20)
    compact=text(38,51,'04 / TOOLKIT',27,'mono',c['mint'])+text(38,121,'Tools I build with.',59,weight=700)
    compact+=lines(38,209,['TypeScript · JavaScript','React · Next.js · Node.js','Python · PostgreSQL · Docker','C · C++ · Linux · Git','RAG · LLMs · Voice'],41,62)
    panel('toolkit',theme,565,body,compact,'Toolkit','AI: retrieval-augmented generation, LLM integration and conversational interfaces. Product: TypeScript, JavaScript, React, Next.js, Node.js and Python. Data and delivery: PostgreSQL, Prisma, Docker, Linux and Git. Foundations: C, C++ and algorithms.')


def exploring(theme):
    c=THEMES[theme]
    body=text(38,44,'05 / EXPLORING NEXT',16,'mono',c['mint'])+text(38,109,'Better ways to interact.',45,weight=700)
    body+=f'<path d="M195 205H805" fill="none" stroke="{c["line"]}" stroke-width="2"/><path d="M195 205H805" class="trace" stroke="{c["mint"]}" stroke-width="2" stroke-dasharray="35 145"/>'
    for x,kind,title,ss in [(38,'nodes','Agentic tutoring',['Explanation, practice,','and useful feedback.']),(359,'signal','Natural voice',['Interfaces that feel','easy to talk to.']),(680,'chip','Reliable answers',['Better retrieval.','Stronger evaluation.'])]:
        body+=f'<g transform="translate({x+95} 153)">{icon(kind,c,105)}</g>'
        body+=text(x+147,307,title,26,weight=700,extra='text-anchor="middle"')
        for j,s in enumerate(ss):body+=text(x+147,346+j*31,s,21,'muted',extra='text-anchor="middle"')
    compact=text(38,51,'05 / EXPLORING NEXT',27,'mono',c['mint'])+text(38,119,'Better ways to interact.',51,weight=700)
    compact+=lines(40,210,['01   Agentic tutoring','02   Natural voice','03   Reliable AI answers'],43,71)
    compact+=f'<g transform="translate(772 157)">{icon("signal",c,170)}</g>'
    panel('exploring',theme,425,body,compact,'What I am exploring','Agentic tutoring that connects explanation, practice and feedback. Natural voice interfaces. Retrieval and evaluation that make AI answers more dependable.')


def connect(theme):
    c=THEMES[theme]
    body=text(38,44,'06 / CONNECT',16,'mono',c['mint'])+text(38,113,'Let’s build something useful.',43,weight=700)
    body+=text(40,160,'AI, education, and thoughtful software.',24,'muted')
    body+=rect(40,202,279,49,c['lime'],24)+text(63,233,'CONNECT ON LINKEDIN',16,'mono',c['bg'],700)+arrow(284,217,c['bg'],.65)
    body+=f'<g transform="translate(810 59)">{icon("terminal",c,150)}</g>'
    compact=text(38,50,'06 / CONNECT',27,'mono',c['mint'])+lines(38,124,['Let’s build something','useful together.'],50,65,cls='')
    compact+=text(40,264,'CONNECT ON LINKEDIN',30,'mono',c['lime'])+arrow(490,237,c['lime'],1.25)
    panel('connect',theme,300,body,compact,'Connect with Crescent','Interested in AI, education or useful software? Connect with Helal Majeed on LinkedIn.')


def picture(name,alt,href=None,width='100%',section=True):
    path='./assets/sections/' if section else './assets/'
    tag=f'''<picture>
  <source media="(prefers-color-scheme: dark)" srcset="{path}{name}-dark.svg">
  <img src="{path}{name}-light.svg" width="{width}" alt="{escape(alt,quote=True)}">
</picture>'''
    if href:tag=f'<a href="{href}">\n{tag}\n</a>'
    return '<p>\n'+tag+'\n</p>\n'


def readme():
    blocks=[picture('crescent','Crescent / HelalMajeed — Turning ideas into intelligent systems. Building from Iraq.',section=False),
            picture('intro','I build AI products, interfaces, APIs and the systems around them. My focus: useful intelligence and approachable software.'),
            picture('oorr','OORR AI — Arabic-first learning for Iraqi students. Textbook retrieval, step-by-step explanations, voice, web and mobile. Explore OORR AI.','https://oorr.ai'),
            picture('work','Selected work: Radiant, FREEZONE, Data structures and Projects for fun.')]
    for slug,num,title,d1,d2,tags,kind,url in PROJECTS:
        blocks.append(picture(slug,f'{title}. {d1} {d2} Open the public repository.',url))
    blocks.extend([
        picture('toolkit','Toolkit: TypeScript, JavaScript, React, Next.js, Node.js, Python, PostgreSQL, Docker, Prisma, C, C++, Linux, Git, RAG, LLM integration and conversational interfaces.'),
        picture('exploring','Exploring agentic tutoring, natural voice, and more reliable answers through retrieval and evaluation.'),
        picture('connect','Let’s build something useful. Connect with Helal Majeed on LinkedIn.','https://www.linkedin.com/in/helal-majeed-528901239/'),
        '<details>\n<summary><strong>About, project links &amp; text version</strong></summary>\n\n'+(ROOT/'docs/PROFILE_TEXT.md').read_text().strip()+'\n\n[Connect on LinkedIn](https://www.linkedin.com/in/helal-majeed-528901239/)\n\n</details>\n',
        picture('divider','Build. Learn. Iterate.',section=False)
    ])
    (ROOT/'README.md').write_text('\n'.join(blocks))


def gallery():
    s='# Artwork preview\n\nActual GitHub image rendering at a 360-pixel width. Both themes are shown directly, independent of the selected GitHub theme.\n\n'
    for name in ['intro','oorr','radiant','freezone','structures','experiments','toolkit','exploring','connect']:
        s+=f'## {name}\n\n<img src="../assets/sections/{name}-dark.svg" width="360" alt="{name} dark compact preview"> <img src="../assets/sections/{name}-light.svg" width="360" alt="{name} light compact preview">\n\n'
    (ROOT/'docs/ARTWORK_PREVIEW.md').write_text(s)


if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True)
    for theme in THEMES:
        intro(theme);flagship(theme);projects(theme);toolkit(theme);exploring(theme);connect(theme)
    readme();gallery()
    print('Generated 20 animated section SVGs, the README, and the compact preview gallery.')
