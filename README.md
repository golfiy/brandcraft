# Brandcraft

Curated resources for leveling up brand designers: inspiration, brand guidelines and studios, visual tools, utilities and people to follow.

Static site, no build step. Open `index.html` via any static server:

```bash
python3 -m http.server 4960
```

## Structure

- `index.html` – layout, styles, hash router (`#/category/section`), theme toggle (auto / light / dark)
- `data.js` – generated catalogue, do not edit by hand
- `scripts/build-data.py` – builds `data.js`; the Brand Guidelines list lives here
- `source/` – base catalogue (sections Inspiration, Visuals, Utilities, Design Engineers)
- `content/brand-identity-studios.md` – review notes on the studio links

To add or edit links: change `scripts/build-data.py` (Brand Guidelines) or `source/full.txt`, then run `python3 scripts/build-data.py`.
