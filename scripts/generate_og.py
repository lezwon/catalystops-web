#!/usr/bin/env python3
"""generate_og.py — Auto-generate OG images for all blog posts."""

import os, re, textwrap, urllib.request, zipfile, io
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BG=(15,17,23); CARD=(22,27,39); BORDER=(30,37,53); ORANGE=(249,115,22)
WHITE=(243,244,246); GRAY=(156,163,175); DGRAY=(75,85,99)
W,H=2400,1260; SCALE=2
FONT_DIR = Path(__file__).parent.parent / ".fonts"

def ensure_fonts():
    fv = FONT_DIR/"InterVariable.ttf"; fm = FONT_DIR/"Inter-Medium.ttf"
    if fv.exists() and fm.exists(): return str(fv), str(fm)
    print("Downloading Inter font...")
    FONT_DIR.mkdir(exist_ok=True)
    data = urllib.request.urlopen("https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip", timeout=60).read()
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        fv.write_bytes(z.open("InterVariable.ttf").read())
        fm.write_bytes(z.open("extras/ttf/Inter-Medium.ttf").read())
    return str(fv), str(fm)

def extract_meta(html):
    def get(pat, default=""):
        m = re.search(pat, html, re.DOTALL)
        return m.group(1).strip() if m else default
    badge   = get(r'<span class="badge">([^<]+)</span>')
    date    = get(r'<span class="text-xs text-muted">([A-Z][a-z]+ \d+, \d{4})</span>')
    version = get(r'<span class="text-xs text-muted font-mono[^"]*">(v[\d.]+)</span>')
    title_block = re.sub(r'<[^>]+>',' ', get(r'<h1[^>]*>(.*?)</h1>'))
    title_block = re.sub(r'\s+',' ', title_block).strip()
    parts = title_block.rsplit(None, 2)
    plain = ' '.join(parts[:-2]) if len(parts) > 2 else title_block
    accent = ' '.join(parts[-2:]) if len(parts) > 2 else ""
    desc = get(r'<meta name="description" content="([^"]+)"')
    return {"badge":badge or "Blog","date":date,"version":version,
            "title":plain,"accent":accent,"subtitle":desc[:120]}

def make_og(meta, fv, fm, out):
    img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img)
    M=80*SCALE; cx1,cy1,cx2,cy2=M,M,W-M,H-M
    d.rounded_rectangle([cx1,cy1,cx2,cy2],radius=20*SCALE,fill=CARD,outline=BORDER,width=SCALE*2)
    d.rounded_rectangle([cx1,cy1,cx2,cy1+10*SCALE],radius=4,fill=ORANGE)
    fb=ImageFont.truetype(fm,15*SCALE); fmt=ImageFont.truetype(fm,14*SCALE)
    ft=ImageFont.truetype(fv,62*SCALE); fs=ImageFont.truetype(fm,20*SCALE)
    fbr=ImageFont.truetype(fv,22*SCALE); fu=ImageFont.truetype(fm,13*SCALE)
    fver=ImageFont.truetype(fm,14*SCALE)
    px=cx1+50*SCALE; bx,by=px,cy1+65*SCALE
    bw=int(d.textlength(meta["badge"],font=fb))+32*SCALE; bh=34*SCALE
    d.rounded_rectangle([bx,by,bx+bw,by+bh],radius=999,fill=(40,20,5),outline=(120,55,10),width=SCALE)
    d.text((bx+16*SCALE,by+9*SCALE),meta["badge"],fill=ORANGE,font=fb)
    if meta["date"]: d.text((bx+bw+20*SCALE,by+10*SCALE),meta["date"],fill=GRAY,font=fmt)
    y=cy1+140*SCALE
    for line in textwrap.wrap(meta["title"],width=28)[:2]:
        d.text((px,y),line,fill=WHITE,font=ft); y+=78*SCALE
    if meta["accent"]: d.text((px,y),meta["accent"],fill=ORANGE,font=ft); y+=78*SCALE
    y+=8*SCALE
    for line in textwrap.wrap(meta["subtitle"],width=62)[:2]:
        d.text((px,y),line,fill=GRAY,font=fs); y+=32*SCALE
    div_y=cy2-70*SCALE
    d.line([(px,div_y),(cx2-50*SCALE,div_y)],fill=BORDER,width=SCALE)
    d.text((px,cy2-58*SCALE),"CatalystOps",fill=ORANGE,font=fbr)
    d.text((px,cy2-32*SCALE),"spendops.dev",fill=DGRAY,font=fu)
    if meta["version"]:
        vw=int(d.textlength(meta["version"],font=fver))+28*SCALE
        px2=cx2-50*SCALE-vw; pcy=cy2-45*SCALE
        d.rounded_rectangle([px2,pcy-14*SCALE,px2+vw,pcy+14*SCALE],radius=8*SCALE,fill=BORDER)
        d.text((px2+14*SCALE,pcy-8*SCALE),meta["version"],fill=GRAY,font=fver)
    Path(out).parent.mkdir(parents=True,exist_ok=True)
    img.save(out,"PNG",optimize=True)
    print(f"  → {out} ({Path(out).stat().st_size//1024}KB)")

def main():
    fv,fm=ensure_fonts()
    blog_root=Path(__file__).parent.parent/"blog"
    posts=[p for p in sorted(blog_root.glob("*/index.html")) if p.parent!=blog_root]
    print(f"Found {len(posts)} post(s)")
    for p in posts:
        meta=extract_meta(p.read_text(encoding="utf-8"))
        print(f"Generating: {p.parent.name}")
        make_og(meta,fv,fm,str(p.parent/"og.png"))
    print("Done.")

if __name__=="__main__":
    main()
