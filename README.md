# Seyaa Jewels Inc. — Trade Catalogue 2026

Handoff brief. Two deliverables built from one dataset: an A4 PDF and a single-file website.

## Client / branding

- Entity: **Seyaa Jewels Inc.**
- Audience: **B2B trade buyers**. Prices shown as "on request" — no price column anywhere.
- Address: 42 West 48th Street, Suite #600, New York, NY 10036, United States
- Contact: Rahul Shah · +1 917 801 6060 · seyaajewels@gmail.com · no website
- WhatsApp QR → `https://wa.me/19178016060?text=...` (pre-filled quote message)
- Colours: ink `#1C1C1C`, paper `#FFFFFF`, accent `#DD611C`
- Fonts: **Allura** (display/script), **Montserrat** (body). `fonts/` holds static TTFs;
  Montserrat weights were instanced from the variable font with fontTools.
- Logo: horse-and-diamond mark + "Seyaa Jewels" lettering, extracted from the client's
  orange-on-white PNG and recoloured white with transparency. See `assets/`.

## Scope — 7 collections, 46 variants

| Collection | Variants (TCW) | Size |
|---|---|---|
| Round Tennis Bracelet | 2, 3, 4, 5, 6, 7, 8, 10, 15 ct | 7 in |
| All Mix Fancy Bracelet | 3, 5, 7, 10, 15 ct | 7 in |
| Straight Line Tennis Necklace | 5, 7, 10, 15, 20 ct | 16.5 in |
| Graduated Tennis Necklace | 7, 10, 15, 20 ct | 16.5 in |
| Round Studs — Basket Setting | 1, 1.5, 2, 3, 4, 5, 8, 10 ct | — |
| Round Studs — Martini Setting | 1, 1.5, 2, 3, 4, 5, 8, 10 ct | — |
| Eternity Bands (Round only) | 2, 3, 4, 5, 8, 12, 14 ct | US 7 |

Decisions taken: both stud settings as separate sections; Round eternity bands only
(Emerald and Emerald Graduated excluded); White and Yellow shown side by side; no
"other sizes available" footnote.

Fixed across every item: 14K gold (yellow/white), lab grown, E-F colour, VS-SI clarity,
IGI certified.

## Data

Source: `Master_Portal_File__7_.xlsx`, sheets Bracelets / Necklaces / Studs / Eternity Bands.
Fields used: Title, description (metal colour), SKU, Total Diamonds weight, Total number of
diamonds, Diamonds shape, Metal weight, Metal length, IMAGE 1–4. Ignored: price, origin,
other sheets.

Rows are per metal colour; the scripts group by Title into one variant carrying `skuW`/`skuY`
and `imgW`/`imgY` (Drive file IDs parsed out of the share URLs).

- `catalogue_data.json` — PDF dataset (Image 1 only)
- `site_data.json` — website dataset (Images 1–4, 266 IDs total)

## Website

A Next.js static site with the same design system as `devalshah713/seyaa-corporate`
(brand kit palette `#FFFFFF` / `#DD611C` / `#1C2120`, Montserrat + Allura, the horse mark,
white theme so the packshots dissolve into their tiles), filled with this catalogue's data.

```
site_data.json ──► scripts/build-catalogue.mjs ──► data/products.json + public/_redirects ──► next build ──► out/
```

```bash
npm ci
npm run dev      # local preview
npm run build    # → out/  (static export, every page prerendered)
```

- **Pages:** `/` home · `/collection` (category → shelf → shape filters, search by name or SKU)
  · `/piece/<slug>` (gallery, White/Yellow toggle, full spec) · `/company` · `/guide` · `/enquiry`.
- **Categories:** Bracelets (Round Tennis, All Mix Fancy) · Necklaces (Straight Line Tennis,
  Graduated Tennis) · Stud Earrings (Basket, Martini) · Rings (Eternity Bands). Mapped in
  `SHELVES` in `scripts/build-catalogue.mjs`.
- **Permanent links:** `/piece/<design id>` and `/piece/<SKU>` (e.g. `/piece/br-sl-02-w`)
  307-redirect to the current slug via the generated `public/_redirects`.
- **Prices:** none published — every piece reads "Price on request".
- **Clarity:** shown as the data states it, **VS–SI**. (The corporate site overrides its sheet
  to VVS–VS; that override is deliberately *not* carried over.)
- **Contact:** `src/lib/contact.ts` — Rahul Shah, +1 917 801 6060, seyaajewels@gmail.com,
  overridable with `NEXT_PUBLIC_WHATSAPP_NUMBER` / `NEXT_PUBLIC_SALES_EMAIL`.
- **Fonts:** self-hosted from `fonts/`, subset to Latin WOFF2 in `src/fonts/` — the build
  needs no network access.
- The build prints source-data problems (e.g. `16RG` titled 4 ct but weighing 5.3 ct; SKU
  `123 RGW` contains a space). They are reported, not corrected.

## PDF

```bash
pip install reportlab pillow
python3 build.py   # → Seyaa_Jewels_Trade_Catalogue_2026.pdf  (56 pages A4)
```

## Deploy (Cloudflare Pages)

Settings → Builds & deployments:

| Setting | Value |
|---|---|
| Framework preset | Next.js (Static HTML Export) |
| Build command | `npm run build` |
| Build output directory | `out` |
| Environment variable | `NODE_VERSION` = `22` (optional — `.nvmrc` already says 22) |

Live at https://seyaa-catalogue.pages.dev (override the canonical origin with
`NEXT_PUBLIC_SITE_URL` if a custom domain is added).

### PDF structure
Cover → About → then per collection: a section opener (blurb + full spec table) followed by
one page per variant (White and Yellow plates side by side + six-cell spec strip) → Contact
page with QR. Image frames fall back to a labelled placeholder when a file is missing.

## The image problem (read this first)

Renders live in Google Drive, ~1.3 MB PNG each, 92 files for Image 1 alone.

- The chat sandbox's network allowlist blocks `drive.google.com`, so the PDF build cannot
  fetch them. Adding custom domains to that allowlist is a Team/Enterprise admin setting.
- The Drive MCP connector returns files as base64 into the conversation, which does not
  scale past a couple of images.
- **The website sidesteps this**: it renders `https://drive.google.com/thumbnail?id=<ID>&sz=w<N>`
  and the viewer's browser fetches directly. Nothing passes through the build.

Consequences:
- The PDF currently ships with placeholder frames. To fill them, drop files named
  `<SKU>.jpg` into the `renders/` directory the script points at.
- The website needs the Drive files set to **"Anyone with the link"**, or buyers see the
  fallback. Test in a private window.
- `BR-SL-02-W`'s Image 1 ID no longer resolves — likely deleted. Fix the link in the sheet.
- Drive naming is inconsistent (`BR-SL-08-W-A.png` vs `2NKW A` vs `124RGW A.png`). Irrelevant
  while using the sheet's links, but worth normalising.

## Open items

- Confirm which angle suffix (`-A` … `-E`) is the hero shot — never answered.
- Product photos load from Google Drive: the files must be shared "Anyone with the link".
- Optional: generate the PDF from the website data so both stay in sync from one source.
