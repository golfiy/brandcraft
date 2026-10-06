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


SOURCE_LABELS = {
    "https://support.claude.com/en/articles/16761823-claude-cowork-and-chat-are-one-claude": "Claude: Cowork і чат",
    "https://code.claude.com/docs/en/overview": "Claude Code: огляд",
    "https://learn.chatgpt.com/docs/models": "ChatGPT: моделі",
    "https://platform.claude.com/docs/en/models/overview": "Claude: моделі",
    "https://developers.openai.com/api/docs/models": "OpenAI API: моделі",
    "https://developers.openai.com/api/docs/models/gpt-image-2.5-flare": "GPT Image 2.5 Flare",
    "https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst": "GPT Image 2.5 Sunburst",
    "https://learn.chatgpt.com/docs/build-skills": "Codex: Build skills",
    "https://code.claude.com/docs/en/skills": "Claude Code: skills",
    "https://support.claude.com/en/articles/12512198-how-to-create-custom-skills": "Claude: власні skills",
    "https://learn.chatgpt.com/docs/agent-configuration/subagents": "Codex: субагенти",
    "https://academy.claude.com/courses/introduction-to-claude-cowork": "Claude Academy: Introduction to Claude Cowork",
}
SOURCE_DESC = {
    "Claude: Cowork і чат": "Чат і Cowork в одному інтерфейсі Claude.",
    "Claude Code: огляд": "Що вміє агент для роботи з кодом і файлами.",
    "ChatGPT: моделі": "Моделі, доступні в ChatGPT і Codex.",
    "Claude: моделі": "Огляд актуальних моделей Claude.",
    "OpenAI API: моделі": "Каталог моделей OpenAI API.",
    "GPT Image 2.5 Flare": "Модель зображень для швидких варіантів.",
    "GPT Image 2.5 Sunburst": "Модель зображень для точного редагування.",
    "Codex: Build skills": "Як створити й зберегти skill у Codex.",
    "Claude Code: skills": "Skills у Claude Code: структура й встановлення.",
    "Claude: власні skills": "Як додати власний skill у Claude.",
    "Codex: субагенти": "Налаштування субагентів для перевірки.",
    "Claude Academy: Introduction to Claude Cowork": "Курс із роботи з файлами в Claude Cowork.",
}
SRC_SPLIT = re.compile(r"\s*(?:Джерело|Джерела|Моделі|Субагенти Codex):\s*(.+)$")


def split_sources(text):
    """Moves trailing 'Джерело: url ; url' into a list of labelled links."""
    m = SRC_SPLIT.search(text)
    if not m:
        return text, []
    urls = [u.strip(" .") for u in m.group(1).split(";")]
    return text[:m.start()].rstrip(), [{"label": SOURCE_LABELS[u], "url": u} for u in urls]


# Model lineup re-checked against platform.claude.com, developers.openai.com and learn.chatgpt.com.
MODELS_CHECKED = "06.10.2026"


def build_ai_guide():
    g = json.loads((SRC / "ai-guide.json").read_text())

    def rows(block):
        out = []
        for r in block["rows"]:
            text, src = split_sources(r["v"].replace("GPT-5.6 Sol або Claude Sonnet 5.", "GPT-6.1 Sol або Claude Sonnet 5.5."))
            out.append({"k": r["k"], "v": text, "sources": src})
        return out

    models_intro = (g["models"]["rows"][0]["v"] +
                    " GPT-5.5 вимикається в ChatGPT і Codex 14.10.2026; GPT-5.6 Sol, Terra й Luna лишаються доступними на час переходу.")
    models = [
        {"task": "Типовий пост, документ, презентація за шаблоном",
         "codex": ["GPT-6.1 Sol", "глибина міркування за замовчуванням"],
         "claude": ["Sonnet 5.5", "якщо є в акаунті"],
         "note": "Почати з одного матеріалу; продовжувати серію тільки після перевірки. Неповний бриф, відсутній шрифт або недоступний файл спочатку виправити."},
        {"task": "Новий skill, складна структура, помилка генератора",
         "codex": ["GPT-6 Astra", "почати з Light, для складного планування підвищувати reasoning effort: більше часу й токенів"],
         "claude": ["Opus 5.5", "якщо не впорався після виправлення вхідних даних – Fable 5.1, якщо доступна"],
         "note": "Дати конкретний збій або критерії складної задачі."},
        {"task": "Багато простих повторів",
         "codex": ["GPT-6 Luna", "після перевірки процесу; почати з High"],
         "claude": ["Haiku 4.5", "після перевірки процесу"],
         "note": "Наприклад, назви файлів, розподіл текстів по готових полях. Порівняти з робочою моделлю на тому самому наборі; якщо помилки додають ручної роботи, лишити попередню модель."},
        {"task": "Картинки",
         "codex": ["GPT Image 2.5 Flare", "швидкі варіанти"],
         "codex2": ["GPT Image 2.5 Sunburst", "точне редагування"],
         "claude": None,
         "note": "Це моделі генерації зображень, не заміна моделі агента. У застосунку модель картинки може обиратися автоматично: тоді використовувати доступний інструмент і перевіряти результат."},
    ]
    model_sources = [split_sources(r["v"])[1] for r in g["models"]["rows"][1:]]
    for m, src in zip(models, model_sources):
        m["sources"] = src

    assess = rows(g["assess"])
    for r in assess:
        if r["k"] == "Курс і результат":
            r["v"] = "Після навчання встановити власний skill і зробити ним новий матеріал. Навчання зараховується через цю роботу, а не сертифікат."
            r["sources"] = [{"label": SOURCE_LABELS[u], "url": u} for u in (
                "https://academy.claude.com/courses/introduction-to-claude-cowork",
                "https://learn.chatgpt.com/docs/build-skills")]

    sources, seen = [], set()
    for u, label in SOURCE_LABELS.items():
        if u not in seen:
            seen.add(u)
            sources.append({"name": label, "url": u, "desc": SOURCE_DESC[label]})

    return {
        "title": g["title"], "intro": g["intro"], "levels": g["levels"],
        "levelNames": g["levelNames"], "checkName": g["checkName"], "skills": g["skills"],
        "env": rows(g["env"]),
        "modelsTitle": g["models"]["title"].replace("22.09.2026", MODELS_CHECKED), "modelsIntro": models_intro, "models": models,
        "save": rows(g["save"]), "workflow": rows(g["workflow"]), "assess": assess,
        "sources": sources,
        # Personal "pick your level" guide rewritten from the matrix (addressed as «ти»).
        "path": json.loads((SRC / "ai-skills-personal.json").read_text()) if (SRC / "ai-skills-personal.json").exists() else None,
    }


PRODUCT_SECTIONS = [
    ("ai", "AI", "AI-продукти", "Як AI-компанії пояснюють складні продукти через бренд і сайт."),
    ("fintech", "Fintech & Payments", "Фінтех і платежі", "Банки, картки й платежі: довіра, цифри та чиста подача."),
    ("crypto", "Crypto & Web3", "Крипто й Web3", "Крипто-бренди з сміливою графікою та нетиповою айдентикою."),
    ("saas", "SaaS & Productivity", "SaaS і продуктивність", "Робочі інструменти: як показати продукт і користь з першого екрана."),
    ("infra", "Data & Cloud", "Дані та хмара", "Технічні продукти, що звучать просто й виглядають преміально."),
    ("growth", "Marketing & Sales", "Маркетинг і продажі", "Продукти для росту, продажів і підтримки клієнтів."),
    ("health", "Health & Bio", "Здоров’я та біотех", "Медицина, велнес і біотех: тепла, але точна мова бренду."),
    ("climate", "Climate & Energy", "Клімат і енергетика", "Клімат, енергія й сталий розвиток у сучасній подачі."),
    ("hardware", "Hardware & Mobility", "Залізо та мобільність", "Пристрої, роботи, транспорт і deep tech."),
    ("consumer", "Consumer", "Консьюмер-бренди", "Їжа, мода, меблі, подорожі й застосунки для людей."),
    ("creative", "Creative Tools", "Креативні інструменти", "Інструменти для дизайну, відео й сайтів."),
    ("studios", "Studios & Portfolios", "Студії та портфоліо", "Сайти студій, агенцій і дизайнерів."),
    ("community", "Venture & Community", "Венчур і спільноти", "Фонди, події, освіта й некомерційні проєкти."),
]


def build_product_sites():
    """Product Sites: link list checked for liveness and deduped; labels from i18n/ps/out-*.json."""
    sites = json.loads((SRC / "product-sites.json").read_text())
    labels = {}
    for f in sorted((ROOT / "i18n" / "ps").glob("out-*.json")):
        labels.update(json.loads(f.read_text()))
    fixes = json.loads((ROOT / "i18n" / "ps" / "fixes.json").read_text())
    by = {k: [] for k, *_ in PRODUCT_SECTIONS}
    missing = 0
    for x in sites:
        if x["id"] in fixes["drop"]:
            continue
        lab = dict(labels.get(x["id"]) or {})
        if lab:
            x = {**x, "url": fixes["url"].get(x["id"], x["url"])}
            lab["name"] = fixes["name"].get(x["id"], lab["name"])
            lab["desc"] = fixes["desc"].get(x["id"], lab["desc"])
        if not lab:
            missing += 1
            continue
        by[lab["section"]].append({"name": lab["name"], "url": x["url"], "desc": lab["desc"].replace("—", "–")})
    if missing:
        print("PRODUCT SITES without labels:", missing)
    sections = []
    for key, en, uk, desc in PRODUCT_SECTIONS:
        items = sorted(by[key], key=lambda i: i["name"].lower())
        if items:
            sections.append({"title": en, "title_uk": uk, "desc": desc, "items": items})
    return sections


# Landings: galleries of landing pages / sites / sections. Moved out of Inspiration (by name) + new links
# from Viktor's list (liveness-checked 2026-10-06; dropped: upshift.supply, niceverynice.com – dead;
# prettyfolio.com – hijacked spam; godly.website – now redirects to Recent Design).
LANDINGS = [
    ("Landing Pages", "Лендинги", "Галереї лендингів за галузями, типами й стилями.",
     ["Land-book", "Lapa Ninja", "Landingfolio", "One Page Love", "SaaS Landing Page", "Saaspo", "SaaSFrame",
      "Best SaaS Web Designs", "Landing Love", "Landdding"], []),
    ("Website Galleries", "Галереї сайтів", "Кураторські добірки сайтів, щоб натренувати око.",
     ["SiteInspire", "Minimal Gallery", "Curated Design", "Best Website Gallery", "Recent Design", "A1",
      "inspora.design", "Hover States"],
     [("Httpster", "https://httpster.net/", "Галерея креативних і нагородних сайтів."),
      ("Umanmade", "https://www.umanmade.com/", "Каталог цифрових робіт, зроблених людьми для людей."),
      ("Scrolltide", "https://www.scrolltide.co/", "Кінематографічні сайти зі скрол-анімацією та AI-промпти до них.")]),
    ("Dark Mode", "Темна тема", "Сайти в темній темі: контраст, світло й акценти.",
     ["Dark Mode Design", "Sombra"],
     [("Dark Design", "https://www.dark.design/", "Добірка сайтів у темній темі, відібраних вручну.")]),
    ("Sections & Components", "Секції та блоки", "Hero, футери, навігація й CTA окремо від цілої сторінки.",
     ["SEESAW", "Supahero", "Sections.wtf", "footer.design", "navbar.design", "navbar.gallery", "cta.gallery"],
     [("Unsection", "https://www.unsection.com/", "Секції лендингів, SaaS, портфоліо й e-commerce."),
      ("Gridddy", "https://gridddy.framer.website/", "Галерея CTA-блоків перед футером.")]),
    ("Product UI", "UI продуктів", "Екрани реальних продуктів і рішення, що за ними стоять.",
     [],
     [("Refero", "https://refero.design/", "Десятки тисяч UI-референсів для вебу та iOS із розумним пошуком."),
      ("Nicelydone", "https://nicelydone.club/", "Понад 200 тисяч екранів SaaS: ціни, онбординг, налаштування."),
      ("abtest.design", "https://abtest.design/", "Результати A/B-тестів у найкращих застосунках."),
      ("Handheld", "https://www.handheld.design/", "Розсилка про мобільний дизайн: фреймворки, натхнення, інструменти.")]),
    ("Portfolios", "Портфоліо", "Сайти-портфоліо дизайнерів і студій.",
     ["Folios Gallery", "Wall of Portfolios"],
     [("Killer Portfolio", "https://www.killerportfolio.com/", "Добірка ефективних сайтів-портфоліо.")]),
    ("Visual Journals", "Візуальні щоденники", "Мудборди й журнали з брендингом і графікою.",
     [],
     [("Savee", "https://savee.com/", "Кураторський простір візуального натхнення без реклами."),
      ("Visual Journal", "https://visualjournal.it/", "Найкраще з брендингу, редакційного й графічного дизайну."),
      ("Aesse Studio", "https://aessestudio.tumblr.com/", "Tumblr-добірка візуальних референсів."),
      ("Klikkenthéke", "https://klikkentheke.com/catalogue/", "Каталог візуальних референсів.")]),
]
LANDING_CASES = {"One Page Love": [{"label": "OG Images", "url": "https://onepagelove.com/og"}]}


def build_landings(categories):
    """Pulls landing/site galleries out of Inspiration and builds the Landings category."""
    insp = next(c for c in categories if c["id"] == "inspiration")
    galleries = next(s for s in insp["sections"] if s["title_en"] == "Design Galleries")
    pool = {i["name"]: i for i in galleries["items"]}
    taken, sections = set(), []
    for en, uk, desc, moved, new in LANDINGS:
        items = []
        for name in moved:
            assert name in pool, name
            items.append(dict(pool[name]))
            taken.add(name)
        items += [{"name": n, "url": u, "desc": d} for n, u, d in new]
        for i in items:
            if i["name"] in LANDING_CASES:
                i["cases"] = LANDING_CASES[i["name"]]
        sections.append({"title": uk, "title_en": en, "desc": desc,
                         "id": re.sub(r"[^a-z0-9]+", "-", en.lower()).strip("-"), "items": items})
    galleries["items"] = [i for i in galleries["items"] if i["name"] not in taken]
    return {"id": "landings", "title": "Landings", "icon": "layout", "sections": sections}


def load_uk():
    uk = {"sections": {}, "items": {}}
    for f in sorted((ROOT / "i18n").glob("uk-part*.json")):
        d = json.loads(f.read_text())
        uk["sections"].update(d["sections"])
        uk["items"].update(d["items"])
    return uk


CODE_WORDS = re.compile(r"фронтенд|full-stack|розробни|інженер|\bкод|React|CSS|npm|JavaScript|терміна|CLI\b", re.I)


def apply_brand_pass(categories):
    """Brand-designer pass: drop dev-only tools, rewrite copy without code/frontend wording."""
    bp = json.loads((ROOT / "i18n" / "brand-pass.json").read_text())
    people_path = ROOT / "i18n" / "designers-brand.json"
    people = json.loads(people_path.read_text()) if people_path.exists() else {}
    dropped = []
    for c in categories:
        for s in c["sections"]:
            en = s["title_en"]
            drop = set(bp["drop"].get(en, []))
            if en == "Design engineers to follow":
                drop |= {n for n, v in people.items() if v.get("drop")}
                for i in s["items"]:
                    if i["name"] in people:
                        i["desc"] = people[i["name"]]["desc"]
            unknown = drop - {i["name"] for i in s["items"]}
            assert not unknown, (en, unknown)
            dropped += [f"{en} / {n}" for n in sorted(drop)]
            s["items"] = [i for i in s["items"] if i["name"] not in drop]
            s["desc"] = bp["sections"].get(en, s["desc"])
            s["title"] = bp["titles"].get(en, s["title"])
            for i in s["items"]:
                i["desc"] = bp["items"].get(en, {}).get(i["name"], i["desc"])
            if c["id"] != "brand-guidelines":
                left = [f"{en} / {i['name']}: {i['desc']}" for i in s["items"] if CODE_WORDS.search(i["desc"])]
                left += [f"{en} (section): {s['desc']}"] if CODE_WORDS.search(s["desc"]) else []
                if left:
                    print("CODE WORDING LEFT:", *left, sep="\n  ")
    print("Dropped:", len(dropped))


def main():
    cat = parse_catalogue()
    pick = lambda *names: [cat[n] for n in names]
    designers = json.loads((SRC / "designers.json").read_text())
    categories = [
        {"id": "inspiration", "title": "Inspiration", "icon": "spark",
         "sections": pick("Design Galleries", "Interface Design", "Reading")},
        {"id": "brand-guidelines", "title": "Brand Guidelines", "icon": "brand", "sections": BRAND},
        {"id": "product-sites", "title": "Product Sites", "icon": "browser", "sections": build_product_sites()},
        {"id": "visuals", "title": "Visuals", "icon": "palette",
         "sections": pick("Type", "Color", "3D", "Shaders", "Icons")},
        {"id": "utilities", "title": "Utilities", "icon": "tool",
         "sections": pick("Utilities", "Desktop", "Video & Capture", "Whiteboard")},
        {"id": "designers", "title": "Design Engineers", "icon": "people",
         "sections": [{"title": "Design engineers to follow",
                       "desc": "Curated design engineers and creative developers to follow.",
                       "items": [{"name": n, "url": u, "desc": d} for n, u, d in designers]}]},
        {"id": "ai-guide", "title": "AI Guide", "icon": "ai", "type": "guide", "sections": []},
    ]
    uk = load_uk()
    missing = []
    for c in categories:
        for s in c["sections"]:
            en_title = s["title"]
            s["title_en"] = en_title  # left nav stays English
            s["id"] = re.sub(r"[^a-z0-9]+", "-", en_title.lower()).strip("-")
            assert all(not DROP_URL.search(i["url"]) for i in s["items"])
            if "title_uk" in s:
                s["title"] = s.pop("title_uk")
                continue
            if en_title in uk["sections"]:
                s["title"] = uk["sections"][en_title]["title"]
                s["desc"] = uk["sections"][en_title]["desc"]
            else:
                missing.append(en_title)
            tr = uk["items"].get(en_title, {})
            for i in s["items"]:
                if i["name"] in tr:
                    i["desc"] = tr[i["name"]].replace("—", "–")
                else:
                    missing.append(f"{en_title} / {i['name']}")
    if missing:
        print("UNTRANSLATED:", len(missing), missing[:10])
    apply_brand_pass(categories)
    landings = build_landings(categories)
    categories.insert(next(i for i, c in enumerate(categories) if c["id"] == "product-sites"), landings)

    ai = build_ai_guide()
    out = ("window.CATALOGUE = " + json.dumps(categories, ensure_ascii=False, indent=1) + ";\n"
           "window.AI_GUIDE = " + json.dumps(ai, ensure_ascii=False, indent=1) + ";\n")
    assert "—" not in out, "em dash leaked into data"
    (ROOT / "data.js").write_text(out)
    for c in categories:
        print(c["title"], sum(len(s["items"]) for s in c["sections"]), [len(s["items"]) for s in c["sections"]])
    print("AI Guide skills:", len(ai["skills"]), "sources:", len(ai["sources"]))


if __name__ == "__main__":
    main()
