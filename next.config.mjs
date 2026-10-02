/** @type {import('next').NextConfig} */
const nextConfig = {
  // Cloudflare Pages serves static files, so every route is prerendered into
  // `out/` at build time — there is no server at runtime.
  output: 'export',
  images: {
    // Static export has no image optimiser. Product photography is requested
    // straight from Google Drive's thumbnail endpoint, which already resizes
    // (`sz=w800` / `sz=w1600`), so visitors never download the 1.3 MB PNG.
    unoptimized: true,
  },
}

export default nextConfig
