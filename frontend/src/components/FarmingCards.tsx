'use client'
import { useState, useEffect } from 'react'
import { getSchemes } from '@/lib/api'
import { 
  LayoutGrid, Coins, BadgeCheck, Landmark, CloudRain, Sprout, 
  Tractor, Globe, DollarSign, ChevronUp, ChevronDown, Check, Loader2, Phone 
} from 'lucide-react'

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
  { key: '',                label: 'All Schemes',    icon: LayoutGrid },
  { key: 'income_support',  label: 'Income Support', icon: Coins },
  { key: 'insurance',       label: 'Insurance',      icon: BadgeCheck },
  { key: 'credit',          label: 'Credit / Loans', icon: Landmark },
  { key: 'irrigation',      label: 'Irrigation',     icon: CloudRain },
  { key: 'organic_farming', label: 'Organic',        icon: Sprout },
  { key: 'mechanization',   label: 'Machinery',      icon: Tractor },
  { key: 'soil_health',     label: 'Soil Health',    icon: Globe },
  { key: 'market',          label: 'Market',         icon: DollarSign },
]

const SCHEME_COLORS = [
  'border-l-emerald-500', 'border-l-blue-500', 'border-l-orange-500',
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
    <div className="space-y-4 animate-slide-up">
      {/* Category filter */}
      <div className="card-premium rounded-2xl p-5">
        <h2 className="text-sm font-bold text-gray-800 mb-3 flex items-center gap-2">
          <Landmark className="w-4 h-4 text-emerald-600" />
          Government Schemes & Subsidies
        </h2>
        <div className="flex flex-wrap gap-2">
          {CATEGORY_FILTERS.map((f) => {
            const Icon = f.icon
            return (
              <button
                key={f.key}
                onClick={() => setCategory(f.key)}
                className={`px-4 py-2 rounded-full text-xs font-semibold transition-all duration-300 flex items-center gap-1.5 ${
                  category === f.key
                    ? 'bg-purple-700 text-white shadow-[0_4px_10px_rgba(109,40,217,0.2)] scale-[1.02]'
                    : 'bg-purple-50 text-purple-700 border border-purple-200 hover:bg-purple-100 hover:text-purple-800'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                {f.label}
              </button>
            )
          })}
        </div>
      </div>

      {loading && (
        <div className="card-premium rounded-2xl p-12 text-center flex flex-col items-center justify-center">
          <Loader2 className="w-8 h-8 text-purple-600 animate-spin mb-2" />
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
                className="p-4 cursor-pointer hover:bg-gray-50/50 transition-colors flex justify-between items-start gap-3"
                onClick={() => setExpanded(expanded === scheme.id ? null : scheme.id)}
              >
                <div className="flex-1">
                  <h3 className="font-bold text-gray-800 text-sm leading-snug">{scheme.name}</h3>
                  <div className="flex items-center gap-1 mt-2 text-emerald-700 text-xs font-semibold bg-emerald-50 px-2.5 py-1 rounded-lg w-fit">
                    <Check className="w-3.5 h-3.5" />
                    <span>{scheme.benefit}</span>
                  </div>
                </div>
                <button className="text-gray-400 p-1 hover:text-gray-600 transition-colors">
                  {expanded === scheme.id ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                </button>
              </div>

              {expanded === scheme.id && (
                <div className="px-4 pb-4 space-y-3 border-t border-gray-50 pt-3 animate-fade-in">
                  <div>
                    <p className="text-xs font-bold text-gray-600 mb-1">Eligibility Requirements</p>
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
                      <p className="text-xs font-bold text-gray-600 mb-1">Premium</p>
                      <p className="text-xs text-gray-600">{scheme.premium}</p>
                    </div>
                  )}

                  <div>
                    <p className="text-xs font-bold text-gray-600 mb-1">How to Apply</p>
                    <p className="text-xs text-gray-600">{scheme.apply_at}</p>
                  </div>

                  <div className="bg-blue-50 border border-blue-100 rounded-lg p-2.5 flex items-center gap-2">
                    <Phone className="w-4 h-4 text-blue-600 flex-shrink-0" />
                    <p className="text-xs text-blue-700">
                      Kisan Call Centre: <strong>1800-180-1551</strong> (Toll Free)
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
