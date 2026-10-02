import type { Metadata } from 'next'
import Link from 'next/link'
import WhatsAppIcon from '@/components/WhatsAppIcon'
import { catalogue } from '@/lib/catalogue'
import { CONTACT, hasWhatsApp, mailtoHref, whatsappHref } from '@/lib/contact'
import { siteUrl } from '@/lib/site'

export const metadata: Metadata = {
  title: 'The Company',
  description:
    'Seyaa Jewels Inc. supplies 14K gold jewellery set with IGI-certified lab-grown diamonds to the trade, from 42 West 48th Street in New York.',
  alternates: { canonical: siteUrl('/company') },
  openGraph: {
    title: 'Seyaa Jewels — The Company',
    description:
      '14K gold lab-grown diamond jewellery for trade buyers, from New York’s diamond district.',
    url: siteUrl('/company'),
    images: ['/brand/og.jpg'],
  },
}

const PROOF = [
  {
    figure: `${catalogue.stats.designs}`,
    label: 'Designs',
    body: `${catalogue.stats.skus} SKUs across ${catalogue.stats.categories} categories, each published with its full specification.`,
  },
  {
    figure: '14K',
    label: 'White & yellow gold',
    body: 'Every design is offered in both metals, each with its own SKU, so the two can be quoted separately.',
  },
  {
    figure: 'E–F',
    label: 'Colour, VS–SI clarity',
    body: 'The grade band every stone in the catalogue is held to — colourless, stated per SKU.',
  },
  {
    figure: 'IGI',
    label: 'Certified',
    body: 'Independently graded by the International Gemological Institute.',
  },
]

/** The client's own description of each line, as written for the printed catalogue. */
const LINES = [
  {
    title: 'Tennis bracelets',
    body: 'The classic four-prong line of uniform round brilliants, and an all-mix fancy line that alternates shapes for more movement and light. 7 inch, box clasp with safety catch.',
  },
  {
    title: 'Tennis necklaces',
    body: 'A straight line of uniform round brilliants, or a graduated line that builds to the largest stones at the front for a tapered drape. 16.5 inch, box clasp with safety catch.',
  },
  {
    title: 'Round studs',
    body: 'An open four-prong basket that lets light through the pavilion, or a low three-prong martini mount that sits close to the ear. Push back, 1 to 10 ct the pair.',
  },
  {
    title: 'Eternity bands',
    body: 'Round brilliants in a continuous shared-prong circuit, 2 to 14 ct. Supplied in US size 7 as standard.',
  },
]

export default function CompanyPage() {
  const initials = CONTACT.person
    .split(/\s+/)
    .map((part) => part[0])
    .join('')

  return (
    <>
      {/* ------------------------------------------------------------- opening */}
      <section className="border-b border-ink-line">
        <div className="shell py-16 lg:py-24">
          <p className="eyebrow">The company</p>
          <h1 className="mt-6 max-w-4xl font-display text-[2.5rem] leading-[1.08] tracking-tight sm:text-6xl">
            Lab-grown diamond jewellery,
            <br />
            <span className="text-brand">specified for the trade.</span>
          </h1>
          <p className="mt-8 max-w-2xl text-base leading-relaxed text-bone-dim sm:text-lg">
            {CONTACT.legalName} supplies 14K gold jewellery set with IGI-certified
            lab-grown diamonds to retailers and trade buyers, from New York&apos;s diamond
            district. The 2026 catalogue concentrates on the pieces a jewellery counter
            sells every day — tennis bracelets, tennis necklaces, studs and eternity
            bands — each in a full run of carat weights.
          </p>
          <p className="mt-5 max-w-2xl text-base leading-relaxed text-bone-dim sm:text-lg">
            Every specification is published: total carat weight, stone count, metal
            weight, colour, clarity and size, for white and yellow gold separately. Prices
            are given on request.
          </p>
        </div>
      </section>

      {/* --------------------------------------------------------------- proof */}
      <section className="border-b border-ink-line bg-ink-soft">
        <div className="shell grid gap-10 py-16 sm:grid-cols-2 lg:grid-cols-4 lg:py-20">
          {PROOF.map((item) => (
            <div key={item.label}>
              <p className="font-display text-5xl leading-none text-brand">{item.figure}</p>
              <p className="eyebrow mt-4">{item.label}</p>
              <p className="mt-3 text-[0.9375rem] leading-relaxed text-bone-dim">{item.body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* --------------------------------------------------------------- lines */}
      <section className="shell py-16 lg:py-24">
        <div className="max-w-2xl">
          <p className="eyebrow">The 2026 range</p>
          <h2 className="rule-gold mt-4 font-display text-4xl leading-tight tracking-tight sm:text-5xl">
            Four lines, every carat weight
          </h2>
        </div>

        <div className="mt-12 grid gap-x-6 gap-y-10 sm:grid-cols-2 lg:grid-cols-4">
          {LINES.map((line) => (
            <div key={line.title} className="border-t border-ink-line pt-5">
              <h3 className="font-display text-2xl">{line.title}</h3>
              <p className="mt-4 text-[0.9375rem] leading-relaxed text-bone-dim">{line.body}</p>
            </div>
          ))}
        </div>
      </section>

      {/* --------------------------------------------------------- certified */}
      <section className="border-y border-ink-line bg-ink-soft">
        <div className="shell grid gap-10 py-16 lg:grid-cols-[auto_1fr] lg:items-start lg:gap-16 lg:py-24">
          <p className="font-display text-7xl leading-none text-brand sm:text-8xl">IGI</p>
          <div className="max-w-2xl">
            <p className="eyebrow">Independently graded</p>
            <h2 className="rule-gold mt-4 font-display text-4xl leading-tight tracking-tight sm:text-5xl">
              Certified by the International Gemological Institute
            </h2>
            <p className="mt-7 text-[0.9375rem] leading-relaxed text-bone-dim sm:text-base">
              Our jewellery is supplied with IGI certification — one of the largest
              independent gemmological laboratories in the world, and the reference
              most retailers already recognise for lab-grown stones.
            </p>
            <p className="mt-5 text-[0.9375rem] leading-relaxed text-bone-dim sm:text-base">
              The grade on the certificate is not our word for it. That is the whole
              point of it, and the reason it belongs on the counter with the piece
              rather than in a drawer behind it.
            </p>
          </div>
        </div>
      </section>

      {/* ------------------------------------------------------------- contact */}
      <section className="shell py-16 lg:py-24">
        <div className="max-w-2xl">
          <p className="eyebrow">Who you will be dealing with</p>
          <h2 className="rule-gold mt-4 font-display text-4xl leading-tight tracking-tight sm:text-5xl">
            New York
          </h2>
        </div>

        <div className="mt-12 grid gap-10 lg:grid-cols-[18rem_1fr] lg:gap-16">
          <div className="well flex aspect-[4/5] max-w-xs items-center justify-center">
            <span className="font-display text-6xl text-brand/30">{initials}</span>
          </div>

          <div>
            <h3 className="font-display text-3xl">{CONTACT.person}</h3>
            <p className="eyebrow mt-3 text-gold-soft">{CONTACT.legalName}</p>

            <address className="mt-7 text-[0.9375rem] not-italic leading-relaxed text-bone-dim sm:text-base">
              {CONTACT.address.map((line) => (
                <span key={line} className="block">
                  {line}
                </span>
              ))}
              <a href={`tel:+${CONTACT.whatsapp}`} className="mt-4 block text-bone hover:text-gold-soft">
                {CONTACT.phoneDisplay}
              </a>
              <a href={`mailto:${CONTACT.email}`} className="block text-bone hover:text-gold-soft">
                {CONTACT.email}
              </a>
            </address>

            <div className="mt-10 flex flex-wrap items-center gap-4">
              {hasWhatsApp() && (
                <a
                  href={whatsappHref(
                    `Hello ${CONTACT.businessName}, I saw your trade catalogue and would like a quote.`,
                  )}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2.5 bg-gold px-8 py-4 text-[0.6875rem] uppercase tracking-label text-onGold transition-opacity hover:opacity-90"
                >
                  <WhatsAppIcon className="h-4 w-4" />
                  Message us
                </a>
              )}
              <a
                href={mailtoHref(
                  'Enquiry from the Seyaa Jewels trade catalogue',
                  'Hello Seyaa Jewels,\n\nI would like to discuss the following:\n\n',
                )}
                className="border border-ink-line px-8 py-4 text-[0.6875rem] uppercase tracking-label text-bone-dim transition-colors hover:border-gold/50 hover:text-gold-soft"
              >
                Email us
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* ------------------------------------------------------------- closing */}
      <section className="border-t border-ink-line bg-ink-soft">
        <div className="shell py-16 text-center lg:py-20">
          <h2 className="mx-auto max-w-2xl font-display text-3xl leading-tight tracking-tight sm:text-4xl">
            The catalogue is open. Every specification is on it.
          </h2>
          <p className="mx-auto mt-5 max-w-xl text-[0.9375rem] leading-relaxed text-bone-dim">
            Browse {catalogue.stats.designs} designs, note the SKUs that fit your floor,
            and send them to us in one message.
          </p>
          <Link
            href="/collection"
            className="mt-9 inline-block bg-gold px-9 py-4 text-[0.6875rem] uppercase tracking-label text-onGold transition-opacity hover:opacity-90"
          >
            View the collection
          </Link>
        </div>
      </section>
    </>
  )
}
