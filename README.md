# Brandcraft

Curated resources for leveling up brand designers: inspiration, brand guidelines and studios, visual tools, utilities and people to follow.

Static site, no build step. Open `index.html` via any static server:

```bash
python3 -m http.server 4960
```

## Structure

- `index.html` – layout, styles, hash router (`#/category/section`), theme toggle (auto / light / dark)
- `data.js` – generated catalogue, do not edit by hand
- `scripts/build-data.py` – builds `data.js`; the Brand Guidelines list and AI Guide structure live here
- `i18n/uk-part*.json` – Ukrainian section titles and link descriptions (UI language is Ukrainian, left-nav categories stay English)
- `source/product-sites.json` + `i18n/ps/out-*.json` – Product Sites (liveness-checked, deduped by domain); `i18n/ps/fixes.json` – manual drops (hijacked/spam domains, shut-down products), dead links in `source/product-sites-dead.txt`
- `source/ai-guidelines.xlsx` → `source/ai-guide.json` – AI Guide content
- `source/` – base catalogue (sections Inspiration, Visuals, Utilities, Design Engineers)
- `content/brand-identity-studios.md` – review notes on the studio links

To add or edit links: change `scripts/build-data.py` (Brand Guidelines) or `source/full.txt`, then run `python3 scripts/build-data.py`.
