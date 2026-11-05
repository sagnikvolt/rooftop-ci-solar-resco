"""Builds the link-preview image (site/assets/og.png, 1200x630), the favicon and the PDF copy for the site.

Everything on the card is real: the roof layout drawing is the project's own drawing and the three
numbers come from resco/model.py. No generated pictures. Run: python3 report/make_og_image.py
"""
import os
import shutil
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "resco"))
import model  # noqa: E402

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf"
INK, PAPER, STEEL, SOLAR = (16, 32, 43), (237, 240, 238), (81, 99, 111), (196, 122, 0)
ASSETS = os.path.join(ROOT, "site", "assets")


def f(size, bold=True):
    return ImageFont.truetype(FONT if bold else FONT_R, size)


def og():
    r = model.run()
    im = Image.new("RGB", (1200, 630), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 1200, 12], fill=SOLAR)
    d.text((56, 52), "A 307 kWp rooftop plant,", font=f(54), fill=INK)
    d.text((56, 114), "from survey to RESCO contract", font=f(54), fill=INK)
    d.text((56, 190), "Design study, assumed warehouse roof in Hooghly district, West Bengal", font=f(24, False), fill=STEEL)
    kpis = [("19.4%".replace("19.4", f"{r['project_irr']*100:.1f}"), "RESCO return a year"),
            (f"₹{r['resco_tariff_year1']:.2f}", "per kWh, 20% below grid"),
            (f"₹{r['client_saving_year1_rs']/1e5:.1f} lakh", "client saves in year 1")]
    x = 56
    for big, small in kpis:
        d.text((x, 262), big, font=f(60), fill=SOLAR if x == 56 else INK)
        d.text((x, 340), small, font=f(22, False), fill=STEEL)
        x += 360
    lay = Image.open(os.path.join(ROOT, "site", "assets", "layout.png")).convert("RGB")
    lay = lay.crop((60, 70, lay.width - 40, lay.height - 40))      # drawing only, without its small title text
    h = 200
    lay = lay.resize((int(lay.width * h / lay.height), h), Image.LANCZOS)
    box = Image.new("RGB", (lay.width + 16, h + 16), (255, 255, 255))
    box.paste(lay, (8, 8))
    im.paste(box, (56, 398))
    d.text((56 + box.width + 24, 430), "Roof layout: 544 modules", font=f(26), fill=INK)
    d.text((56 + box.width + 24, 468), "409 MWh a year (PVsyst)", font=f(26, False), fill=STEEL)
    d.text((56 + box.width + 24, 506), "rooftop.sagniknath.in", font=f(26), fill=SOLAR)
    im.save(os.path.join(ASSETS, "og.png"), optimize=True)


def favicon():
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#10202B"/>'
           '<circle cx="46" cy="18" r="8" fill="#E7A92A"/><path d="M8 50 L32 24 L56 50 Z" fill="#5AA2EE"/>'
           '<path d="M32 24 L32 50 M20 37 L44 37" stroke="#10202B" stroke-width="2.5"/></svg>')
    open(os.path.join(ASSETS, "favicon.svg"), "w").write(svg)
    im = Image.new("RGB", (180, 180), INK)
    d = ImageDraw.Draw(im)
    d.ellipse([112, 28, 156, 72], fill=(231, 169, 42))
    d.polygon([(22, 146), (90, 68), (158, 146)], fill=(90, 162, 238))
    d.line([(90, 68), (90, 146)], fill=INK, width=6)
    d.line([(56, 107), (124, 107)], fill=INK, width=6)
    im.save(os.path.join(ASSETS, "apple-touch-icon.png"), optimize=True)


if __name__ == "__main__":
    og()
    favicon()
    shutil.copy(os.path.join(ROOT, "drawings", "sld.svg"), os.path.join(ASSETS, "sld.svg"))
    shutil.copy(os.path.join(HERE, "rooftop_ci_resco_report.pdf"), os.path.join(ASSETS, "rooftop_ci_resco_report.pdf"))
    print("wrote site/assets: og.png, favicon.svg, apple-touch-icon.png, sld.svg, report pdf")
