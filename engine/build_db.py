import json
import os

watch_db = {
    "version": "2026.1",
    "updated_at": "2026-11-24",
    "market_benchmark": "Chrono24, WatchCharts, Antiquorum, Phillips New York",
    "models": {
        "rolex_sub_126610ln": {
            "name": "Rolex Submariner Date 41mm",
            "reference": "126610LN",
            "production_years": "2020 - Present",
            "calibre": "Rolex Calibre 3235 (70-hour Chronergy Escapement)",
            "retail_msrp": 10250,
            "fair_market_avg": 13800,
            "market_range": [12800, 15200],
            "common_issues": [
                {"issue": "Calibre 3235 Low Amplitude Drop", "cost": 1100, "detail": "Known lubrication migration on escape wheel pivot causing amplitude to drop below 200 degrees after 18-24 months."},
                {"issue": "Cerachrom Bezel Numbering Graying", "cost": 1600, "detail": "Platinum PVD coating in recessed numerals washing out from ultrasonic cleaning solutions."},
                {"issue": "Glidelock Clasp Track Debris Jamming", "cost": 650, "detail": "Fine grit accumulating in the toothed adjustment track preventing micro-extension lock."}
            ],
            "counterfeit_risk_zones": [
                "Laser-etched coronet (LEC) at 6 o'clock must be invisible to naked eye; visible under 10x loop only as dashed micro-dots.",
                "Hand stack height: Hour hand bottom, Minute hand middle, Seconds hand top on a convex central pinion.",
                "Serial number laser engraved on inner rehaut: Lettering must align precisely with dial minute track hashes.",
                "New warranty card contains NFC chip reading official rolex.com redirect with authorized dealer code."
            ],
            "negotiation_deductions": {
                "missing_warranty_card": 2800,
                "missing_original_box": 650,
                "overpolished_lugs": 1500,
                "missing_bracelet_links": 350,
                "service_overdue_5yrs": 950
            }
        },
        "rolex_sub_116610ln": {
            "name": "Rolex Submariner Date 'Maxi Case' 40mm",
            "reference": "116610LN",
            "production_years": "2010 - 2020",
            "calibre": "Rolex Calibre 3135 (Parachrom Bleu Hairspring)",
            "retail_msrp": 8550,
            "fair_market_avg": 11400,
            "market_range": [10500, 12600],
            "common_issues": [
                {"issue": "Rotor Axle Jewel Wear (Scraping Bridge)", "cost": 950, "detail": "Jeweled bearing on oscillating weight wears out if dried of oil, causing brass rotor to scrape mainplate."},
                {"issue": "Maxi Case Softened Chamfers", "cost": 1400, "detail": "Careless independent polishing erodes the crisp factory chamfer bevels, permanently devaluing case."},
                {"issue": "Cyclops 2.5x Date Magnification Distortion", "cost": 450, "detail": "Aftermarket replacement sapphire crystals feature substandard 1.5x magnification or poor AR coating."}
            ],
            "counterfeit_risk_zones": [
                "Rehaut engraving: ROLEXROLEX alignment (R aligns with 1-5 minute ticks, X aligns with 7-11 minute ticks).",
                "Bezel click spring mechanism: 120 crisp tactile clicks with zero back-play or wobble."
            ],
            "negotiation_deductions": {
                "missing_warranty_card": 2200,
                "missing_original_box": 550,
                "overpolished_lugs": 1800,
                "service_overdue": 850
            }
        },
        "rolex_daytona_116500ln": {
            "name": "Rolex Cosmograph Daytona 'Panda / Reverse Panda'",
            "reference": "116500LN",
            "production_years": "2016 - 2023",
            "calibre": "Rolex Calibre 4130 (Vertical Clutch Column Wheel)",
            "retail_msrp": 14550,
            "fair_market_avg": 29800,
            "market_range": [27500, 33500],
            "common_issues": [
                {"issue": "Chronograph Minute Counter Jitter", "cost": 1850, "detail": "Friction spring tension loss on the minute-recorder runner causing minute subdial hand to skip or lag."},
                {"issue": "Screw-Down Pusher Gasket Degradation", "cost": 750, "detail": "Internal pusher O-rings hardening over 6+ years allowing moisture ingress during chronograph actuation."},
                {"issue": "Cerachrom Tachymetre Bezel Chipping", "cost": 3200, "detail": "Hard impact at 12 or 6 o'clock causing micro-fissures in monobloc ceramic."}
            ],
            "counterfeit_risk_zones": [
                "Subdial thickness: Genuine dials feature razor-sharp snail-pattern concentric rings inside subdials.",
                "Thickness audit: Genuine 116500LN measures exactly 12.2mm thick. Most 'Superclones' (Clean/BTF) measure 12.5mm+.",
                "Pusher feel: Column-wheel tactile snap is solid and mechanical; fake 7750 movements feel spongy or gritty."
            ],
            "negotiation_deductions": {
                "missing_warranty_card": 4500,
                "missing_original_box": 900,
                "overpolished_case": 3000,
                "missing_links": 600
            }
        },
        "rolex_gmt_126710blro": {
            "name": "Rolex GMT-Master II 'Pepsi' Jubilee/Oyster",
            "reference": "126710BLRO",
            "production_years": "2018 - Present",
            "calibre": "Rolex Calibre 3285 (Independent Jumping Local Hour Hand)",
            "retail_msrp": 10900,
            "fair_market_avg": 19500,
            "market_range": [18200, 22000],
            "common_issues": [
                {"issue": "MK1 vs MK2/MK3 Bezel Color Variation Controversy", "cost": 2200, "detail": "MK1 pastel red/blue transitions command premiums; swapped replacement modern dark bezels devalue early 2018 models."},
                {"issue": "Hour Jumper Cam Wheel Wear", "cost": 1200, "detail": "Rapid independent hour changing without following crown engagement rules causing spring fatigue."}
            ],
            "counterfeit_risk_zones": [
                "Ceramic color seam: The red/blue transition at 6 and 18 hours must be perfectly split mid-digit with zero color bleed under 20x magnification.",
                "Hand stack order: Hour hand, 24-Hour GMT hand (red), Minute hand, Seconds hand."
            ],
            "negotiation_deductions": {
                "missing_warranty_card": 3200,
                "missing_box": 650,
                "stretched_jubilee": 1600
            }
        },
        "patek_nautilus_5711": {
            "name": "Patek Philippe Nautilus Stainless Steel Blue Dial",
            "reference": "5711/1A-010",
            "production_years": "2006 - 2021",
            "calibre": "Patek Calibre 324 S C (Gyromax Balance, 21k Gold Rotor)",
            "retail_msrp": 34890,
            "fair_market_avg": 98500,
            "market_range": [89000, 115000],
            "common_issues": [
                {"issue": "Satin-Brushed Bezel Edge Softening", "cost": 6500, "detail": "The octagonal bezel with polished side flanks loses sharp geometric facet corners when polished by non-Geneva workshops."},
                {"issue": "Date Disc Font Revision Divergence", "cost": 4200, "detail": "Early 315 SC movements vs late 324 SC movements feature different font kerning. Swapped date wheels signify flood or damage repair."},
                {"issue": "Calibre 324 Reversing Wheel Slippage", "cost": 2800, "detail": "Teflon-coated click wheels in automatic winding train requiring complete movement overhaul."}
            ],
            "counterfeit_risk_zones": [
                "Case thickness: Must be exactly 8.3mm ultra-thin. High-end fakes exceed 9.0mm.",
                "Geneva Seal vs Patek Philippe Seal: 2006-2009 features Geneva Seal (crowned eagle & key); post-2009 features double 'PP' Hallmark.",
                "Certificate of Origin: Watermarked textured paper with matching Geneva movement serial number."
            ],
            "negotiation_deductions": {
                "missing_certificate_of_origin": 18000,
                "missing_cork_or_wooden_box": 2500,
                "overpolished_bezel": 8500,
                "bracelet_stretch": 4000
            }
        },
        "ap_royal_oak_15500st": {
            "name": "Audemars Piguet Royal Oak Selfwinding 41mm",
            "reference": "15500ST.OO.1220ST.01 (Blue Dial)",
            "production_years": "2019 - Present",
            "calibre": "Audemars Piguet Calibre 4302 (70-hour Reserve, 28,800 vph)",
            "retail_msrp": 27800,
            "fair_market_avg": 42500,
            "market_range": [39000, 48000],
            "common_issues": [
                {"issue": "White Gold Bezel Screw Misalignment", "cost": 2400, "detail": "Hexagonal white gold bolts recessed into the octagonal bezel must align tangent to the bezel perimeter."},
                {"issue": "Grande Tapisserie Guilloché Dial Flaking", "cost": 3800, "detail": "Authentic dial cut with pantograph machine; printed/stamped fake dials lack micro-pyramid light refraction."}
            ],
            "counterfeit_risk_zones": [
                "Tapisserie square pattern spacing and pyramid facet angle.",
                "Bracelet link taper: Each link decreases in size down to the AP deployant clasp by exact millimetric steps."
            ],
            "negotiation_deductions": {
                "missing_warranty_card": 7500,
                "missing_box": 1200,
                "bezel_dents": 3200
            }
        },
        "omega_speedmaster_pro": {
            "name": "Omega Speedmaster Professional 'Moonwatch' Sapphire",
            "reference": "310.30.42.50.01.002",
            "production_years": "2021 - Present",
            "calibre": "Omega Co-Axial Master Chronometer Calibre 3861",
            "retail_msrp": 8300,
            "fair_market_avg": 6900,
            "market_range": [6400, 7600],
            "common_issues": [
                {"issue": "DON (Dot Over Ninety) Bezel Swaps", "cost": 1200, "detail": "Earlier replacement bezels feature Dot Next to Ninety; collectors demand original DON specs."},
                {"issue": "Hesalite vs Sapphire Mismatch on Resale", "cost": 950, "detail": "Dealers mislabeling base Hesalite references as Sapphire Sandwich variants."}
            ],
            "counterfeit_risk_zones": [
                "Co-Axial escapement ticking frequency (21,600 vph with distinctive tri-level escapement sound).",
                "METAS magnetic resistance certification card with laser QR code."
            ],
            "negotiation_deductions": {
                "missing_cards_pictogram": 1100,
                "missing_suit_box": 450,
                "bracelet_wear": 500
            }
        }
    }
}

os.makedirs(r'C:\chronospec-ai\data', exist_ok=True)
with open(r'C:\chronospec-ai\data\watch_specs.json', 'w', encoding='utf-8') as f:
    json.dump(watch_db, f, indent=2)

print("Created watch_specs.json successfully!")
