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


def fm(size):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size)


def f(size, bold=True):
    return ImageFont.truetype(FONT if bold else FONT_R, size)


def og():
    """Report-style card: title block, layout drawing, three numbers, on white."""
    r = model.run()
    BLUE, RULE = (31, 95, 173), (205, 211, 217)
    im = Image.new("RGB", (1200, 630), (255, 255, 255))
    d = ImageDraw.Draw(im)
    # title block
    X0, Y0, X1, Y1 = 48, 44, 1152, 188
    d.rectangle([X0, Y0, X1, Y1], outline=INK, width=2)
    d.line([(X0, 120), (X1, 120)], fill=INK, width=2)
    for x in (740, 960):
        d.line([(x, Y0), (x, 120)], fill=INK, width=2)
    for x in (520, 880):
        d.line([(x, 120), (x, Y1)], fill=INK, width=2)
    def lab(x, y, t): d.text((x, y), t, font=f(13, False), fill=STEEL)
    lab(60, 52, "PROJECT"); d.text((60, 68), "307 kWp Rooftop Solar PV, C&I shed,", font=f(22), fill=INK)
    d.text((60, 93), "Hooghly district, West Bengal", font=f(22), fill=INK)
    lab(752, 52, "DOC NO."); d.text((752, 76), "RCI-307-DS-01", font=fm(20), fill=INK)
    lab(972, 52, "REV"); d.text((972, 76), "B", font=fm(20), fill=INK)
    lab(60, 128, "PREPARED BY"); d.text((60, 148), "Sagnik Kumar Nath, B.Tech EE (IEM Kolkata, 2027)", font=f(19, False), fill=INK)
    lab(532, 128, "STATUS"); d.text((532, 148), "Design study, not for construction", font=f(19, False), fill=INK)
    lab(892, 128, "DATE"); d.text((892, 148), "05-11-2026", font=fm(19), fill=INK)
    # drawing frame with caption strip
    lay = Image.open(os.path.join(ROOT, "site", "assets", "layout.png")).convert("RGB")
    lay = lay.crop((60, 70, lay.width - 40, lay.height - 40))
    h = 330
    lay = lay.resize((int(lay.width * h / lay.height), h), Image.LANCZOS)
    fx, fy = 48, 212
    d.rectangle([fx, fy, fx + lay.width + 16, fy + h + 16 + 30], outline=INK, width=2)
    im.paste(lay, (fx + 8, fy + 8))
    d.rectangle([fx + 1, fy + h + 16, fx + lay.width + 15, fy + h + 45], fill=(243, 245, 247))
    d.line([(fx, fy + h + 16), (fx + lay.width + 16, fy + h + 16)], fill=INK, width=2)
    d.text((fx + 10, fy + h + 22), "DWG-01", font=fm(15), fill=INK)
    d.text((fx + 84, fy + h + 22), "Roof layout", font=f(15, False), fill=INK)
    # key numbers table
    tx = fx + lay.width + 16 + 36
    d.text((tx, 212), "KEY DESIGN DATA", font=f(13, False), fill=STEEL)
    rows = [("Annual yield, P50", "409 MWh"),
            ("RESCO tariff, year 1", f"₹{r['resco_tariff_year1']:.2f} /kWh"),
            ("RESCO IRR", f"{r['project_irr']*100:.1f} %"),
            ("Client saving, yr 1", f"₹{r['client_saving_year1_rs']/1e5:.1f} lakh")]
    y = 238
    d.line([(tx, y), (1152, y)], fill=INK, width=2)
    for k, v in rows:
        d.text((tx, y + 14), k, font=f(18, False), fill=INK)
        d.text((1152, y + 10), v, font=fm(24), fill=BLUE, anchor="ra")
        y += 62
        d.line([(tx, y), (1152, y)], fill=RULE, width=1)
    d.text((tx, y + 18), "Assumed warehouse roof; values from", font=f(16, False), fill=STEEL)
    d.text((tx, y + 40), "the model in the repository.", font=f(16, False), fill=STEEL)
    d.text((tx, 586), "rooftop.sagniknath.in", font=fm(20), fill=BLUE)
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
