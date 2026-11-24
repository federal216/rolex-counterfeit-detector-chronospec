import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

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

    def draw_page_decorations(self, page_count):
        self.saveState()
        # Dark Luxury Background
        self.setFillColor(colors.HexColor('#06090e'))
        self.rect(0, 0, 612, 792, fill=True, stroke=False)
        
        # Gold Top Accent Bar
        self.setFillColor(colors.HexColor('#d4af37'))
        self.rect(40, 755, 532, 4, fill=True, stroke=False)

        # Header Text
        self.setFont("Helvetica-Bold", 10)
        self.setFillColor(colors.HexColor('#ffffff'))
        self.drawString(40, 765, "CHRONOSPEC AI — HOROLOGICAL FORENSIC APPRAISAL DOSSIER")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#94a3b8'))
        self.drawRightString(572, 765, "SECURITY CODE: CS-2026-ROLEX-981")

        # Footer
        self.setStrokeColor(colors.HexColor('#1e293b'))
        self.setLineWidth(0.5)
        self.line(40, 45, 572, 45)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor('#64748b'))
        self.drawString(40, 32, "CHRONOSPEC HOROLOGICAL INTELLIGENCE &bull; VERIFIED SECONDARY MARKET AUDIT")
        self.drawRightString(572, 32, f"PAGE {self._pageNumber} OF {page_count} (OFFICIAL SAMPLE)")
        
        # Diagonal Sample Watermark on each page
        self.setFont("Helvetica-Bold", 54)
        self.setFillColor(colors.HexColor('#1b2436'), alpha=0.35)
        self.translate(306, 396)
        self.rotate(45)
        self.drawCentredString(0, 0, "SAMPLE APPRAISAL")
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=55,
        bottomMargin=55
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#ffffff'),
        spaceAfter=4
    )
    
    sub_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#f59e0b'),
        spaceAfter=15
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#d4af37'),
        spaceBefore=12,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=13,
        textColor=colors.HexColor('#cbd5e1')
    )

    bold_body = ParagraphStyle(
        'BoldBodyDark',
        parent=body_style,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#ffffff')
    )

    story = []

    # ================= PAGE 1 =================
    story.append(Paragraph("EXECUTIVE HOROLOGICAL APPRAISAL & VALUATION", title_style))
    story.append(Paragraph("TARGET ASSET: ROLEX COSMOGRAPH DAYTONA 'PANDA' (REF: 116500LN)", sub_style))

    # Overview Table
    overview_data = [
        [Paragraph("<b>Factory Reference:</b> 116500LN", body_style), Paragraph("<b>Production Era:</b> 2016 – 2023", body_style)],
        [Paragraph("<b>Calibre:</b> Rolex Cal. 4130 (Vertical Clutch, 72h)", body_style), Paragraph("<b>Case Spec:</b> 40mm x 12.2mm, 904L Oystersteel", body_style)],
        [Paragraph("<b>Bezel:</b> Monobloc Black Cerachrom Ceramic", body_style), Paragraph("<b>Water Resistance:</b> 100m / 330ft Triplock", body_style)],
        [Paragraph("<b>Inspected Listing:</b> Chrono24 Certified Private Dealer", body_style), Paragraph("<b>Serial Prefix:</b> Random 8-Digit Laser Rehaut", body_style)]
    ]
    t1 = Table(overview_data, colWidths=[260, 260])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0c121d')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1e293b')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#1b2436')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t1)
    story.append(Spacer(1, 15))

    # Valuation Metrics Matrix
    story.append(Paragraph("PRIMARY VALUATION & DEALER SPREAD MATRIX", h2_style))
    val_data = [
        [
            Paragraph("<font color='#94a3b8'>SELLER ASKING PRICE</font><br/><br/><b><font size='14' color='#ffffff'>$33,500</font></b><br/><font size='7' color='#64748b'>Dealer Listed Ask</font>", body_style),
            Paragraph("<font color='#94a3b8'>VERIFIED COMP BENCHMARK</font><br/><br/><b><font size='14' color='#10b981'>$29,800</font></b><br/><font size='7' color='#10b981'>Chrono24 / WatchCharts</font>", body_style),
            Paragraph("<font color='#94a3b8'>RECOMMENDED COUNTER-OFFER</font><br/><br/><b><font size='14' color='#f59e0b'>$27,900</font></b><br/><font size='7' color='#f59e0b'>Maximum Firm Wire Offer</font>", body_style)
        ]
    ]
    t_val = Table(val_data, colWidths=[173, 173, 174])
    t_val.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#0f172a')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#d4af37')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_val)
    story.append(Spacer(1, 15))

    # Applied Condition Deductions
    story.append(Paragraph("APPLIED VALUE TRAPS & DEDUCTION AUDIT", h2_style))
    ded_data = [
        [Paragraph("Missing Original Guarantee Card / NFC Papers", bold_body), Paragraph("-$3,500", bold_body)],
        [Paragraph("Softened Case Chamfers (Over-Polishing Wear)", bold_body), Paragraph("-$1,800", bold_body)],
        [Paragraph("Service Overdue (&gt;6 Years Unserviced Amplitude)", bold_body), Paragraph("-$1,200", bold_body)],
        [Paragraph("Minor Ceramic Bezel Rim Impact Scuff", bold_body), Paragraph("-$900", bold_body)],
        [Paragraph("<b>TOTAL JUSTIFIED NEGOTIATION DEDUCTION:</b>", bold_body), Paragraph("<b>-$7,400</b>", bold_body)]
    ]
    t_ded = Table(ded_data, colWidths=[380, 140])
    t_ded.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-2), colors.HexColor('#0c121d')),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#1e1b4b')),
        ('TEXTCOLOR', (1,-1), (1,-1), colors.HexColor('#f59e0b')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#312e81')),
        ('INNERGRID', (0,0), (-1,-2), 0.5, colors.HexColor('#1b2436')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_ded)

    # ================= PAGE 2 =================
    story.append(PageBreak())
    story.append(Paragraph("MACRO DIAL & TYPOGRAPHY FORENSICS", title_style))
    story.append(Paragraph("HIGH-MAGNIFICATION DIAL, HANDSTACK & CORONET VERIFICATION", sub_style))

    story.append(Paragraph("1. Laser-Etched Coronet (LEC) at 6 O'Clock Inspection", h2_style))
    story.append(Paragraph(
        "Authentic Rolex sapphire crystals manufactured post-2002 incorporate an ultra-fine coronet laser-etched directly into the lower plane of the sapphire crystal. Under 20x optical loupe inspection, the coronet must be composed of microscopic dashed dots rather than continuous engraved grooves. Counterfeit 'Clean/BTF' crystals exhibit heavy, opaque coronets visible under casual ambient light without directional beam illumination.",
        body_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("2. Subdial Concentric Ring Guilloché (Snailing) Sizing", h2_style))
    story.append(Paragraph(
        "The three subdials at 3, 6, and 9 o'clock on reference 116500LN feature micro-grooved concentric snailing with contrasting black outer tracks. Superclone dials frequently fail the inner track circumference ratio: the inner silver dial aperture must leave exactly 0.42mm of white dial separation from the outer tachymetre scale perimeter.",
        body_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("3. Central Handstack Pinion Height & Finishing", h2_style))
    story.append(Paragraph(
        "Rolex Calibre 4130 utilizes a proprietary stacked hand post. The central chronograph seconds hand must be capped with a rounded, mirror-finished dome. Replicas based on modified Shanghai 7750 movements feature a flat, hollow, or rough unburnished central pinion tube.",
        body_style
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("4. Pad-Printed Typography Font Kerning & Serifs", h2_style))
    story.append(Paragraph(
        "Inspection of 'ROLEX OYSTER PERPETUAL SUPERLATIVE CHRONOMETER OFFICIALLY CERTIFIED' under UV microscope verifies crisp paint edges without ink bleeding. The distinctive red 'DAYTONA' font must curve symmetrically above the 6 o'clock hour counter with equal font spacing.",
        body_style
    ))

    # ================= PAGE 3 =================
    story.append(PageBreak())
    story.append(Paragraph("CASE GEOMETRY & OVER-POLISHING STRESS AUDIT", title_style))
    story.append(Paragraph("LUG CHAMFERS, BEVEL CRISPNESS & BRACELET WEAR TOLERANCES", sub_style))

    story.append(Paragraph("Case Chamfer Geometry & Material Depletion", h2_style))
    story.append(Paragraph(
        "A pre-owned luxury watch polished by independent jewelers frequently suffers permanent value destruction due to excessive material removal. ChronoSpec inspects four critical structural planes:",
        body_style
    ))
    story.append(Spacer(1, 8))

    chamfer_table_data = [
        [Paragraph("<b>Inspection Point</b>", bold_body), Paragraph("<b>Factory Spec</b>", bold_body), Paragraph("<b>Listing Observed Condition</b>", bold_body)],
        [Paragraph("Lug Tip Width (Crown Side)", body_style), Paragraph("4.15mm &plusmn; 0.05mm", body_style), Paragraph("3.82mm (Material lost to buffing wheel)", body_style)],
        [Paragraph("Bevel Chamfer Crispness", body_style), Paragraph("Sharp 45° transition", body_style), Paragraph("Softened / rounded facet edge", body_style)],
        [Paragraph("Springbar Hole Protrusion", body_style), Paragraph("&gt; 1.8mm clearance", body_style), Paragraph("1.3mm (Thinning lug horn wall)", body_style)],
        [Paragraph("Crown Guard Asymmetry", body_style), Paragraph("Identical profile", body_style), Paragraph("Lower guard thinned by 0.3mm", body_style)]
    ]
    t_chamfer = Table(chamfer_table_data, colWidths=[160, 160, 200])
    t_chamfer.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#0c121d')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#334155')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#1e293b')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_chamfer)
    story.append(Spacer(1, 15))

    story.append(Paragraph("Oyster Bracelet Stretch & Clasp Tolerance", h2_style))
    story.append(Paragraph(
        "Reference 78590 solid-link Oyster bracelet with Easylink 5mm extension comfort system. Lateral deflection under gravity must remain under 15 degrees. Internal link pins exhibit moderate cosmetic scratching without structural pin necking.",
        body_style
    ))

    # ================= PAGE 4 =================
    story.append(PageBreak())
    story.append(Paragraph("CALIBRE ARCHITECTURE & OVERHAUL SCHEDULE", title_style))
    story.append(Paragraph("ROLEX IN-HOUSE CALIBRE 4130 MECHANICAL TOLERANCES", sub_style))

    story.append(Paragraph("Calibre 4130 Technical Specifications", h2_style))
    calibre_specs = [
        [Paragraph("<b>Parameter</b>", bold_body), Paragraph("<b>Factory Benchmark</b>", bold_body)],
        [Paragraph("Power Reserve", body_style), Paragraph("72 Hours (Continuous Chronograph Running)", body_style)],
        [Paragraph("Escapement Frequency", body_style), Paragraph("28,800 vph (4 Hertz)", body_style)],
        [Paragraph("Balance Spring", body_style), Paragraph("Paramagnetic Parachrom Bleu with Breguet overcoil", body_style)],
        [Paragraph("Chronograph Clutch", body_style), Paragraph("Vertical Friction Clutch with Column Wheel", body_style)],
        [Paragraph("Regulation System", body_style), Paragraph("Microstella variable inertia balance with gold screws", body_style)]
    ]
    t_cal = Table(calibre_specs, colWidths=[200, 320])
    t_cal.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#0c121d')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#334155')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#1e293b')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_cal)
    story.append(Spacer(1, 15))

    story.append(Paragraph("Timegrapher Health & Factory Overhaul Road-Map", h2_style))
    story.append(Paragraph(
        "• <b>Balance Amplitude:</b> Listing timing indicates 235° amplitude in dial-up position. Factory standard is 275°-310°. Indicates oil degradation across escapement and barrel arbor pivots.<br/>"
        "• <b>Beat Error:</b> Measured at 0.4ms (within acceptable operational limit &lt; 0.5ms).<br/>"
        "• <b>Full Service Recommendation:</b> Overhaul required within 12 months. Official Rolex Service Centre (RSC) complete movement overhaul standard fee is <b>$1,150 + tax</b>. Use this exact figure as non-negotiable buyer deduction.",
        body_style
    ))

    # ================= PAGE 5 =================
    story.append(PageBreak())
    story.append(Paragraph("DEALER COUNTER-OFFER & ESCROW PROTOCOL", title_style))
    story.append(Paragraph("VERBATIM NEGOTIATION SCRIPT & RISK-FREE ESCROW CHECKLIST", sub_style))

    story.append(Paragraph("Verbatim Counter-Offer Script for Dealer Communications", h2_style))
    story.append(Paragraph(
        "Copy and paste this professional, non-emotional negotiation script directly into Chrono24 messaging or email to the seller:",
        body_style
    ))
    story.append(Spacer(1, 6))

    script_text = (
        "<i>\"Hello [Seller Name],<br/><br/>"
        "Thank you for sharing the listing photos and serial records for the Rolex Cosmograph Daytona 116500LN. "
        "We have completed a formal horological comp appraisal against recent verified secondary transactions on Chrono24 and WatchCharts.<br/><br/>"
        "While we are prepared to transact immediately, our inspection identifies three mandatory condition adjustments: "
        "(1) The absence of the original punched/NFC guarantee card (-$3,500 replacement market liquidity discount), "
        "(2) Visible lug chamfer material loss from past rotary wheel polishing (-$1,800), and "
        "(3) Amplitude readings below 240 degrees necessitating an upcoming $1,150 RSC movement overhaul.<br/><br/>"
        "Factoring these elements against current cash comps ($29,800), our firm cash counter-offer is <b>$27,900 USD</b>. "
        "We have immediate funds ready to wire through Chrono24 Trusted Checkout / Escrow.com upon receipt of your updated offer.<br/><br/>"
        "Sincerely,<br/>[Your Name]\"</i>"
    )
    story.append(Paragraph(script_text, ParagraphStyle('ScriptBox', parent=body_style, backColor=colors.HexColor('#0c121d'), borderColor=colors.HexColor('#d4af37'), borderWidth=1, borderPadding=10, textColor=colors.HexColor('#fde68a'))))
    story.append(Spacer(1, 15))

    story.append(Paragraph("Pre-Wire Transfer Escrow Safety Checklist", h2_style))
    checklist_text = (
        "1. <b>Demand Escrow Protection:</b> Never execute direct bank wire transfers to private personal accounts without Chrono24 Buyer Protection or Escrow.com escrow lock.<br/>"
        "2. <b>Video Verification:</b> Demand a 10-second video of the watch set to a specific non-standard time (e.g. 10:19 and 42 seconds) to guarantee physical possession.<br/>"
        "3. <b>Serial Matching:</b> Verify that the rehaut serial matches the guarantee card and dealer commercial invoice exactly.<br/>"
        "4. <b>Insured Armored Courier:</b> Require delivery via insured armored transit (Ferrari Logistics, Malca-Amit, or DHL Express with signature confirmation)."
    )
    story.append(Paragraph(checklist_text, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated sample 5-page dossier: {filename}")

if __name__ == '__main__':
    out_dir1 = r'C:\chronospec-ai'
    out_dir2 = r'C:\hse-english-site'
    for d in [out_dir1, out_dir2]:
        os.makedirs(d, exist_ok=True)
        pdf_path = os.path.join(d, 'sample_chronospec_dossier.pdf')
        build_pdf(pdf_path)
