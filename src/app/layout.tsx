import type { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'
import localFont from 'next/font/local'
import './globals.css'
import SiteHeader from '@/components/SiteHeader'
import WhatsAppIcon from '@/components/WhatsAppIcon'
import { CONTACT, hasWhatsApp, whatsappHref } from '@/lib/contact'
import { catalogue } from '@/lib/catalogue'
import { SITE_URL } from '@/lib/site'

/**
 * The two typefaces the brand kit names, self-hosted from the brand files in
 * `fonts/` (subset to Latin as WOFF2 in `src/fonts/`). No request to a font CDN
 * at runtime, no layout shift, and the build needs no network access.
 */
const montserrat = localFont({
  src: [
    { path: '../fonts/Montserrat-Light.woff2', weight: '300', style: 'normal' },
    { path: '../fonts/Montserrat-Regular.woff2', weight: '400', style: 'normal' },
    { path: '../fonts/Montserrat-SemiBold.woff2', weight: '600', style: 'normal' },
    { path: '../fonts/Montserrat-Bold.woff2', weight: '700', style: 'normal' },
  ],
  display: 'swap',
  variable: '--font-montserrat',
})

const allura = localFont({
  src: '../fonts/Allura-Regular.woff2',
  weight: '400',
  display: 'swap',
  variable: '--font-allura',
})

export const metadata: Metadata = {
  // Resolves relative asset paths below into the absolute URLs Open Graph
  // requires. Absent, Next falls back to http://localhost:3000 and every
  // shared link advertises a card image nobody can load.
  metadataBase: new URL(SITE_URL),
  title: {
    default: 'Seyaa Jewels — Trade Catalogue 2026',
    template: '%s · Seyaa Jewels',
  },
  description:
    'The Seyaa Jewels Inc. trade catalogue — 14K gold lab-grown diamond tennis bracelets, tennis necklaces, studs and eternity bands, IGI certified, with full specifications. Prices on request.',
  openGraph: {
    title: 'Seyaa Jewels — Trade Catalogue 2026',
    description:
      '14K gold lab-grown diamond jewellery for trade buyers. IGI certified, specified in full, prices on request.',
    type: 'website',
    siteName: 'Seyaa Jewels',
    url: SITE_URL,
    images: ['/brand/og.jpg'],
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${montserrat.variable} ${allura.variable}`}>
      <body className="flex min-h-screen flex-col">
        <SiteHeader categories={catalogue.categories} />

        <main className="flex-1">{children}</main>

        {/* The brand's own lockup is white on orange, so the footer closes the
            page the same way — and it is the one place a full orange field
            cannot fight the product photography. */}
        <footer className="mt-24 bg-brand text-white">
          <div className="shell grid gap-10 py-16 sm:grid-cols-2 lg:grid-cols-4">
            <div>
              {/* The artwork is a single flat colour, so brightness(0) invert(1)
                  renders the same file in white — no second asset to keep in
                  step with the first. */}
              <Image
                src="/brand/mark.webp"
                alt=""
                width={117}
                height={160}
                className="h-16 w-auto [filter:brightness(0)_invert(1)]"
              />
              <p className="mt-3 font-script text-[2.5rem] leading-none text-white">Seyaa Jewels</p>
              <p className="mt-5 max-w-xs text-sm leading-relaxed text-white/80">
                14K gold jewellery set with IGI-certified lab-grown diamonds, for
                trade buyers.
              </p>
            </div>

            <div>
              <p className="eyebrow text-white/70">Collection</p>
              <ul className="mt-3 space-y-0.5">
                {catalogue.categories.map((c) => (
                  <li key={c.slug}>
                    <Link
                      href={`/collection?category=${c.slug}`}
                      className="block py-2.5 text-sm text-white/85 transition-colors hover:text-white"
                    >
                      {c.name}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <p className="eyebrow text-white/70">Information</p>
              <ul className="mt-3 space-y-0.5">
                <li>
                  <Link href="/company" className="block py-2.5 text-sm text-white/85 transition-colors hover:text-white">
                    The company
                  </Link>
                </li>
                <li>
                  <Link href="/guide" className="block py-2.5 text-sm text-white/85 transition-colors hover:text-white">
                    Understanding your diamond
                  </Link>
                </li>
                <li>
                  <Link href="/collection" className="block py-2.5 text-sm text-white/85 transition-colors hover:text-white">
                    Full catalogue
                  </Link>
                </li>
              </ul>
            </div>

            <div>
              <p className="eyebrow text-white/70">Enquiries</p>
              <p className="mt-4 text-sm leading-relaxed text-white/80">
                A trade catalogue — pieces are not sold online. Contact {CONTACT.person} with
                a SKU for availability and trade pricing.
              </p>
              <address className="mt-4 text-sm not-italic leading-relaxed text-white/80">
                {CONTACT.legalName}
                {CONTACT.address.map((line) => (
                  <span key={line} className="block">
                    {line}
                  </span>
                ))}
                <a href={`tel:+${CONTACT.whatsapp}`} className="mt-2 block text-white/90 hover:text-white">
                  {CONTACT.phoneDisplay}
                </a>
                <a href={`mailto:${CONTACT.email}`} className="block text-white/90 hover:text-white">
                  {CONTACT.email}
                </a>
              </address>
              {hasWhatsApp() && (
                <a
                  href={whatsappHref(`Hello ${CONTACT.businessName}, I have a question about your collection.`)}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-5 inline-flex items-center gap-2.5 border border-white/40 px-5 py-3 text-[0.6875rem] uppercase tracking-label text-white transition-colors hover:bg-white hover:text-brand"
                >
                  <WhatsAppIcon className="h-4 w-4" />
                  Chat on WhatsApp
                </a>
              )}
            </div>
          </div>

          <div className="border-t border-white/25">
            <div className="shell flex flex-col gap-2 py-6 text-xs text-white/75 sm:flex-row sm:items-center sm:justify-between">
              <p>© {new Date().getFullYear()} {CONTACT.legalName} All rights reserved.</p>
              {/* Counts are a sign of range; "0 designs · 0 SKUs" is only a
                  sign of something broken. Drop the line while empty. */}
              {catalogue.stats.designs > 0 && (
                <p>
                  {catalogue.stats.designs} designs · {catalogue.stats.skus} SKUs · updated{' '}
                  {new Date(catalogue.generatedAt).toLocaleDateString('en-GB', {
                    day: 'numeric',
                    month: 'short',
                    year: 'numeric',
                  })}
                </p>
              )}
            </div>
          </div>
        </footer>
      </body>
    </html>
  )
}
