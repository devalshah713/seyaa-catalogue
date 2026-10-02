/**
 * Where enquiries go — the one place contact details live.
 *
 * The WhatsApp number and email can be overridden from the environment
 * (`NEXT_PUBLIC_WHATSAPP_NUMBER`, `NEXT_PUBLIC_SALES_EMAIL`) in Cloudflare Pages →
 * Settings → Variables, so they can change without a code change.
 * `NEXT_PUBLIC_` is required so the value is inlined into the static build.
 */

/** Whatever a human pastes — "+1 (917) 801-6060" — reduced to wa.me's format. */
function normaliseNumber(input: string | undefined): string {
  const digits = (input ?? '').replace(/\D/g, '')
  // International numbers run 8–15 digits including country code; anything
  // outside that is a typo, and a wrong number is worse than no button.
  return /^\d{8,15}$/.test(digits) ? digits : ''
}

/** Fallback when no environment variable is set: +1 917 801 6060, New York. */
const WHATSAPP_FALLBACK = '19178016060'

export const CONTACT = {
  whatsapp: normaliseNumber(process.env.NEXT_PUBLIC_WHATSAPP_NUMBER || WHATSAPP_FALLBACK),
  email: process.env.NEXT_PUBLIC_SALES_EMAIL || 'seyaajewels@gmail.com',
  businessName: 'Seyaa Jewels',
  legalName: 'Seyaa Jewels Inc.',
  person: 'Rahul Shah',
  phoneDisplay: '+1 917 801 6060',
  address: ['42 West 48th Street, Suite #600', 'New York, NY 10036', 'United States'],
} as const

export const hasWhatsApp = () => CONTACT.whatsapp.length > 0

/**
 * A wa.me deep link. Opens the WhatsApp app on a phone and WhatsApp Web on a
 * desktop, landing straight in the chat with the message already typed — the
 * customer only has to press send.
 */
export function whatsappHref(message: string): string {
  return `https://wa.me/${CONTACT.whatsapp}?text=${encodeURIComponent(message)}`
}

export function mailtoHref(subject: string, body: string): string {
  return `mailto:${CONTACT.email}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`
}
