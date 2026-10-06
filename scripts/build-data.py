#!/usr/bin/env python3
"""Builds data.js from source/full.txt (catalogue), source/designers.json and the Brand Guidelines list below.

Run: python3 scripts/build-data.py
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source"

# Sections dropped on purpose: Components, Build (whole categories) + anything Behance.
DROP_SECTIONS = {"Component Libraries", "Motion", "Development", "Agents & MCP", "Deploy"}
DROP_URL = re.compile(r"behance\.net", re.I)


def parse_catalogue():
    sections, cur = {}, None
    for line in (SRC / "full.txt").read_text().splitlines():
        if line.startswith("## "):
            cur = {"title": line[3:].strip(), "desc": "", "items": []}
            sections[cur["title"]] = cur
        elif cur and line.startswith("- ["):
            m = re.match(r"- \[(.+?)\]\((.+?)\): (.+)", line)
            if m and not DROP_URL.search(m.group(2)):
                cur["items"].append({"name": m.group(1), "url": m.group(2), "desc": m.group(3)})
        elif cur and line.strip() and not cur["desc"] and not line.startswith(">"):
            cur["desc"] = line.strip()
    return sections


def case(label, url):
    return {"label": label, "url": url}


BRAND = [
    {
        "title": "Global Agencies",
        "desc": "Network agencies and consultancies that set the bar for identity systems.",
        "items": [
            {"name": "Pentagram", "url": "https://www.pentagram.com/", "desc": "Partner-led studio behind some of the most cited identities.",
             "cases": [case("Oxide", "https://www.pentagram.com/work/oxide"), case("Cazana", "https://www.pentagram.com/work/cazana"),
                       case("Secondmind", "https://www.pentagram.com/work/secondmind"), case("Lightmatter", "https://www.pentagram.com/work/lightmatter"),
                       case("Lightmatter Hardware", "https://www.pentagram.com/work/lightmatter-hardware"), case("Realspace", "https://www.pentagram.com/work/realspace"),
                       case("NAMHG", "https://www.pentagram.com/work/national-ambulance-mental-health-group")]},
            {"name": "MetaDesign", "url": "https://metadesign.com/", "desc": "Berlin-born consultancy for large corporate brand systems.",
             "cases": [case("AmerisourceBergen", "https://metadesign.com/en/work/amerisourcebergen"), case("TK Elevator", "https://metadesign.com/en/work/tkelevator")]},
            {"name": "Wolff Olins", "url": "https://wolffolins.com/work/", "desc": "London brand consultancy known for bold, strategy-led rebrands.",
             "cases": [case("AES", "https://wolffolins.com/case-study/aes/"), case("McKinsey & Company", "https://wolffolins.com/case-study/mckinsey-company/")]},
            {"name": "Collins", "url": "https://www.wearecollins.com/", "desc": "Brand experience studio building identities as living systems.",
             "cases": [case("Twitch", "https://www.wearecollins.com/work/twitch/"), case("The One Club", "https://www.wearecollins.com/work/one-club/"),
                       case("bp", "https://www.wearecollins.com/work/bp/"), case("Bose Frames", "https://www.wearecollins.com/work/bose-frames/")]},
            {"name": "Interbrand", "url": "https://interbrand.com/", "desc": "Global brand consultancy behind large-scale rebrands.",
             "cases": [case("CSA", "https://interbrand.com/work/connectivity-standards-alliance-csa/"), case("Kia", "https://interbrand.com/work/kia-movement-that-inspires/")]},
            {"name": "FutureBrand", "url": "https://www.futurebrand.com/", "desc": "Global brand transformation consultancy.",
             "cases": [case("Octave", "https://www.futurebrand.com/our-work/octave")]},
            {"name": "JKR", "url": "https://www.jkrglobal.com/work", "desc": "Independent creative agency known for consumer brand identities."},
            {"name": "Studio Dumbar", "url": "https://studiodumbar.com/", "desc": "Rotterdam studio famous for systemic, motion-first identities.",
             "cases": [case("MSI", "https://studiodumbar.com/work/msi-24")]},
            {"name": "R/GA", "url": "https://rga.com/", "desc": "Agency at the intersection of brand, product and technology."},
            {"name": "Huge", "url": "https://www.hugeinc.com/", "desc": "Digital-first agency for brand and experience design."},
            {"name": "Instrument", "url": "https://www.instrument.com/", "desc": "Digital agency crafting brand and product experiences."},
            {"name": "ustwo", "url": "https://ustwo.com/", "desc": "Digital product studio with strong brand craft."},
            {"name": "Fantasy", "url": "https://fantasy.co/", "desc": "Digital product design agency for iconic brands."},
            {"name": "AREA 17", "url": "https://area17.com/work", "desc": "Brand and digital agency for culture and institutions."},
            {"name": "Base Design", "url": "https://www.basedesign.com/work", "desc": "Brand studio with clean, typographic identity systems."},
            {"name": "Kurppa Hosk", "url": "https://kurppahosk.com/", "desc": "Stockholm brand agency for strategy and design."},
            {"name": "BVD", "url": "https://bvd.se/about/", "desc": "Stockholm agency built around simplifying brands."},
            {"name": "Stockholm Design Lab", "url": "https://www.stockholmdesignlab.se/work", "desc": "Swedish studio known for reductive, timeless identities."},
            {"name": "Spin", "url": "https://spin.co.uk/", "desc": "London studio with rigorous, typographic identity work.",
             "cases": [case("ALRA", "https://spin.co.uk/work/alra"), case("Megamac", "https://spin.co.uk/work/megamac"), case("Kintek", "https://spin.co.uk/work/kintek"),
                       case("UCA", "https://spin.co.uk/work/university-for-the-creative-arts"), case("Ministry of Sound", "https://spin.co.uk/work/ministry-of-sound"),
                       case("Wim Crouwel", "https://spin.co.uk/work/wim-crouwel-exhibition")]},
            {"name": "Knowit", "url": "https://www.knowit.eu/cases/", "desc": "Nordic consultancy with a brand and experience practice."},
        ],
    },
    {
        "title": "Independent Studios",
        "desc": "Smaller studios with sharp, distinctive identity work.",
        "items": [
            {"name": "Gretel", "url": "https://gretelny.com/work", "desc": "New York studio for brand identity and motion."},
            {"name": "The Branx", "url": "https://thebranx.com/", "desc": "Brand and digital design agency."},
            {"name": "Together", "url": "https://together.agency/work/", "desc": "Brand, web and product studio for B2B tech."},
            {"name": "Wild Wild Web", "url": "https://wildwildweb.es/es/portfolio", "desc": "Spanish studio for brand and web design."},
            {"name": "Flowstate", "url": "https://flowstatebranding.com/work/", "desc": "Branding studio for identity and strategy."},
            {"name": "Matchstic", "url": "https://matchstic.com/work", "desc": "Atlanta brand identity firm."},
            {"name": "Dwarf", "url": "https://dwarf.dk/", "desc": "Copenhagen digital and brand agency."},
            {"name": "Grávita", "url": "https://somosgravita.com/", "desc": "Strategic branding agency: strategy, identity, activation."},
            {"name": "Orizon", "url": "https://dribbble.com/Orizon", "desc": "Canadian UI/UX agency with strong visual craft."},
            {"name": "Joseph Mark", "url": "https://josephmark.studio/work", "desc": "Venture design studio for brand and product."},
            {"name": "Ascend Studio", "url": "https://www.ascendstudio.co.uk/work/", "desc": "UK branding agency across tech, real estate and culture."},
            {"name": "Humaan", "url": "https://www.humaan.com/work/commercial/", "desc": "Australian studio for websites, apps and brands."},
            {"name": "Koto", "url": "https://koto.studio/work/", "desc": "Global brand studio known for playful, ownable systems."},
            {"name": "Mubien", "url": "https://mubien.com/portfolio/", "desc": "Studio across branding, motion and digital products."},
            {"name": "Moment", "url": "https://www.thisismoment.com/", "desc": "Brand and visual design studio for design-led companies."},
            {"name": "Emdash", "url": "https://emdashoslo.no/work", "desc": "Oslo design studio for identity and editorial work."},
            {"name": "Vrints-Kolsteren", "url": "https://www.vrints-kolsteren.com/", "desc": "Belgian studio for identity and graphic design."},
            {"name": "Play", "url": "https://www.play.studio/", "desc": "San Francisco studio for brands, campaigns and products."},
            {"name": "Half Decent", "url": "https://halfdecent.studio/", "desc": "Design studio with a visual journal on craft."},
            {"name": "Bedow", "url": "https://www.bedow.se/work/", "desc": "Stockholm studio known for crisp, minimal identities."},
            {"name": "Studio Mast", "url": "https://www.studiomast.co/", "desc": "Denver graphic design and branding studio."},
            {"name": "BerrielBrands", "url": "https://berrielbrands.com/", "desc": "Branding and visual identity studio."},
            {"name": "Traina", "url": "https://wearetraina.com/work/", "desc": "San Francisco brand studio for tech and startups.",
             "cases": [case("Deepcell", "https://wearetraina.com/work/deepcell/")]},
            {"name": "dimadima", "url": "https://dimadima.partners/", "desc": "Independent branding studio."},
            {"name": "Good Habit", "url": "https://goodhabit.studio/", "desc": "Brand and design studio for early-stage tech."},
            {"name": "Tekni", "url": "https://studiotekni.com/", "desc": "Creative bureau between physical and virtual worlds."},
            {"name": "Hymn", "url": "https://www.hymn.design/", "desc": "Lausanne branding and design agency."},
            {"name": "Daydream", "url": "https://daydreamstudio.uk/", "desc": "UK design studio for brand and digital."},
            {"name": "Athletics", "url": "https://athleticsnyc.com/", "desc": "New York studio for identity, motion and digital."},
            {"name": "Fol", "url": "https://fol.com.tr/", "desc": "Istanbul studio for identity, UI and packaging."},
            {"name": "Bold Scandinavia", "url": "https://boldscandinavia.com/", "desc": "Scandinavian brand agency for bold identities."},
            {"name": "Vagrant", "url": "https://vagrant.studio/", "desc": "Design and communication consultancy, research-led."},
            {"name": "Monroe", "url": "https://monroe.works/", "desc": "Independent design studio."},
            {"name": "ODA Branding", "url": "https://odabranding.com/", "desc": "Independent UK branding agency."},
            {"name": "ED.", "url": "https://ed.studio/", "desc": "Brand and design studio.",
             "cases": [case("Enko", "https://ed.studio/work/enko/")]},
            {"name": "LORD", "url": "https://www.callmelord.com/", "desc": "Branding agency: be bold, be a brand."},
            {"name": "Onda Studio", "url": "https://www.ondastudio.co/", "desc": "Design studio for brands that lead."},
            {"name": "Afternow", "url": "https://bb.agency/", "desc": "Brand identity and communication studio.",
             "cases": [case("Pilot44", "https://bb.agency/project/pilot44/"), case("Crisp", "https://bb.agency/project/crisp/")]},
            {"name": "Anagram Club", "url": "https://anagram.club/", "desc": "Studio for bold branding and product design."},
            {"name": "Nord ID", "url": "https://nordid.se/", "desc": "Swedish agency for 360 brand experiences."},
            {"name": "Kallan&Co", "url": "https://www.kallan.co/work", "desc": "Design and innovation studio blending craft and AI."},
            {"name": "Ragged Edge", "url": "https://raggededge.com/work/", "desc": "London brand agency for rebrands and campaigns.",
             "cases": [case("Wise", "https://raggededge.com/partnerships/wise")]},
            {"name": "SKINN", "url": "https://www.skinn.agency/", "desc": "Belgian branding agency, Antwerp and Bruges."},
            {"name": "Clou", "url": "https://www.clou.ch/", "desc": "Lucerne advertising and brand agency."},
            {"name": "Ashfall", "url": "https://ashfall.studio/work", "desc": "Creative and technology studio for brands."},
            {"name": "ONBOX", "url": "https://onboxcreative.com/", "desc": "Vancouver studio for brand, web and product."},
            {"name": "Rhythm", "url": "https://rhythm.design/", "desc": "Independent design studio."},
            {"name": "Jamie Quantrill", "url": "https://www.jamiequantrill.co.uk/", "desc": "Bristol designer across branding, motion and digital."},
        ],
    },
    {
        "title": "Specialists",
        "desc": "Craft beyond the logo: sound, image-making and art direction.",
        "items": [
            {"name": "Press Play On Tape", "url": "https://pressplayontape.studio/", "desc": "Paris sound studio for audio branding."},
            {"name": "Services Généraux", "url": "https://generaux.services/", "desc": "Image-making studio for photography and direction."},
        ],
    },
    {
        "title": "Guidelines & Libraries",
        "desc": "Real brand guidelines to study how systems are documented.",
        "items": [
            {"name": "Brandbase", "url": "https://www.brandbase.xyz/", "desc": "Growing collection of real brand guidelines."},
            {"name": "Semrush Brand", "url": "https://brand.semrush.com/", "desc": "Live brand guidelines site worth dissecting."},
            {"name": "Circular", "url": "https://www.madebycircular.com.au/", "desc": "Brand guideline templates for designers."},
        ],
    },
    {
        "title": "Publications",
        "desc": "Where new identities get published and discussed.",
        "items": [
            {"name": "The Brand Identity", "url": "https://the-brandidentity.com/", "desc": "Publication covering new identity work.",
             "cases": [case("StreetBeat by Clay", "https://the-brandidentity.com/project/clays-identity-for-investment-platform-streetbeat-reflects-its-expertise-and-swift-footed-spirit")]},
            {"name": "Rebrand Gallery", "url": "https://www.rebrand.gallery/", "desc": "Before and after archive of rebrands.",
             "cases": [case("Semrush 2026", "https://www.rebrand.gallery/rebrand/semrush-2026")]},
        ],
    },
    {
        "title": "Awards",
        "desc": "Award archives to benchmark identity work.",
        "items": [
            {"name": "Ukrainian Design Awards", "url": "https://design-awards.com.ua/winners/", "desc": "Winners archive of Ukrainian design awards."},
            {"name": "Best Awards", "url": "https://bestawards.co.nz/", "desc": "New Zealand design awards archive."},
        ],
    },
]


def main():
    cat = parse_catalogue()
    pick = lambda *names: [cat[n] for n in names]
    designers = json.loads((SRC / "designers.json").read_text())
    categories = [
        {"id": "inspiration", "title": "Inspiration", "icon": "spark",
         "sections": pick("Design Galleries", "Interface Design", "Reading")},
        {"id": "brand-guidelines", "title": "Brand Guidelines", "icon": "brand", "sections": BRAND},
        {"id": "visuals", "title": "Visuals", "icon": "palette",
         "sections": pick("Type", "Color", "3D", "Shaders", "Icons")},
        {"id": "utilities", "title": "Utilities", "icon": "tool",
         "sections": pick("Utilities", "Desktop", "Video & Capture", "Whiteboard")},
        {"id": "designers", "title": "Design Engineers", "icon": "people",
         "sections": [{"title": "Design engineers to follow",
                       "desc": "Curated design engineers and creative developers to follow.",
                       "items": [{"name": n, "url": u, "desc": d} for n, u, d in designers]}]},
    ]
    for c in categories:
        for s in c["sections"]:
            s["id"] = re.sub(r"[^a-z0-9]+", "-", s["title"].lower()).strip("-")
            assert all(not DROP_URL.search(i["url"]) for i in s["items"])
    out = "window.CATALOGUE = " + json.dumps(categories, ensure_ascii=False, indent=1) + ";\n"
    (ROOT / "data.js").write_text(out)
    for c in categories:
        print(c["title"], sum(len(s["items"]) for s in c["sections"]), [len(s["items"]) for s in c["sections"]])


if __name__ == "__main__":
    main()
