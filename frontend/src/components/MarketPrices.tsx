'use client'
import { useState, useEffect } from 'react'
import { getMarketPrices, type MarketPrice } from '@/lib/api'
import { 
  TrendingUp, Sprout, ArrowUpRight, ArrowDownRight, 
  Percent, Loader2, AlertCircle, HelpCircle 
} from 'lucide-react'

const COMMODITIES = [
  'wheat', 'rice', 'maize', 'cotton', 'soybean',
  'onion', 'tomato', 'potato', 'mustard', 'arhar',
]

export default function MarketPrices() {
  const [commodity, setCommodity] = useState('wheat')
  const [prices, setPrices] = useState<MarketPrice[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const fetchPrices = async (c: string) => {
    setLoading(true)
    setError('')
    try {
      const data = await getMarketPrices(c)
      setPrices(data)
    } catch (e) {
      setError('Failed to load market prices.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchPrices(commodity)
  }, [commodity])

  const maxPrice = prices.length
    ? Math.max(...prices.map((p) => parseFloat(p.modal_price) || 0))
    : 0

  return (
    <div className="space-y-4 animate-slide-up">
      {/* Commodity selector */}
      <div className="card-premium rounded-2xl p-5">
        <h2 className="text-sm font-bold text-gray-800 mb-3 flex items-center gap-2">
          <TrendingUp className="w-4 h-4 text-emerald-600" />
          Live Mandi Prices (₹/quintal)
        </h2>
        <div className="flex flex-wrap gap-2">
          {COMMODITIES.map((c) => (
            <button
              key={c}
              onClick={() => setCommodity(c)}
              className={`px-4 py-2 rounded-full text-xs font-semibold transition-all duration-300 flex items-center gap-1.5 ${
                commodity === c
                  ? 'bg-orange-600 text-white shadow-[0_4px_10px_rgba(234,88,12,0.2)] scale-[1.02]'
                  : 'bg-orange-50 text-orange-700 border border-orange-200 hover:bg-orange-100 hover:text-orange-800'
              }`}
            >
              <Sprout className="w-3.5 h-3.5" />
              {c.charAt(0).toUpperCase() + c.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {loading && (
        <div className="card-premium rounded-2xl p-12 text-center flex flex-col items-center justify-center">
          <Loader2 className="w-8 h-8 text-orange-600 animate-spin mb-2" />
          <p className="text-gray-500 text-sm font-medium">Fetching prices…</p>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-2xl p-4 text-red-600 text-sm flex items-center gap-2">
          <AlertCircle className="w-4 h-4" />
          <span>{error}</span>
        </div>
      )}

      {!loading && prices.length > 0 && (
        <>
          {/* Summary card */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {[
              {
                label: 'Highest Price',
                value: `₹${Math.max(...prices.map((p) => parseFloat(p.modal_price) || 0)).toLocaleString()}`,
                color: 'bg-green-50 border-green-200 text-green-800',
                icon: ArrowUpRight
              },
              {
                label: 'Lowest Price',
                value: `₹${Math.min(...prices.map((p) => parseFloat(p.modal_price) || 0)).toLocaleString()}`,
                color: 'bg-red-50 border-red-200 text-red-800',
                icon: ArrowDownRight
              },
              {
                label: 'Average Price',
                value: `₹${Math.round(prices.reduce((s, p) => s + (parseFloat(p.modal_price) || 0), 0) / prices.length).toLocaleString()}`,
                color: 'bg-blue-50 border-blue-200 text-blue-800',
                icon: Percent
              },
            ].map((stat) => {
              const Icon = stat.icon
              return (
                <div key={stat.label} className={`rounded-2xl border p-4 flex items-center justify-between shadow-[0_4px_12px_rgba(0,0,0,0.01)] ${stat.color}`}>
                  <div>
                    <p className="text-xs opacity-75 font-semibold">{stat.label}</p>
                    <p className="text-2xl font-extrabold mt-1 tracking-tight">{stat.value}</p>
                    <p className="text-[10px] opacity-60">/quintal</p>
                  </div>
                  <div className="p-2.5 bg-white/40 rounded-xl">
                    <Icon className="w-5 h-5" />
                  </div>
                </div>
              )
            })}
          </div>

          {/* Price table */}
          <div className="card-premium rounded-2xl overflow-hidden">
            <div className="px-4 py-3.5 bg-gray-50/50 border-b border-gray-100 flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-emerald-600" />
              <p className="text-sm font-bold text-gray-800">
                {commodity.charAt(0).toUpperCase() + commodity.slice(1)} — All Markets
              </p>
            </div>
            <div className="divide-y divide-gray-50">
              {prices.map((price, i) => {
                const val = parseFloat(price.modal_price) || 0
                const pct = maxPrice ? (val / maxPrice) * 100 : 0
                return (
                  <div key={i} className="px-4 py-3 hover:bg-emerald-50/30 transition-colors">
                    <div className="flex justify-between items-start mb-1">
                      <div>
                        <p className="text-sm font-semibold text-gray-800">{price.market}</p>
                        <p className="text-xs text-gray-400 font-medium">{price.state}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-extrabold text-emerald-700">₹{parseInt(price.modal_price || '0').toLocaleString()}</p>
                        {price.min_price && price.max_price && (
                          <p className="text-[10px] text-gray-400 font-medium">
                            ₹{parseInt(price.min_price).toLocaleString()} – ₹{parseInt(price.max_price).toLocaleString()}
                          </p>
                        )}
                      </div>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-1.5 mt-2 overflow-hidden">
                      <div
                        className="bg-emerald-500 h-1.5 rounded-full transition-all duration-500"
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

          <p className="text-[10px] text-gray-400 text-center flex items-center justify-center gap-1">
            <HelpCircle className="w-3.5 h-3.5" />
            Data source: data.gov.in • Updated periodically • Prices may vary from actual mandi rates
          </p>
        </>
      )}
    </div>
  )
}
