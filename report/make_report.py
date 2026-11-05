"""Builds report/rooftop_ci_resco_report.pdf from the same numbers the rest of the repo uses.

How this works: design numbers come from design/sizing.py, money numbers from resco/model.py,
and the pictures from drawings/ and a chart made here. The text states each number's status
(verified / partly verified / assumed) in plain words, matching VERIFICATION.md.
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle)

FONTS = "/usr/share/fonts/truetype/dejavu/"
for name, f in (("Serif", "DejaVuSerif.ttf"), ("Serif-Bold", "DejaVuSerif-Bold.ttf"), ("Serif-Italic", "DejaVuSerif-Italic.ttf"),
                ("Sans", "DejaVuSans.ttf"), ("Sans-Bold", "DejaVuSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(name, FONTS + f))     # DejaVu has the rupee sign and superscripts
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-Bold", italic="Serif-Italic", boldItalic="Serif-Bold")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(ROOT, "design"))
sys.path.insert(0, os.path.join(ROOT, "resco"))
import sizing   # noqa: E402
import model    # noqa: E402

D = sizing.design()
BASE = model.run(plant_kwp=307.4)
E = BASE["energy_year1"]

INK = colors.HexColor("#10202B")
STEEL = colors.HexColor("#51636F")
RULE = colors.HexColor("#C9D2D0")
SS = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=SS["Title"], fontName="Sans-Bold", fontSize=26, leading=28, alignment=0, textColor=INK, spaceAfter=10)
H2 = ParagraphStyle("H2", parent=SS["Heading2"], fontName="Sans-Bold", fontSize=15, leading=18, textColor=INK, spaceBefore=12, spaceAfter=5)
BODY = ParagraphStyle("B", parent=SS["BodyText"], fontName="Serif", fontSize=9.6, leading=14, textColor=INK, spaceAfter=5)
SMALL = ParagraphStyle("S", parent=BODY, fontSize=8.8, leading=11.5, textColor=STEEL)
NOTE = ParagraphStyle("N", parent=BODY, fontName="Serif-Italic", textColor=STEEL)


def P(t, s=BODY):
    return Paragraph(t, s)


def table(rows, widths, header=True):
    t = Table(rows, colWidths=widths, hAlign="LEFT")
    st = [("FONTNAME", (0, 0), (-1, -1), "Serif"), ("FONTSIZE", (0, 0), (-1, -1), 9.5),
          ("TEXTCOLOR", (0, 0), (-1, -1), INK), ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if header:
        st += [("FONTNAME", (0, 0), (-1, 0), "Sans-Bold"), ("LINEBELOW", (0, 0), (-1, 0), 1, INK)]
    t.setStyle(TableStyle(st))
    return t


def pic(path, width):
    from PIL import Image as PILImage
    w, h = PILImage.open(path).size
    return Image(path, width=width, height=width * h / w)


def wrap(rows):
    return [[Paragraph(str(c), ParagraphStyle("c", parent=BODY, fontSize=9.3, leading=12, spaceAfter=0)) for c in r] for r in rows]


def make_charts():
    curve = model.self_consumption_curve(step=10, lo=50, hi=500)
    fig, ax = plt.subplots(figsize=(7.2, 3.0))
    ax.plot([r["kwp"] for r in curve], [r["self_fraction"] * 100 for r in curve], color="#1D63B8", lw=2.5)
    ax.axvline(D["dc_kwp"], color="#C47A00", lw=1.5, ls="--")
    ax.text(D["dc_kwp"] + 6, 62, f"design {D['dc_kwp']:.0f} kWp", color="#C47A00", fontsize=9)
    ax.set_xlabel("Plant size (kWp)")
    ax.set_ylabel("Solar energy used on site (%)")
    ax.set_ylim(55, 102)
    ax.grid(alpha=.3)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "self_use_vs_size.png"), dpi=170)
    plt.close(fig)

    discs = [0.10, 0.20, 0.30, 0.40]
    fig, ax = plt.subplots(figsize=(7.2, 3.0))
    for capex, c in ((38, "#1D63B8"), (44, "#7A8FA0"), (50, "#C47A00")):
        ax.plot([d * 100 for d in discs], [model.run(resco_discount=d, capex_per_wp=capex)["project_irr"] * 100 for d in discs],
                marker="o", color=c, lw=2, label=f"capex ₹{capex}/Wp")
    ax.set_xlabel("RESCO discount to the grid energy charge (%)")
    ax.set_ylabel("RESCO return (%/year)")
    ax.grid(alpha=.3)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "irr_vs_discount.png"), dpi=170)
    plt.close(fig)


def build(path):
    make_charts()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=18 * mm,
                            title="Rooftop C&I solar design and RESCO model", author="Sagnik Kumar Nath")
    W = A4[0] - 40 * mm
    s = []
    s += [P("A 307 kWp rooftop plant, from survey to RESCO contract", H1),
          P("Design study for an assumed warehouse roof in Hooghly district, West Bengal", ParagraphStyle("sub", parent=BODY, fontName="Sans", fontSize=12, textColor=STEEL)),
          Spacer(1, 6),
          P("Design decisions, inputs and checks are mine; AI tools assisted with scripting and documentation. The roof and the client are assumed, not a real project. No AI-generated images are used; every drawing is produced by a script in the repository.", NOTE),
          P("Summary", H2),
          P(f"A metal-sheet shed with a 60 m ridge and two 20 m slopes (east and west, 7° tilt) takes {D['n_modules']} modules of 565 Wp, which is {D['dc_kwp']:.1f} kWp, on two 110 kVA inverters. "
            f"PVsyst predicts 409,153 kWh a year, and {E['self_fraction']*100:.0f}% of it is used by an assumed two-shift factory. "
            f"A RESCO that charges 20% below the grid energy charge of about ₹7.06 per kWh earns about {BASE['project_irr']*100:.0f}% a year (before tax and loan) on a capex of ₹{BASE['capex_rs']/1e7:.2f} crore, "
            f"paying back in {BASE['payback_years']:.1f} years, while the factory saves ₹{BASE['client_saving_year1_rs']/1e5:.1f} lakh in the first year."),
          P("The main lesson: at an 11 kV industrial energy charge of about ₹7 per kWh, a 20 to 30% discount gives the developer roughly 17 to 19% a year and the factory a real saving with no capex. The biggest risks are the capex (a quotation is needed), the actual yield (soiling and shading are not yet modelled) and the reading of the capacity cap."),
          P("How to read the marks", H2),
          P("<b>Verified</b>: taken from a document read this month (datasheet, utility document). <b>Partly verified</b>: from a secondary source or one source only. <b>Assumed</b>: a design choice or placeholder with its reason logged in ASSUMPTIONS.md. The full source list with links and access dates is in VERIFICATION.md in the repository."),
          PageBreak()]

    s += [P("1. Site and inputs", H2),
          P("Roof (assumed): ridge 60 m north-south; two slopes of 20 m facing east and west; tilt 7°; setbacks 1.0 m at eaves and gable ends and 0.5 m at the ridge; two translucent skylight strips per slope (1.2 m wide, 0.5 m clearance each side). Usable area 1,983 m² of 2,400 m² (83%)."),
          P("Client (assumed): light manufacturing, two shifts, 06:00 to 22:00 Monday to Saturday; 11 kV supply, WBSEDCL area, contract demand 350 kVA; 120,000 kWh a month; an hourly load profile for 8,760 hours was generated from that, with seasonal and weekday shape."),
          P("2. Sizing and strings", H2),
          P("Plant size is the smallest of three limits, then rounded to whole strings split equally between the slopes and across inverters."),
          table(wrap([["Limit", "Value", "Basis"],
                      ["Roof", f"{D['roof_limit_kwp']:.0f} kWp ({D['roof_modules']} modules)", "Layout rows after setbacks and skylights"],
                      ["Grid rule", f"{D['regulatory_limit_kw']:.0f} kW", "Lower of 500 kW or 350 kVA × 0.95 (reading is open; see section 4)"],
                      ["Daytime load", f"{D['load_limit_kwp']:.0f} kWp", "Mean working-day 08:00 to 16:00 load ÷ 0.80 kW peak AC per kWp (assumed)"],
                      ["Chosen", f"{D['dc_kwp']:.1f} kWp", f"{D['n_strings']} strings × {D['modules_per_string']} modules"]]), [28 * mm, 50 * mm, W - 78 * mm]),
          Spacer(1, 6),
          P("Strings: voltage rises as modules get cold, so the string must stay under the 1,000 V connector limit with a 5% margin at the coldest morning. Module open-circuit voltage at that temperature is 51.90 × (1 + 0.0026 × (25 − 3.4)) = 54.81 V. Seventeen modules give 931.8 V (6.8% under the limit); eighteen would give 986.7 V (1.3%, rejected). Hot, the maximum-power voltage with 17 modules is 629 V, inside the inverter's 200 to 1,000 V tracking window. Two strings per tracker draw 25.9 A against a 26 A limit; brief clipping above that is possible."),
          pic(os.path.join(ROOT, "drawings", "layout.png"), W * 0.86),
          P("Roof layout. Colours show the string grouping, which is indicative. The unused roof is kept as spare space.", SMALL),
          PageBreak()]

    s += [P("3. Yield (PVsyst 7.4.7)", H2),
          table(wrap([["Result", "Value"],
                      ["Energy to grid", "409,153 kWh a year"],
                      ["Specific production", "1,331 kWh per kWp a year"],
                      ["Performance ratio", "84.9%"],
                      ["Biggest losses", "Cell heat 7.5%; incidence angle 2.8%; inverter efficiency 2.1%; mismatch 2.0%"],
                      ["Inverter clipping at DC/AC 1.40", "0.32% of energy"]]), [60 * mm, W - 60 * mm]),
          Spacer(1, 6),
          P("What this run leaves out: soiling, shading and downtime are at zero; weather is Meteonorm synthetic data for Kolkata, about 30 km from Hooghly; the bifacial module is treated as single-sided; the inverter is the SG110CX-P2 variant because the plain SG110CX is not in the PVsyst database. The PVsyst licence showed 0 days remaining at the time. The full PVsyst report is in the repository (pvsyst/).", NOTE),
          P("4. Grid connection", H2),
          P("WBSEDCL's procedures (2025) let an HT consumer connect its plant at its low-voltage bus provided the net meter is on the high-voltage side of the transformer. Net metering is allowed up to the lower of 500 kW or the contract demand. The HV application fee is ₹5,000 and the FY 2025-26 feed-in rate for HV is ₹3.89 per kWh. A RESCO is allowed as a service provider. Plants above 170 kW are re-tested every two years."),
          P("<b>Open question.</b> The same document pairs 170 kW with 200 kVA (a power factor near 0.85). If the cap means kWp at that ratio, 350 kVA allows 297.5 kW, and the 307.4 kWp plant would be 9.9 kWp over; the fix would be 28 strings (269 kWp). The documents do not say which reading is right, so the larger plant is kept and the question flagged."),
          pic(os.path.join(ROOT, "drawings", "sld.png"), W),
          P("Single-line diagram. Breaker sizes are 125% of continuous current, rounded up (assumed until a protection study).", SMALL),
          PageBreak()]

    s += [P("5. RESCO financial model", H2),
          P("Each hour, the factory uses the lower of solar output and its load; surplus is exported. The RESCO charges the factory its tariff for the energy used; the factory saves the difference to the grid energy charge. Demand-charge savings are set to zero. Cash flows run for 25 years with degradation of 1% in year one and 0.4% a year after (from the module's linear warranty), a 2% yearly tariff rise (assumed), and maintenance at 1% of capex (assumed)."),
          table(wrap([["Base case", "Value", "Status"],
                      ["Capex", f"₹38 per Wp = ₹{BASE['capex_rs']/1e7:.2f} crore", "Partly verified (two installer pages)"],
                      ["Grid energy charge", "₹7.06 per kWh (Rate E(B), 11 kV; monsoon column, flat)", "Verified (FY 2025-26); MVCA extra, not included"],
                      ["RESCO tariff, year 1", f"₹{BASE['resco_tariff_year1']:.2f} per kWh (20% discount)", "Assumed discount"],
                      ["Solar used on site", f"{E['self_kwh']:,.0f} kWh ({E['self_fraction']*100:.1f}%)", "Computed"],
                      ["RESCO return", f"{BASE['project_irr']*100:.1f}% a year, no loan or tax", "Computed"],
                      ["RESCO payback", f"{BASE['payback_years']:.1f} years", "Computed"],
                      ["Factory saving, year 1 / 25 years", f"₹{BASE['client_saving_year1_rs']/1e5:.1f} lakh / ₹{BASE['client_saving_total_rs']/1e7:.2f} crore", "Computed"]]),
                [52 * mm, 62 * mm, W - 114 * mm]),
          Spacer(1, 8),
          pic(os.path.join(HERE, "irr_vs_discount.png"), W * 0.70),
          P("RESCO return as the discount and the capex change.", SMALL),
          pic(os.path.join(HERE, "self_use_vs_size.png"), W * 0.70),
          P("Share of solar energy used on site, by plant size. Above about 350 kWp the factory cannot absorb it at weekends, and the share falls.", SMALL),
          P("Reading: the self-use is robust because the plant is sized to the daytime load. The grid energy charge of about ₹7 per kWh is what makes the RESCO work. A client that bought the plant outright would see roughly a 4 to 5 year payback; a RESCO trades that for zero upfront cost and a 20% saving. If the factory is on the time-of-day scheme E(BT), solar offsets the 06:00 to 17:00 rate (about ₹6.94), and the return drops only slightly (about 19.0%). The demand charge (₹384 per kVA per month) is not counted as a saving. The sensitivity chart shows the return falling as the discount or the capex rises."),
          PageBreak()]

    s += [P("6. Commissioning and safety", H2),
          P("The repository holds a commissioning checklist with expected readings worked from the design. A healthy 17-module string should read about 882 V open-circuit at 25 °C cell temperature (836 V at 45 °C). The test list follows an installer's summary of IEC 62446-1; the standard's own text was not read, so acceptance ranges are common practice. The safety note covers falls through skylights, strings that cannot be switched off in daylight (up to about 932 V when cold), and DC fire."),
          P("7. Wind and structure", H2),
          P("The wind code gives 50 m/s for Kolkata (secondary source; Hooghly assumed the same). With all correction factors set to 1, the reference pressure is 0.6 × 50² = 1,500 Pa; this is illustration only because the factors were not looked up. The modules weigh 123 N/m², small beside wind uplift, so the check that matters is clamp pull-out and purlin strength on the real roof."),
          P("8. What is still open", H2),
          table(wrap([["Item", "What is needed"],
                      ["Real roof and client", "Survey, bill and 12 months of load data to replace the assumed ones"],
                      ["ALMM listing of this exact module", "Check the MNRE list for model BiN-08-565; Waaree's plant is listed, the model is not confirmed"],
                      ["Regulation gazette text", "Read the WBERC 2025 regulation for the capacity unit and RESCO terms"],
                      ["FY 2026-27 tariff order", "Not found; FY 2025-26 values used"],
                      ["Capex and maintenance", "Get a quotation; maintenance is assumed"],
                      ["PVsyst", "Add soiling and shading, re-run on a valid licence"],
                      ["Structure and fire", "Engineer's check and fire-authority requirements"]]), [60 * mm, W - 60 * mm]),
          P("9. Sources", H2),
          P("Full list with links and access dates: VERIFICATION.md in https://github.com/sagnikvolt/rooftop-ci-solar-resco. Main sources: WBSEDCL rooftop procedures (2025); WBSEDCL FY 2025-26 tariff order summary; Waaree ELITE BiN-08-565 datasheet; Sungrow SG110CX datasheet; PVsyst 7.4.7 simulation; installer cost pages (May and October 2026); a general RESCO guide; an installer summary of IEC 62446-1.", SMALL)]
    doc.build(s, onFirstPage=footer, onLaterPages=footer)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Sans", 7.5)
    canvas.setFillColor(STEEL)
    canvas.drawString(20 * mm, 10 * mm, "Rooftop C&I solar and RESCO model: design study, assumed site")
    canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, f"Page {doc.page}")
    canvas.restoreState()


if __name__ == "__main__":
    out = os.path.join(HERE, "rooftop_ci_resco_report.pdf")
    build(out)
    print("wrote", out, os.path.getsize(out), "bytes")
