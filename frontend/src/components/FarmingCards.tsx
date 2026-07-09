'use client'
import { useState, useEffect } from 'react'
import { getSchemes } from '@/lib/api'

interface Scheme {
  id: string
  name: string
  benefit: string
  eligibility: string[]
  apply_at: string
  category: string
  premium?: string
  credit_limit?: string
}

const CATEGORY_FILTERS = [
  { key: '',                label: 'All Schemes',    emoji: '📋' },
  { key: 'income_support',  label: 'Income Support', emoji: '💵' },
  { key: 'insurance',       label: 'Insurance',      emoji: '🛡️' },
  { key: 'credit',          label: 'Credit / Loans', emoji: '🏦' },
  { key: 'irrigation',      label: 'Irrigation',     emoji: '💧' },
  { key: 'organic_farming', label: 'Organic',        emoji: '🌱' },
  { key: 'mechanization',   label: 'Machinery',      emoji: '🚜' },
  { key: 'soil_health',     label: 'Soil Health',    emoji: '🌍' },
  { key: 'market',          label: 'Market',         emoji: '💰' },
]

const SCHEME_COLORS = [
  'border-l-green-500', 'border-l-blue-500', 'border-l-orange-500',
  'border-l-purple-500', 'border-l-teal-500', 'border-l-red-500',
  'border-l-yellow-500', 'border-l-pink-500',
]

export default function FarmingCards() {
  const [schemes, setSchemes] = useState<Scheme[]>([])
  const [loading, setLoading] = useState(true)
  const [category, setCategory] = useState('')
  const [expanded, setExpanded] = useState<string | null>(null)

  useEffect(() => {
    setLoading(true)
    getSchemes(category || undefined)
      .then((data) => setSchemes(data.schemes || []))
      .catch(() => setSchemes([]))
      .finally(() => setLoading(false))
  }, [category])

  return (
    <div className="space-y-4">
      {/* Category filter */}
      <div className="card-premium rounded-2xl p-5">
        <h2 className="text-sm font-bold text-gray-800 mb-3">📢 Government Schemes & Subsidies</h2>
        <div className="flex flex-wrap gap-2">
          {CATEGORY_FILTERS.map((f) => (
            <button
              key={f.key}
              onClick={() => setCategory(f.key)}
              className={`px-4 py-2 rounded-full text-xs font-semibold transition-all duration-300 ${
                category === f.key
                  ? 'bg-purple-700 text-white shadow-[0_4px_10px_rgba(109,40,217,0.2)] scale-[1.02]'
                  : 'bg-purple-50 text-purple-700 border border-purple-200 hover:bg-purple-100 hover:text-purple-800'
              }`}
            >
              {f.emoji} {f.label}
            </button>
          ))}
        </div>
      </div>

      {loading && (
        <div className="card-premium rounded-2xl p-12 text-center">
          <div className="text-3xl mb-2 animate-pulse">📋</div>
          <p className="text-gray-500 text-sm font-medium">Loading schemes…</p>
        </div>
      )}

      {!loading && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {schemes.map((scheme, i) => (
            <div
              key={scheme.id}
              className={`card-premium rounded-2xl border-l-4 ${SCHEME_COLORS[i % SCHEME_COLORS.length]} overflow-hidden`}
            >
              <div
                className="p-4 cursor-pointer hover:bg-gray-50 transition-colors"
                onClick={() => setExpanded(expanded === scheme.id ? null : scheme.id)}
              >
                <div className="flex justify-between items-start gap-2">
                  <h3 className="font-semibold text-gray-800 text-sm leading-tight">{scheme.name}</h3>
                  <span className="text-gray-400 text-lg flex-shrink-0">
                    {expanded === scheme.id ? '▲' : '▼'}
                  </span>
                </div>
                <p className="text-green-700 text-xs font-medium mt-2 bg-green-50 px-2 py-1 rounded-lg inline-block">
                  ✅ {scheme.benefit}
                </p>
              </div>

              {expanded === scheme.id && (
                <div className="px-4 pb-4 space-y-3 border-t border-gray-50 pt-3">
                  <div>
                    <p className="text-xs font-semibold text-gray-600 mb-1">📋 Eligibility</p>
                    <ul className="space-y-1">
                      {scheme.eligibility.map((e) => (
                        <li key={e} className="text-xs text-gray-600 flex items-start gap-1">
                          <span className="text-green-500 flex-shrink-0 mt-0.5">•</span>
                          {e}
                        </li>
                      ))}
                    </ul>
                  </div>

                  {scheme.premium && (
                    <div>
                      <p className="text-xs font-semibold text-gray-600 mb-1">💰 Premium</p>
                      <p className="text-xs text-gray-600">{scheme.premium}</p>
                    </div>
                  )}

                  <div>
                    <p className="text-xs font-semibold text-gray-600 mb-1">📍 How to Apply</p>
                    <p className="text-xs text-gray-600">{scheme.apply_at}</p>
                  </div>

                  <div className="bg-blue-50 border border-blue-100 rounded-lg p-2">
                    <p className="text-xs text-blue-700">
                      📞 Kisan Call Centre: <strong>1800-180-1551</strong> (Free)
                    </p>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
