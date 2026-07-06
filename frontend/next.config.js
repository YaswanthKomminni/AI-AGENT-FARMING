/** @type {import('next').NextConfig} */
const nextConfig = {
  // Allow both local dev and deployed backend URL
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || '',
  },
  // Required for Netlify deployment
  output: 'standalone',
  images: {
    unoptimized: true,
  },
  // Silence the Next.js version warning in production
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/:path*`,
      },
    ]
  },
}

module.exports = nextConfig
