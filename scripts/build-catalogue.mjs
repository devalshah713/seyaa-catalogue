#!/usr/bin/env node
/**
 * site_data.json → data/products.json
 *
 * site_data.json is the trade-catalogue dataset (one entry per design, White and
 * Yellow SKUs side by side, Drive image IDs per metal). This reshapes it into
 * the catalogue structure the site reads: categories → shelves → designs →
 * per-metal variants with a gallery each.
 *
 * Problems in the source are reported, never silently corrected.
 */
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const SOURCE = path.join(ROOT, 'site_data.json')
const OUT = path.join(ROOT, 'data', 'products.json')
const REDIRECTS = path.join(ROOT, 'public', '_redirects')

/**
 * Every collection in the source, in the order the catalogue presents them,
 * mapped to the category and shelf it sits on.
 */
const SHELVES = {
  'Round Tennis Bracelet': ['Bracelets', 'Round Tennis', 'Bracelet'],
  'All Mix Fancy Bracelet': ['Bracelets', 'All Mix Fancy', 'Bracelet'],
  'Straight Line Tennis Necklace': ['Necklaces', 'Straight Line Tennis', 'Necklace'],
  'Graduated Tennis Necklace': ['Necklaces', 'Graduated Tennis', 'Necklace'],
  'Round Studs — Basket Setting': ['Stud Earrings', 'Basket Setting', 'Studs'],
  'Round Studs — Martini Setting': ['Stud Earrings', 'Martini Setting', 'Studs'],
  'Eternity Bands': ['Rings', 'Eternity Bands', 'Ring'],
}

const METAL = '14K Gold'
const ORIGIN = 'Lab Grown'

const slugify = (s) =>
  String(s)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')

const thumb = (id, w) => `https://drive.google.com/thumbnail?id=${id}&sz=w${w}`
const round = (n, dp = 3) => (typeof n === 'number' && isFinite(n) ? +n.toFixed(dp) : null)

/** "BR-SL-02-W" → "BR-SL-02", "18RGW" → "18RG", "123 RGW" → "123 RG". */
const designIdOf = (skuW) => String(skuW).trim().replace(/-?W$/i, '')

const problems = []
const report = (code, detail) => problems.push({ code, detail })

const source = JSON.parse(fs.readFileSync(SOURCE, 'utf8'))
const designs = []

for (const [collection, items] of Object.entries(source)) {
  const shelf = SHELVES[collection]
  if (!shelf) {
    report('UNKNOWN_COLLECTION', `"${collection}" has no shelf in SHELVES — skipped`)
    continue
  }
  const [category, subCategory, designType] = shelf

  for (const item of items) {
    const id = designIdOf(item.skuW)
    const minCarat = parseFloat(String(item.title).match(/^([\d.]+)/)?.[1] ?? '') || null
    const carat = round(item.tcw)
    const size = ['', 'NA', 'NONE'].includes(String(item.size ?? '').trim().toUpperCase())
      ? ''
      : String(item.size).trim()

    if (/\s/.test(item.skuW) || /\s/.test(item.skuY))
      report('SKU_WHITESPACE', `${item.skuW} / ${item.skuY} contain a space`)
    if (carat && minCarat && carat - minCarat > 1)
      report('CARAT_MISMATCH', `${id}: titled ${minCarat} ct but total weight is ${carat} ct`)

    const variants = [
      ['White', item.skuW, item.imgW],
      ['Yellow', item.skuY, item.imgY],
    ]
      .filter(([, sku]) => sku)
      .map(([metalColour, sku, images = []]) => {
        if (!images.length) report('NO_IMAGE', `${sku} has no photograph`)
        const gallery = images.map((imgId) => ({ id: imgId, full: thumb(imgId, 1600), thumb: thumb(imgId, 800) }))
        return {
          designId: id,
          sku: String(sku).trim(),
          title: item.title,
          metalColour,
          metal: METAL,
          price: null,
          carat,
          minCarat,
          diamondCount: item.stones ? Math.round(item.stones) : null,
          metalWeight: round(item.gold, 2),
          shape: String(item.shape ?? '').trim(),
          colour: item.color,
          clarity: item.clarity,
          origin: ORIGIN,
          designType,
          size,
          imageId: images[0] ?? '',
          image: gallery[0]?.full ?? null,
          thumbnail: gallery[0]?.thumb ?? null,
          gallery,
          video: null,
        }
      })

    const lead = variants[0]
    designs.push({
      id,
      slug: `${slugify(item.title)}-${slugify(id)}`,
      title: item.title,
      category,
      categorySlug: slugify(category),
      subCategory,
      subCategorySlug: slugify(subCategory),
      setting: null,
      designType,
      shape: lead.shape,
      metal: METAL,
      colour: lead.colour,
      clarity: lead.clarity,
      origin: ORIGIN,
      size,
      carat,
      minCarat,
      diamondCount: lead.diamondCount,
      metalColours: variants.map((v) => v.metalColour),
      priceFrom: null,
      priceTo: null,
      caratFrom: carat,
      image: lead.image,
      thumbnail: lead.thumbnail,
      variants,
    })
  }
}

const seen = new Set()
for (const d of designs) {
  if (seen.has(d.slug)) report('DUPLICATE_SLUG', d.slug)
  seen.add(d.slug)
}

const categories = []
for (const [category, subCategory] of Object.values(SHELVES)) {
  let c = categories.find((x) => x.name === category)
  if (!c) categories.push((c = { name: category, slug: slugify(category), count: 0, subCategories: [] }))
  if (!c.subCategories.some((s) => s.name === subCategory)) {
    const count = designs.filter((d) => d.category === category && d.subCategory === subCategory).length
    c.subCategories.push({ name: subCategory, slug: slugify(subCategory), count })
    c.count += count
  }
}

const uniq = (xs) => [...new Set(xs.filter(Boolean))].sort()
const skus = designs.reduce((n, d) => n + d.variants.length, 0)

const catalogue = {
  generatedAt: new Date().toISOString(),
  source: { sheetId: null },
  stats: { designs: designs.length, skus, categories: categories.length, priceFrom: null, priceTo: null },
  filters: {
    shapes: uniq(designs.map((d) => d.shape)),
    metalColours: uniq(designs.flatMap((d) => d.metalColours)),
    sizes: uniq(designs.map((d) => d.size)),
  },
  categories,
  designs,
}

fs.mkdirSync(path.dirname(OUT), { recursive: true })
fs.writeFileSync(OUT, JSON.stringify(catalogue, null, 1) + '\n')

/**
 * Cloudflare Pages redirects: every design id and SKU address forwards to the
 * piece's current slug — `/piece/br-sl-02-w` is a link that never goes stale.
 * 307, not 308: a title can change back, and a permanent redirect would be
 * cached by browsers past that. (The pages also exist in the static export, so
 * the same addresses work on any other static host, via a client redirect.)
 */
const redirects = designs.flatMap((d) =>
  [...new Set([d.id, ...d.variants.map((v) => v.sku)].map(slugify))]
    .filter((alias) => alias !== d.slug)
    .map((alias) => `/piece/${alias} /piece/${d.slug} 307`),
)
fs.mkdirSync(path.dirname(REDIRECTS), { recursive: true })
fs.writeFileSync(REDIRECTS, `# Generated by scripts/build-catalogue.mjs — do not edit.\n${redirects.join('\n')}\n`)

console.log(`catalogue: ${designs.length} designs · ${skus} SKUs · ${categories.length} categories → data/products.json`)
for (const p of problems) console.log(`  ! ${p.code}: ${p.detail}`)
