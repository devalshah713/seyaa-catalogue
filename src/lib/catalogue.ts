import data from '../../data/products.json'

export type GalleryImage = { id: string; full: string; thumb: string }

export type Variant = {
  designId: string
  sku: string
  title: string
  metalColour: 'White' | 'Yellow' | 'Rose'
  metal: string
  price: number | null
  carat: number | null
  minCarat: number | null
  diamondCount: number | null
  metalWeight: number | null
  shape: string
  colour: string
  clarity: string
  origin: string
  designType: string
  size: string
  imageId: string
  image: string | null
  thumbnail: string | null
  gallery: GalleryImage[]
}

export type Design = {
  id: string
  slug: string
  title: string
  category: string
  categorySlug: string
  subCategory: string
  subCategorySlug: string
  /** "Prong" / "Bezel", or null when the title does not say. */
  setting: string | null
  designType: string
  shape: string
  metal: string
  colour: string
  clarity: string
  origin: string
  size: string
  carat: number | null
  minCarat: number | null
  diamondCount: number | null
  metalColours: Variant['metalColour'][]
  priceFrom: number | null
  priceTo: number | null
  caratFrom: number | null
  image: string | null
  thumbnail: string | null
  variants: Variant[]
}

export type SubCategory = { name: string; slug: string; count: number }

export type Category = {
  name: string
  slug: string
  count: number
  /** Narrower shelves within the category — "Tennis", "Eternity Bands". */
  subCategories: SubCategory[]
}

export type Catalogue = {
  generatedAt: string
  // Null when no source sheet is configured, and the price bounds are null
  // when there is nothing priced to take bounds of.
  source: { sheetId: string | null }
  stats: {
    designs: number
    skus: number
    categories: number
    priceFrom: number | null
    priceTo: number | null
  }
  filters: { shapes: string[]; metalColours: string[]; sizes: string[] }
  categories: Category[]
  designs: Design[]
}

export const catalogue = data as unknown as Catalogue

export const designs = catalogue.designs
export const categories = catalogue.categories

export function getDesign(slug: string): Design | undefined {
  return designs.find((d) => d.slug === slug)
}

/** Lower-case, hyphenated form of a design id or SKU — "123 RGW" → "123-rgw". */
const slugPart = (s: string) => s.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '')

/**
 * Resolve an address that is not a current slug back to its design.
 *
 * A slug is built from the title, and titles get edited. The design id is the
 * stable part, so `/piece/br-sl-02` (a design) and `/piece/br-sl-02-w` (a SKU)
 * are permanent addresses worth sharing, and a stale title-derived slug still
 * finds its way home as long as it ends in the design id.
 */
export function findByIdentifier(slug: string): Design | undefined {
  const key = slugPart(slug)
  if (!key) return undefined
  return (
    designs.find((d) => slugPart(d.id) === key) ??
    designs.find((d) => d.variants.some((v) => slugPart(v.sku) === key)) ??
    designs.find((d) => key.endsWith(`-${slugPart(d.id)}`))
  )
}

/** Every short address a design answers to: its id and each of its SKUs. */
export function aliasesOf(design: Design): string[] {
  return [...new Set([design.id, ...design.variants.map((v) => v.sku)].map(slugPart))].filter(
    (alias) => alias !== design.slug,
  )
}

export function getCategory(slug: string): Category | undefined {
  return categories.find((c) => c.slug === slug)
}

export function getSubCategory(categorySlug: string, subSlug: string): SubCategory | undefined {
  return getCategory(categorySlug)?.subCategories.find((s) => s.slug === subSlug)
}

/**
 * Prices are not published — this is a trade catalogue and every price is on
 * request. `scripts/build-catalogue.mjs` writes null for every price, so this
 * reads "Price on request" throughout.
 *
 * The formatting is kept rather than deleted because it is what makes turning
 * prices back on a one-line change in the sync — and because a figure that
 * somehow survives should still render as money rather than as a raw float.
 */
export function formatPrice(value: number | null | undefined): string {
  if (typeof value !== 'number' || !isFinite(value)) return 'Price on request'
  return value.toLocaleString('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0,
  })
}

/** "From $2,700" when the metal colours are priced differently. */
export function priceRange(design: Design): string {
  const { priceFrom, priceTo } = design
  if (typeof priceFrom !== 'number') return 'Price on request'
  if (typeof priceTo === 'number' && priceTo !== priceFrom) return `From ${formatPrice(priceFrom)}`
  return formatPrice(priceFrom)
}

export function formatCarat(value: number | null | undefined): string {
  if (typeof value !== 'number' || !isFinite(value)) return '—'
  return `${value.toFixed(2).replace(/\.00$/, '')} ct`
}

/**
 * Grading language means nothing to most buyers, so every spec that uses a
 * trade code is paired with the plain-English equivalent shown alongside it.
 */
export const PLAIN_ENGLISH: Record<string, { label: string; meaning: string }> = {
  'E-F': {
    label: 'Colourless',
    meaning:
      'E–F sits in the top colour band. The diamond reads as pure white to the eye, with no warm tint.',
  },
  'VS-SI': {
    label: 'Typically eye-clean',
    meaning:
      'VS–SI covers very slightly to slightly included stones. Inclusions are small and, at this grade, are not normally visible to the naked eye at a normal viewing distance.',
  },
  'Lab Grown': {
    label: 'Lab grown',
    meaning:
      'Chemically and optically identical to a mined diamond, grown in a controlled environment. Conflict-free and materially better value.',
  },
}

export const METAL_SWATCHES: Record<Variant['metalColour'], string> = {
  White: 'linear-gradient(135deg, #F2F2F0 0%, #C9CACC 55%, #8E9094 100%)',
  Yellow: 'linear-gradient(135deg, #F6E3AE 0%, #D9B45A 55%, #A67C23 100%)',
  Rose: 'linear-gradient(135deg, #F3D2C4 0%, #DDA286 55%, #B87355 100%)',
}
