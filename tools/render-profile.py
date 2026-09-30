"""Generate original profile motion graphics. Requires Pillow.

Run: python tools/render-profile.py
Fonts: Segoe UI on Windows or DejaVu Sans on Linux. No network requests.
"""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
W = 1120
BG = (7, 12, 24)
TEXT = (239, 245, 255)
MUTED = (150, 171, 197)
TEAL = (79, 231, 206)
BLUE = (102, 175, 255)
PURPLE = (182, 144, 255)

def font(size, bold=False, mono=False):
    choices = (['C:/Windows/Fonts/consola.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'] if mono else
        ['C:/Windows/Fonts/segoeuib.ttf' if bold else 'C:/Windows/Fonts/segoeui.ttf',
         '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'])
    for p in choices:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    raise RuntimeError('Install Segoe UI or DejaVu Sans.')

def mix(a, b, amount):
    return tuple(round(x + (y-x)*amount) for x,y in zip(a,b))

def base(height):
    im = Image.new('RGB', (W,height), BG)
    d = ImageDraw.Draw(im)
    for y in range(height):
        d.line((0,y,W,y), fill=mix(BG,(15,24,43),y/height))
    for x in range(24,W,32):
        for y in range(24,height,32):
            d.point((x,y), fill=(33,47,65))
    d.rounded_rectangle((1,1,W-2,height-2), radius=22, outline=(45,63,85), width=2)
    return im

def label(d, xy, text, size=16, fill=MUTED, bold=False, mono=True):
    d.text(xy,text,font=font(size,bold,mono),fill=fill)

def ghost(d,cx,cy,radius=44,phase=0):
    cy += 5*math.sin(phase)
    x0,x1=cx-radius,cx+radius
    body=(188,255,242)
    d.ellipse((x0-12,cy-radius-12,x1+12,cy+radius+12),fill=(17,46,54))
    d.ellipse((x0,cy-radius,x1,cy+radius),fill=body)
    d.rectangle((x0,cy,x1,cy+radius-8),fill=body)
    for i in range(3):
        tx=x0+i*radius*2/3
        d.ellipse((tx,cy+radius-18,tx+radius*2/3,cy+radius+9),fill=body)
    blink=abs(phase/(2*math.pi)-.72)<.025
    for ex in (cx-radius*.33,cx+radius*.33):
        if blink:
            d.line((ex-4,cy-7,ex+4,cy-7),fill=BG,width=3)
        else:
            d.ellipse((ex-5,cy-15,ex+5,cy-1),fill=BG)

def packet(d,coords,phase,color,offset=0):
    lengths=[math.dist(a,b) for a,b in zip(coords,coords[1:])]
    for tail in range(10,-1,-1):
        pos=((phase/(2*math.pi)+offset-tail*.007)%1)*sum(lengths)
        for index,length in enumerate(lengths):
            if pos<=length:
                a,b=coords[index:index+2]
                f=pos/length
                x,y=a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f
                r=3 if tail else 5
                d.ellipse((x-r,y-r,x+r,y+r),fill=mix(BG,color,1-tail*.075))
                break
            pos-=length

def hero(phase):
    im=base(360)
    d=ImageDraw.Draw(im)
    label(d,(36,29),'ROBYRORO / BUILDER LOG',17,TEAL)
    label(d,(34,65),'ROBERT',57,TEXT,True,False)
    label(d,(32,128),'VIND-GARDOȘ',57,TEXT,True,False)
    label(d,(37,209),'PRODUCT  /  ENGINEERING  /  GROWTH',17)
    label(d,(37,245),'Recompensated · STRAT Agency',22,TEXT,False,False)
    d.line((37,305,310,305),fill=(46,69,92),width=2)
    label(d,(37,319),'ROMANIA  /  OPEN SOURCE',14)
    d.line((577,35,577,324),fill=(42,59,82))
    label(d,(617,30),'CURRENT FOCUS',16,TEAL)
    label(d,(615,56),'PROJECT GHOST',36,TEXT,True,False)
    label(d,(617,105),'CHROMIUM / PRE-ALPHA',15)
    cx,cy=876,226
    for radius in (80,101,123):
        d.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),outline=(35,57,76))
    for i,color in enumerate((TEAL,BLUE,PURPLE)):
        angle=phase+i*math.pi*2/3
        x,y=cx+math.cos(angle)*101,cy+math.sin(angle)*101
        d.ellipse((x-5,y-5,x+5,y+5),fill=color)
        start=(620,172+i*48)
        path=[start,(690,start[1]),(742,cy),(798,cy)]
        d.line(path,fill=mix(BG,color,.25),width=2)
        packet(d,path,phase,color,i/3)
        d.rounded_rectangle((612,start[1]-8,629,start[1]+8),radius=4,fill=color)
    ghost(d,cx,cy,42,phase)
    label(d,(1026,303),'01',29,TEAL)
    return im

def identities(phase):
    im=base(340)
    d=ImageDraw.Draw(im)
    label(d,(34,26),'PROJECT GHOST / IDENTITY CONCEPT',17,TEAL)
    d.rounded_rectangle((926,22,1086,56),radius=17,fill=(31,27,49),outline=(89,72,119))
    label(d,(950,30),'PRE-ALPHA',16,PURPLE)
    label(d,(34,61),'One browser. Separate contexts.',37,TEXT,True,False)
    for i,(name,caption,color) in enumerate((('WORK','Client accounts',TEAL),('PERSONAL','Your own space',BLUE),('RESEARCH','A fresh context',PURPLE))):
        x=34+i*363
        d.rounded_rectangle((x,126,x+326,264),radius=14,fill=(11,20,35),outline=mix(BG,color,.42),width=2)
        d.line((x+18,161,x+308,161),fill=(39,52,73))
        for k in range(3):
            d.ellipse((x+19+k*14,140,x+24+k*14,145),fill=color if k==0 else (57,70,88))
        label(d,(x+19,174),name,23,color,True,False)
        label(d,(x+19,209),caption,20,MUTED,False,False)
        d.ellipse((x+252,186,x+290,224),outline=mix(BG,color,.5),width=2)
        angle=phase+i*2*math.pi/3
        px,py=x+271+19*math.cos(angle),205+19*math.sin(angle)
        d.ellipse((px-3,py-3,px+3,py+3),fill=color)
        path=[(x+20,248),(x+308,248)]
        d.line(path,fill=mix(BG,color,.24),width=2)
        packet(d,path,phase,color,i/3)
    label(d,(35,292),'OPEN SOURCE  /  PRIVACY BY DESIGN  /  UNDER DEVELOPMENT',15)
    return im

def save_motion(name,render):
    frames=[render(i*2*math.pi/60) for i in range(60)]
    palette=frames[0].quantize(colors=128,dither=Image.Dither.NONE)
    indexed=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    indexed[0].save(ASSETS/name,save_all=True,append_images=indexed[1:],duration=100,loop=0,optimize=True,disposal=1)

def main():
    ASSETS.mkdir(exist_ok=True)
    save_motion('profile-signal.gif',hero)
    save_motion('ghost-identities.gif',identities)
    signature='''<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="100" viewBox="0 0 1120 100" role="img" aria-labelledby="title">
<title id="title">Robert Vind-Gardoș / robyroro — Build. Observe. Iterate.</title>
<rect width="1120" height="100" rx="18" fill="#0b1423"/>
<path d="M28 51H218M902 51h190" stroke="#284357"/>
<circle cx="28" cy="51" r="4" fill="#4fe7ce"/><circle cx="1092" cy="51" r="4" fill="#b690ff"/>
<text x="560" y="47" text-anchor="middle" font-family="Segoe UI,Arial,sans-serif" font-size="24" font-weight="700" fill="#eff5ff">BUILD. OBSERVE. ITERATE.</text>
<text x="560" y="73" text-anchor="middle" font-family="Consolas,monospace" font-size="14" letter-spacing="2" fill="#96abc5">ROBERT VIND-GARDOȘ / ROBYRORO</text>
</svg>'''
    (ASSETS/'build-signature.svg').write_text(signature,encoding='utf-8')
    for name in ('profile-signal.gif','ghost-identities.gif'):
        print(f'{name}: {(ASSETS/name).stat().st_size:,} bytes')

if __name__=='__main__':
    main()
