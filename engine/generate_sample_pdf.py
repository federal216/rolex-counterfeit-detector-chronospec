import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# Theme Palette (Luxury Dark Horology)
C_BG = colors.HexColor("#06090e")
C_SURFACE = colors.HexColor("#0d121d")
C_SURFACE_ALT = colors.HexColor("#121927")
C_BORDER = colors.HexColor("#1e293b")
C_GOLD = colors.HexColor("#d4af37")
C_GOLD_DIM = colors.HexColor("#997b24")
C_TEXT_WHITE = colors.HexColor("#f8fafc")
C_TEXT_MUTED = colors.HexColor("#94a3b8")
C_TEXT_ACCENT = colors.HexColor("#38bdf8")
C_ALERT_BG = colors.HexColor("#1f1418")
C_ALERT_BORDER = colors.HexColor("#7f1d1d")
C_ALERT_TEXT = colors.HexColor("#f87171")
C_SUCCESS_TEXT = colors.HexColor("#34d399")

TOTAL_PAGES = 10

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        # Header line
        self.setStrokeColor(C_GOLD)
        self.setLineWidth(1.5)
        self.line(40, 755, 572, 755)

        # Header Title
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(C_TEXT_WHITE)
        self.drawString(40, 762, "CHRONOSPEC AI — HOROLOGICAL FORENSIC APPRAISAL DOSSIER")
        
        self.setFont("Courier-Bold", 7)
        self.setFillColor(C_GOLD)
        self.drawRightString(572, 762, "SECURITY CODE: CS-2026-ROLEX-981")

        # Footer line
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(1)
        self.line(40, 42, 572, 42)

        # Footer labels
        self.setFont("Helvetica", 7)
        self.setFillColor(C_TEXT_MUTED)
        self.drawString(40, 32, "CHRONOSPEC HOROLOGICAL INTELLIGENCE • VERIFIED SECONDARY MARKET AUDIT")
        self.drawRightString(572, 32, f"PAGE {self._pageNumber} OF {total_pages} (OFFICIAL 10-PAGE DOSSIER)")

def draw_background(c, doc):
    c.saveState()
    # Dark luxury background fill
    c.setFillColor(C_BG)
    c.rect(0, 0, 612, 792, fill=True, stroke=False)
    # Subtle diagonal watermark
    c.setFont("Helvetica-Bold", 46)
    c.setFillColor(colors.HexColor("#1e293b"), alpha=0.06)
    c.saveState()
    c.translate(306, 396)
    c.rotate(45)
    c.drawCentredString(0, 0, "OFFICIAL FORENSIC DOSSIER")
    c.restoreState()
    c.restoreState()

def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    style_h1 = ParagraphStyle(
        'DocH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=C_TEXT_WHITE,
        spaceAfter=4
    )
    style_subtitle = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=C_GOLD,
        spaceAfter=12
    )
    style_body = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=C_TEXT_MUTED,
        spaceAfter=7
    )
    style_strong_body = ParagraphStyle(
        'DocStrongBody',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11.5,
        textColor=C_TEXT_WHITE,
        spaceAfter=7
    )
    style_section_title = ParagraphStyle(
        'SecTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=C_GOLD,
        spaceBefore=8,
        spaceAfter=5
    )

    story = []

    # =========================================================================
    # PAGE 1: EXECUTIVE HOROLOGICAL APPRAISAL & VALUATION
    # =========================================================================
    story.append(Paragraph("EXECUTIVE HOROLOGICAL APPRAISAL & VALUATION", style_h1))
    story.append(Paragraph("TARGET ASSET: ROLEX COSMOGRAPH DAYTONA 'PANDA' (REF: 116500LN)", style_subtitle))

    asset_data = [
        [Paragraph("<b>Factory Reference:</b> 116500LN", style_body), Paragraph("<b>Production Era:</b> 2016 – 2023", style_body)],
        [Paragraph("<b>Calibre:</b> Rolex Cal. 4130 (Vertical Clutch, 72h)", style_body), Paragraph("<b>Case Spec:</b> 40mm x 12.2mm, 904L Oystersteel", style_body)],
        [Paragraph("<b>Bezel:</b> Monobloc Black Cerachrom Ceramic", style_body), Paragraph("<b>Water Resistance:</b> 100m / 330ft Triplock", style_body)],
        [Paragraph("<b>Inspected Listing:</b> Chrono24 Certified Private Dealer", style_body), Paragraph("<b>Serial Prefix:</b> Random 8-Digit Laser Rehaut", style_body)]
    ]
    t_asset = Table(asset_data, colWidths=[266, 266])
    t_asset.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_SURFACE),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_asset)
    story.append(Spacer(1, 14))

    story.append(Paragraph("PRIMARY VALUATION & DEALER SPREAD MATRIX", style_section_title))
    val_data = [
        [
            Paragraph("<b>SELLER ASKING PRICE</b><br/><font size='14' color='#ffffff'><b>$33,500</b></font><br/><font color='#94a3b8' size='7'>Dealer Listed Ask</font>", style_body),
            Paragraph("<b>VERIFIED COMP BENCHMARK</b><br/><font size='14' color='#34d399'><b>$29,800</b></font><br/><font color='#94a3b8' size='7'>Chrono24 / WatchCharts</font>", style_body),
            Paragraph("<b>RECOMMENDED COUNTER-OFFER</b><br/><font size='14' color='#f59e0b'><b>$27,900</b></font><br/><font color='#94a3b8' size='7'>Maximum Firm Wire Offer</font>", style_body)
        ]
    ]
    t_val = Table(val_data, colWidths=[177, 177, 178])
    t_val.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_SURFACE_ALT),
        ('BOX', (0,0), (-1,-1), 1.5, C_GOLD),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    story.append(t_val)
    story.append(Spacer(1, 14))

    story.append(Paragraph("APPLIED VALUE TRAPS & DEDUCTION AUDIT", style_section_title))
    ded_data = [
        [Paragraph("<b>Missing Original Guarantee Card / NFC Papers</b>", style_body), Paragraph("<font color='#f87171'><b>-$3,500</b></font>", style_body)],
        [Paragraph("<b>Softened Case Chamfers (Over-Polishing Wear)</b>", style_body), Paragraph("<font color='#f87171'><b>-$1,800</b></font>", style_body)],
        [Paragraph("<b>Service Overdue (>6 Years Unserviced Amplitude)</b>", style_body), Paragraph("<font color='#f87171'><b>-$1,200</b></font>", style_body)],
        [Paragraph("<b>Minor Ceramic Bezel Rim Impact Scuff</b>", style_body), Paragraph("<font color='#f87171'><b>-$900</b></font>", style_body)],
        [Paragraph("<b>TOTAL JUSTIFIED NEGOTIATION DEDUCTION:</b>", style_strong_body), Paragraph("<font color='#f59e0b'><b>-$7,400</b></font>", style_strong_body)]
    ]
    t_ded = Table(ded_data, colWidths=[400, 132])
    t_ded.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-2), C_SURFACE),
        ('BACKGROUND', (0,-1), (-1,-1), C_SURFACE_ALT),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#4338ca")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ALIGN', (1,0), (1,-1), 'RIGHT'),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_ded)

    # =========================================================================
    # PAGE 2: MACRO DIAL & TYPOGRAPHY FORENSICS
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("MACRO DIAL & TYPOGRAPHY FORENSICS", style_h1))
    story.append(Paragraph("HIGH-MAGNIFICATION DIAL, HANDSTACK & CORONET VERIFICATION", style_subtitle))

    story.append(Paragraph("1. Laser-Etched Coronet (LEC) at 6 O'Clock Inspection", style_section_title))
    story.append(Paragraph(
        "Authentic Rolex sapphire crystals manufactured post-2002 incorporate an ultra-fine coronet laser-etched directly into the lower plane of the sapphire crystal. Under 20x optical loupe inspection, the coronet must be composed of microscopic dashed dots rather than continuous engraved grooves. Counterfeit 'Clean/BTF' crystals exhibit heavy, opaque coronets visible under casual ambient light without directional beam illumination.",
        style_body
    ))

    story.append(Paragraph("2. Subdial Concentric Ring Guilloché (Snailing) Sizing", style_section_title))
    story.append(Paragraph(
        "The three subdials at 3, 6, and 9 o'clock on reference 116500LN feature micro-grooved concentric snailing with contrasting black outer tracks. Superclone dials frequently fail the inner track circumference ratio: the inner silver dial aperture must leave exactly 0.42mm of white dial separation from the outer tachymetre scale perimeter.",
        style_body
    ))

    story.append(Paragraph("3. Central Handstack Pinion Height & Finishing", style_section_title))
    story.append(Paragraph(
        "Rolex Calibre 4130 utilizes a proprietary stacked hand post. The central chronograph seconds hand must be capped with a rounded, mirror-finished dome. Replicas based on modified Shanghai 7750 movements feature a flat, hollow, or rough unburnished central pinion tube.",
        style_body
    ))

    story.append(Paragraph("4. Pad-Printed Typography Font Kerning & Serifs", style_section_title))
    story.append(Paragraph(
        "Inspection of 'ROLEX OYSTER PERPETUAL SUPERLATIVE CHRONOMETER OFFICIALLY CERTIFIED' under UV microscope verifies crisp paint edges without ink bleeding. The distinctive red 'DAYTONA' font must curve symmetrically above the 6 o'clock hour counter with equal font spacing.",
        style_body
    ))

    dial_table = [
        [Paragraph("<b>Inspection Point</b>", style_strong_body), Paragraph("<b>OEM Factory Spec</b>", style_strong_body), Paragraph("<b>Counterfeit / Replica Traps</b>", style_strong_body)],
        [Paragraph("Coronet @ 6 (LEC)", style_body), Paragraph("Multi-layered micro dots, invisible in head-on light", style_body), Paragraph("Single solid laser burn, easily visible from any angle", style_body)],
        [Paragraph("Lume Quality (Chromalight)", style_body), Paragraph("Bright blue emission @ 480nm, crisp triangular indices", style_body), Paragraph("Green tint bleed, uneven granular application", style_body)],
        [Paragraph("Subdial Text Fonts", style_body), Paragraph("Sharp flat-top '3' on 30-min counter, micro serifs", style_body), Paragraph("Rounded '3', blotchy ink bleed at line intersections", style_body)]
    ]
    t_dial = Table(dial_table, colWidths=[120, 206, 206])
    t_dial.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_SURFACE_ALT),
        ('BACKGROUND', (0,1), (-1,-1), C_SURFACE),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(Spacer(1, 8))
    story.append(t_dial)

    # =========================================================================
    # PAGE 3: CASE GEOMETRY & OVER-POLISHING STRESS AUDIT
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("CASE GEOMETRY & OVER-POLISHING STRESS AUDIT", style_h1))
    story.append(Paragraph("LUG CHAMFERS, BEVEL CRISPNESS & BRACELET WEAR TOLERANCES", style_subtitle))

    story.append(Paragraph("Case Chamfer Geometry & Material Depletion", style_section_title))
    story.append(Paragraph(
        "A pre-owned luxury watch polished by independent jewelers frequently suffers permanent value destruction due to rotary abrasive buffing. Factory-correct Rolex Oyster cases possess razor-sharp 45° polished lateral chamfers separating the satin-brushed lug tops from mirror-polished case flanks. Rounded lug tips or uneven lug thicknesses indicate severe material depletion and justify an immediate $1,800 to $2,500 deduction.",
        style_body
    ))

    story.append(Paragraph("Caseback Fluting & Service Tool Marks", style_section_title))
    story.append(Paragraph(
        "The perimeter of genuine Rolex casebacks features exactly 144 precisely cut micro-serrations designed exclusively for Rolex tool die No. 1001. Gouges, slipped wrench scratches, or rounded teeth indicate uncertified watchmakers serviced the timepiece using generic suction or rubber ball wrenches.",
        style_body
    ))

    story.append(Paragraph("Oyster Bracelet Stretch & Pin Deformation", style_section_title))
    story.append(Paragraph(
        "Hold the watch horizontally by the case. An authentic 904L Oyster bracelet with less than 5% stretch drops less than 15mm from horizontal alignment. Sinking beyond 25mm indicates internal friction pin thinning and requires laser-welding or complete link replacement.",
        style_body
    ))

    case_data = [
        [Paragraph("<b>Metric</b>", style_strong_body), Paragraph("<b>Factory Factory Spec</b>", style_strong_body), Paragraph("<b>Audit Finding</b>", style_strong_body), Paragraph("<b>Valuation Impact</b>", style_strong_body)],
        [Paragraph("Crown Guard Symmetry", style_body), Paragraph("Balanced thickness, sharp inner bevel", style_body), Paragraph("Uneven lateral polish detected", style_body), Paragraph("-$800", style_strong_body)],
        [Paragraph("Lug Tip Thickness", style_body), Paragraph("Minimum 4.85mm across all 4 lugs", style_body), Paragraph("Bottom-left lug measures 4.52mm", style_body), Paragraph("-$1,000", style_strong_body)],
        [Paragraph("Caseback Serrations", style_body), Paragraph("144 razor teeth, zero slip gouges", style_body), Paragraph("Minor tool slip mark at 7 o'clock", style_body), Paragraph("-$400", style_strong_body)],
        [Paragraph("Bracelet Deflection", style_body), Paragraph("Horizontal deflection < 12mm", style_body), Paragraph("Deflection measured at 14.5mm", style_body), Paragraph("-$500", style_strong_body)]
    ]
    t_case = Table(case_data, colWidths=[120, 140, 172, 100])
    t_case.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_SURFACE_ALT),
        ('BACKGROUND', (0,1), (-1,-1), C_SURFACE),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(Spacer(1, 8))
    story.append(t_case)

    # =========================================================================
    # PAGE 4: CALIBRE ARCHITECTURE & OVERHAUL SCHEDULE
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("CALIBRE ARCHITECTURE & OVERHAUL SCHEDULE", style_h1))
    story.append(Paragraph("ROLEX IN-HOUSE CALIBRE 4130 MECHANICAL TOLERANCES", style_subtitle))

    story.append(Paragraph("Calibre 4130 Technical Specifications", style_section_title))
    calibre_specs = [
        [Paragraph("<b>Parameter</b>", style_strong_body), Paragraph("<b>Factory Benchmark</b>", style_strong_body)],
        [Paragraph("Power Reserve", style_body), Paragraph("72 Hours (Continuous Chronograph Running)", style_body)],
        [Paragraph("Escapement Frequency", style_body), Paragraph("28,800 vph (4 Hertz)", style_body)],
        [Paragraph("Coupling System", style_body), Paragraph("Vertical Clutch with Column Wheel (Instant zero-jitter start)", style_body)],
        [Paragraph("Oscillator Spring", style_body), Paragraph("Paramagnetic Blue Parachrom Hairspring with Breguet Overcoil", style_body)],
        [Paragraph("Traversing Balance Bridge", style_body), Paragraph("Dual-supported with two microstella regulating screws", style_body)]
    ]
    t_cal = Table(calibre_specs, colWidths=[200, 332])
    t_cal.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_SURFACE_ALT),
        ('BACKGROUND', (0,1), (-1,-1), C_SURFACE),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_cal)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Timegrapher Vibrograf Diagnostics & Overdue Service Warning", style_section_title))
    story.append(Paragraph(
        "A proper timegrapher test measures rate deviation, amplitude, and beat error across 5 positions (Dial Up, Dial Down, Crown Down, Crown Up, 12 Down). An authentic Rolex Calibre 4130 freshly serviced will maintain an amplitude of 280° to 310°. When amplitude falls below 265°, synthetic lubricant drying creates metal-on-metal pivot wear.",
        style_body
    ))

    time_data = [
        [Paragraph("<b>Testing Position</b>", style_strong_body), Paragraph("<b>Observed Amplitude</b>", style_strong_body), Paragraph("<b>Daily Rate (s/d)</b>", style_strong_body), Paragraph("<b>Beat Error</b>", style_strong_body), Paragraph("<b>Evaluation</b>", style_strong_body)],
        [Paragraph("Dial Up (CH)", style_body), Paragraph("258° (Degraded)", style_body), Paragraph("+2.2 s/d", style_body), Paragraph("0.1 ms", style_body), Paragraph("Service Overdue", style_strong_body)],
        [Paragraph("Dial Down (FH)", style_body), Paragraph("254° (Degraded)", style_body), Paragraph("+1.9 s/d", style_body), Paragraph("0.1 ms", style_body), Paragraph("Service Overdue", style_strong_body)],
        [Paragraph("Crown Down (6H)", style_body), Paragraph("242° (Low)", style_body), Paragraph("-1.1 s/d", style_body), Paragraph("0.2 ms", style_body), Paragraph("Friction Present", style_strong_body)],
        [Paragraph("Crown Left (9H)", style_body), Paragraph("240° (Low)", style_body), Paragraph("-1.4 s/d", style_body), Paragraph("0.2 ms", style_body), Paragraph("Friction Present", style_strong_body)]
    ]
    t_time = Table(time_data, colWidths=[110, 110, 100, 92, 120])
    t_time.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_SURFACE_ALT),
        ('BACKGROUND', (0,1), (-1,-1), C_SURFACE),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_time)

    # =========================================================================
    # PAGE 5: BEZEL CERAMIC ENGINEERING & INSERT FORENSICS
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("CERACHROM BEZEL FORENSICS & INSERT AUDIT", style_h1))
    story.append(Paragraph("MONOBLOC CERAMIC CHEMICAL MATRIX & PVD PLATINUM GRADUATION", style_subtitle))

    story.append(Paragraph("Cerachrom Composition & Sintering Science", style_section_title))
    story.append(Paragraph(
        "Rolex Cerachrom bezels are manufactured from ultra-pure zirconium dioxide (ZrO2) ceramic powder heated to 1,500°C, shrinking the ring by 25% and attaining diamond-grade scratch resistance (1,500 Vickers). Replicas utilize cheap molded polycarbonate or low-density sintered porcelain that cracks under minor lateral torque.",
        style_body
    ))

    story.append(Paragraph("Platinum PVD Deposit Depth & Font Bevels", style_section_title))
    story.append(Paragraph(
        "The numeral graduations on an authentic 116500LN tachymetre bezel are laser-carved into the ceramic, then coated with genuine micron-thin platinum deposit using Physical Vapour Deposition (PVD). Under optical microscopy, the platinum layer shows a soft silver sheen with microscopic brush texture. Fakes use white enamel paint or silver powder spray that flakes off when cleaned with isopropyl alcohol.",
        style_body
    ))

    bezel_table = [
        [Paragraph("<b>Inspection Vector</b>", style_strong_body), Paragraph("<b>OEM Rolex Spec</b>", style_strong_body), Paragraph("<b>Inspection Finding</b>", style_strong_body)],
        [Paragraph("Tachymetre Font Edges", style_body), Paragraph("Crisp 90° ceramic drop into recess", style_body), Paragraph("OEM Authentic - sharp stepped edge", style_body)],
        [Paragraph("Platinum Coating Purity", style_body), Paragraph("Genuine Pt950 sputtering, warm grey", style_body), Paragraph("Genuine Pt deposit confirmed", style_body)],
        [Paragraph("Triangular Dot at 12", style_body), Paragraph("Perfect isosceles triangle, sharp tip", style_body), Paragraph("Factory correct angle and alignment", style_body)],
        [Paragraph("Outer Edge Rim Impact", style_body), Paragraph("Completely smooth, zero micro-chips", style_body), Paragraph("<font color='#f87171'><b>Minor 0.3mm scuff at 82 units mark (-$900)</b></font>", style_body)]
    ]
    t_bez = Table(bezel_table, colWidths=[140, 192, 200])
    t_bez.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_SURFACE_ALT),
        ('BACKGROUND', (0,1), (-1,-1), C_SURFACE),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(Spacer(1, 6))
    story.append(t_bez)

    # =========================================================================
    # PAGE 6: CLASP CODE, END-LINK & SERIAL MATRIX
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("CLASP CODES, END-LINKS & SERIAL MATRIX", style_h1))
    story.append(Paragraph("REHAUT ENGRAVING, SOLID END LINKS & ERA COMPATIBILITY AUDIT", style_subtitle))

    story.append(Paragraph("Laser Rehaut Double-Etching & Crown Alignment", style_section_title))
    story.append(Paragraph(
        "On all post-2007 modern Rolex watches, the inner steel rehaut ring features repeated 'ROLEXROLEXROLEX' laser engraving. The Rolex coronet at 12 o'clock must align with mathematical precision to the 12 o'clock dial index. On the minute side (1 to 5 o'clock), the letter 'X' aligns with every hour marker; on the hour side (7 to 11 o'clock), the letter 'R' aligns with each marker. Any misaligned letter signifies a fake rehaut or dial swap.",
        style_body
    ))

    story.append(Paragraph("Solid End Link (SEL) Fitment & Springbar Recess", style_section_title))
    story.append(Paragraph(
        "Modern Daytona references use precision-machined Solid End Links (SEL). There must be zero light visible between the end link and the inner lug wall. Squeaking or loose fitment indicates non-original aftermarket replacement pins or stretched lug holes.",
        style_body
    ))

    clasp_table = [
        [Paragraph("<b>Component</b>", style_strong_body), Paragraph("<b>Expected OEM Identifier</b>", style_strong_body), Paragraph("<b>Observed Asset Status</b>", style_strong_body)],
        [Paragraph("Laser Rehaut Serial", style_body), Paragraph("Random 8-character alphanumeric", style_body), Paragraph("Random alphanumeric verified (clean cut)", style_body)],
        [Paragraph("Crown Alignment @ 12", style_body), Paragraph("Center of coronet exactly on 12 index", style_body), Paragraph("100% dead-center alignment verified", style_body)],
        [Paragraph("Clasp Hinge Code", style_body), Paragraph("Random 3-digit modern stamping", style_body), Paragraph("Matches modern Oysterlock era", style_body)],
        [Paragraph("Easylink Extension", style_body), Paragraph("5mm tool-free foldout, audible snap", style_body), Paragraph("Snaps firmly into spring bar channel", style_body)],
        [Paragraph("Springbar Spec", style_body), Paragraph("Heavy-duty 2.0mm shoulderless Rolex OEM", style_body), Paragraph("OEM Rolex springbars verified in place", style_body)]
    ]
    t_clasp = Table(clasp_table, colWidths=[140, 192, 200])
    t_clasp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_SURFACE_ALT),
        ('BACKGROUND', (0,1), (-1,-1), C_SURFACE),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(Spacer(1, 6))
    story.append(t_clasp)

    # =========================================================================
    # PAGE 7: NFC GUARANTEE CARD & DOCUMENT FORENSICS
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("NFC GUARANTEE CARD & DOCUMENT FORENSICS", style_h1))
    story.append(Paragraph("CHIP ENCRYPTION, UV FIBERS & PAPERWORK AUTHENTICATION", style_subtitle))

    story.append(Paragraph("Generation 3 Smart NFC Warranty Card Protocol", style_section_title))
    story.append(Paragraph(
        "Rolex introduced the current Generation 3 NFC guarantee card in mid-2020. The card embeds a high-frequency RFID/NFC chip beneath the green polymer surface. When scanned with an NFC-enabled smartphone, the authentic card opens the official rolex.com domain. Counterfeit cards use unprogrammed NFC tags, tags that link to fake replica phishing domains, or have no chip embedded at all.",
        style_body
    ))

    story.append(Paragraph("Micro-Optic UV Security Printing", style_section_title))
    story.append(Paragraph(
        "Under 365nm ultraviolet radiation, an authentic Rolex card illuminates a hidden pattern of green glowing lines and fluorescent micro-fibers embedded inside the plastic matrix. Replicas use surface-printed fluorescent ink that washes out or shows blurry boundaries under blacklight inspection.",
        style_body
    ))

    nfc_table = [
        [Paragraph("<b>Document Feature</b>", style_strong_body), Paragraph("<b>OEM Requirement</b>", style_strong_body), Paragraph("<b>Deduction Risk</b>", style_strong_body)],
        [Paragraph("NFC Antenna Trace", style_body), Paragraph("Invisible embedded dual-loop antenna", style_body), Paragraph("Fake tag / no tag: Invalidates provenance", style_body)],
        [Paragraph("Authorized Dealer Name", style_body), Paragraph("Laser printed by official Rolex AD", style_body), Paragraph("Blank or handwritten: Potential grey import", style_body)],
        [Paragraph("Serial Match", style_body), Paragraph("100% match with rehaut 8-digit code", style_body), Paragraph("Mismatch: Stolen or franken-card (-$5,000)", style_body)],
        [Paragraph("Current Asset Status", style_body), Paragraph("Original Card Missing From Listing", style_body), Paragraph("<font color='#f87171'><b>-$3,500 Applied Justified Deduction</b></font>", style_body)]
    ]
    t_nfc = Table(nfc_table, colWidths=[140, 192, 200])
    t_nfc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_SURFACE_ALT),
        ('BACKGROUND', (0,1), (-1,-1), C_SURFACE),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(Spacer(1, 6))
    story.append(t_nfc)

    # =========================================================================
    # PAGE 8: STOLEN REGISTRY & SERIAL TITLE PROTOCOL
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("STOLEN REGISTRY & LEGAL TITLE PROTOCOL", style_h1))
    story.append(Paragraph("CROSS-DATABASE SEARCH: THE WATCH REGISTER, ART LOSS & ENQUIRUS", style_subtitle))

    story.append(Paragraph("Global Secondary Title Risk Assessment", style_section_title))
    story.append(Paragraph(
        "Buying a pre-owned Rolex without a verified stolen registry certificate puts you at risk of total asset forfeiture. If a watch reported stolen to insurance companies or law enforcement is submitted to a Rolex Service Centre (RSC) anywhere in the world, Rolex policy mandates immediate police confiscation without buyer compensation.",
        style_body
    ))

    stolen_data = [
        [Paragraph("<b>Database Registry</b>", style_strong_body), Paragraph("<b>Records Scanned</b>", style_strong_body), Paragraph("<b>Search Result</b>", style_strong_body)],
        [Paragraph("The Watch Register (London)", style_body), Paragraph("Over 350,000 stolen serial records", style_body), Paragraph("<font color='#34d399'><b>CLEAN • ZERO MATCHES</b></font>", style_body)],
        [Paragraph("Enquirus (Richemont Global)", style_body), Paragraph("Industry-wide luxury police reports", style_body), Paragraph("<font color='#34d399'><b>CLEAN • ZERO MATCHES</b></font>", style_body)],
        [Paragraph("Art Loss Register Database", style_body), Paragraph("High-value international thefts", style_body), Paragraph("<font color='#34d399'><b>CLEAN • ZERO MATCHES</b></font>", style_body)],
        [Paragraph("Interpol Stolen Property List", style_body), Paragraph("Cross-border customs alerts", style_body), Paragraph("<font color='#34d399'><b>CLEAN • ZERO MATCHES</b></font>", style_body)]
    ]
    t_stolen = Table(stolen_data, colWidths=[170, 182, 180])
    t_stolen.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_SURFACE_ALT),
        ('BACKGROUND', (0,1), (-1,-1), C_SURFACE),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(Spacer(1, 6))
    story.append(t_stolen)

    story.append(Paragraph("Seller Warranty of Clear Title Mandate", style_section_title))
    story.append(Paragraph(
        "Never wire funds without demanding the seller include an express warranty of clear title on the commercial invoice: 'Seller warrants and guarantees that the timepiece (Serial: CS-2026-ROLEX-981) is free from all liens, claims, encumbrances, and has not been reported lost or stolen to any police agency or insurance underwriter.'",
        style_body
    ))

    # =========================================================================
    # PAGE 9: 10-POINT PRE-PURCHASE ESCROW SAFETY PROTOCOL
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("10-POINT PRE-PURCHASE ESCROW SAFETY PROTOCOL", style_h1))
    story.append(Paragraph("MANDATORY STEPS BEFORE RELEASING WIRE TRANSFER FUNDS", style_subtitle))

    escrow_steps = [
        "1. Never wire funds directly to private personal bank accounts; always use Chrono24 Buyer Protection or Escrow.com.",
        "2. Request a live video showing the watch set to a random requested time (e.g. 10:14 with date on 19).",
        "3. Cross-reference the seller's commercial tax ID or dealer license with local business registries.",
        "4. Mandate armored, fully insured transit (Ferrari Logistics, Malca-Amit, or FedEx Priority Direct Signature).",
        "5. Record continuous unboxing video with single-take footage showing parcel seals intact before opening.",
        "6. Perform immediate loupe inspection of laser-etched coronet at 6 o'clock before wearing the watch.",
        "7. Place watch on a vibrograf timegrapher within 24 hours of delivery to verify amplitude > 270°.",
        "8. Confirm bezel clicks and chronograph pushers snap crisp with zero spongy resistance or needle stutter.",
        "9. Check water-tightness on a dry pressure testing rig before any exposure to water or humidity.",
        "10. File any escrow dispute within the statutory 7-day buyer inspection window; never let the countdown expire."
    ]

    for step in escrow_steps:
        story.append(Paragraph(f"• <b>{step[:3]}</b> {step[3:]}", style_body))

    story.append(Spacer(1, 8))
    story.append(Paragraph("Escrow Hold Strategy", style_section_title))
    story.append(Paragraph(
        "If a dealer refuses independent escrow and demands direct wire transfer, treat this as an immediate red flag. ChronoSpec AI recommends walking away from any transaction where the seller refuses to accept third-party escrow verification.",
        style_strong_body
    ))

    # =========================================================================
    # PAGE 10: VERBATIM DEALER COUNTER-OFFER & NEGOTIATION SCRIPTS
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("DEALER COUNTER-OFFER & NEGOTIATION SCRIPTS", style_h1))
    story.append(Paragraph("VERBATIM COPY-PASTE SCRIPT FOR CHRONO24, EBAY & WHATSAPP", style_subtitle))

    story.append(Paragraph("Verbatim Counter-Offer Script for Dealer Communications", style_section_title))
    story.append(Paragraph(
        "Copy and paste this professional, non-emotional negotiation script directly into Chrono24 messaging or WhatsApp to secure your target price:",
        style_body
    ))

    script_text = (
        "<i>\"Hello [Dealer Name], thank you for sharing the listing details for the Rolex Daytona 116500LN. "
        "I have completed a forensic pre-purchase review and cross-referenced recent verified market comps from Chrono24 and WatchCharts. "
        "While the watch is appealing, our appraisal identifies three concrete value adjustments: the absence of the original guarantee card (-$3,500), "
        "noticeable chamfer softening from prior polishing (-$1,800), and an amplitude of 258° indicating an overdue RSC overhaul (-$1,200). "
        "Factoring in these mechanical and provenance realities, my firm purchase target is <b>$27,900 USD</b>. "
        "I am fully funded and prepared to initiate payment immediately via wire through Chrono24 Escrow upon agreement. "
        "Please let me know if we can finalize this today.\"</i>"
    )

    t_script = Table([[Paragraph(script_text, style_body)]], colWidths=[532])
    t_script.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_SURFACE_ALT),
        ('BOX', (0,0), (-1,-1), 1.5, C_GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
    ]))
    story.append(t_script)
    story.append(Spacer(1, 14))

    story.append(Paragraph("APPRAISAL CERTIFICATION & AUDIT SIGN-OFF", style_section_title))
    sign_data = [
        [Paragraph("<b>Lead Horologist:</b> Sofia Laurent, Master Horological Forensics", style_body), Paragraph("<b>Audit Engine:</b> ChronoSpec AI Autonomous V3.8", style_body)],
        [Paragraph("<b>Inspection Protocol:</b> ISO 9001 Horology Verification Standard", style_body), Paragraph("<b>Security Hash:</b> 8f72a91c0e3b994d", style_body)],
        [Paragraph("<b>Status:</b> OFFICIALLY CERTIFIED FOR SECONDARY ACQUISITION", style_strong_body), Paragraph("<b>Target Offer:</b> $27,900 FIRM", style_strong_body)]
    ]
    t_sign = Table(sign_data, colWidths=[266, 266])
    t_sign.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_SURFACE),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_sign)

    doc.build(
        story,
        onFirstPage=draw_background,
        onLaterPages=draw_background,
        canvasmaker=NumberedCanvas
    )
    print(f"[+] 10-Page Master Horological Forensic Dossier built: {output_path}")

if __name__ == '__main__':
    out = os.path.join(os.path.dirname(__file__), '..', 'sample_chronospec_dossier.pdf')
    build_pdf(out)
