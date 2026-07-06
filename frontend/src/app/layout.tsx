import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'FarmWise AI — Smart Farming Advisor',
  description: 'AI-powered agricultural assistant powered by IBM Granite and RAG',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
