'use client'
import { useState, useEffect } from 'react'
import { getMarketPrices, type MarketPrice } from '@/lib/api'

const COMMODITIES = [
  'wheat', 'rice', 'maize', 'cotton', 'soybean',
  'onion', 'tomato', 'potato', 'mustard', 'arhar',
]

const COMMODITY_EMOJI: Record<string, string> = {
  wheat: '🌾', rice: '🍚', maize: '🌽', cotton: '🪻', soybean: '🫘',
  onion: '🧅', tomato: '🍅', potato: '🥔', mustard: '🌿', arhar: '🫘',
}

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
    <div className="space-y-4">
      {/* Commodity selector */}
      <div className="bg-white rounded-2xl border border-green-100 shadow-sm p-4">
        <h2 className="text-sm font-semibold text-gray-700 mb-3">
          💰 Live Mandi Prices (₹/quintal)
        </h2>
        <div className="flex flex-wrap gap-2">
          {COMMODITIES.map((c) => (
            <button
              key={c}
              onClick={() => setCommodity(c)}
              className={`px-3 py-1.5 rounded-full text-xs font-medium transition-all ${
                commodity === c
                  ? 'bg-orange-600 text-white shadow'
                  : 'bg-orange-50 text-orange-700 border border-orange-200 hover:bg-orange-100'
              }`}
            >
              {COMMODITY_EMOJI[c] || '🌱'} {c.charAt(0).toUpperCase() + c.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {loading && (
        <div className="bg-white rounded-2xl border border-orange-100 p-8 text-center">
          <div className="text-3xl mb-2 animate-pulse">💰</div>
          <p className="text-gray-500 text-sm">Fetching prices…</p>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-2xl p-4 text-red-600 text-sm">{error}</div>
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
              },
              {
                label: 'Lowest Price',
                value: `₹${Math.min(...prices.map((p) => parseFloat(p.modal_price) || 0)).toLocaleString()}`,
                color: 'bg-red-50 border-red-200 text-red-800',
              },
              {
                label: 'Average Price',
                value: `₹${Math.round(prices.reduce((s, p) => s + (parseFloat(p.modal_price) || 0), 0) / prices.length).toLocaleString()}`,
                color: 'bg-blue-50 border-blue-200 text-blue-800',
              },
            ].map((stat) => (
              <div key={stat.label} className={`rounded-2xl border p-4 ${stat.color}`}>
                <p className="text-xs opacity-70">{stat.label}</p>
                <p className="text-2xl font-bold mt-1">{stat.value}</p>
                <p className="text-xs opacity-60">/quintal</p>
              </div>
            ))}
          </div>

          {/* Price table */}
          <div className="bg-white rounded-2xl border border-green-100 shadow-sm overflow-hidden">
            <div className="px-4 py-3 bg-gray-50 border-b border-gray-100">
              <p className="text-sm font-semibold text-gray-700">
                {COMMODITY_EMOJI[commodity] || '🌱'} {commodity.charAt(0).toUpperCase() + commodity.slice(1)} — All Markets
              </p>
            </div>
            <div className="divide-y divide-gray-50">
              {prices.map((price, i) => {
                const val = parseFloat(price.modal_price) || 0
                const pct = maxPrice ? (val / maxPrice) * 100 : 0
                return (
                  <div key={i} className="px-4 py-3 hover:bg-green-50 transition-colors">
                    <div className="flex justify-between items-start mb-1">
                      <div>
                        <p className="text-sm font-medium text-gray-800">{price.market}</p>
                        <p className="text-xs text-gray-400">{price.state}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-bold text-green-700">₹{parseInt(price.modal_price || '0').toLocaleString()}</p>
                        {price.min_price && price.max_price && (
                          <p className="text-xs text-gray-400">
                            ₹{parseInt(price.min_price).toLocaleString()} – ₹{parseInt(price.max_price).toLocaleString()}
                          </p>
                        )}
                      </div>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-1.5 mt-2">
                      <div
                        className="bg-green-500 h-1.5 rounded-full transition-all"
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                  </div>
                )
              })}
            </div>
          </div>

          <p className="text-xs text-gray-400 text-center">
            Data source: data.gov.in • Updated periodically • Prices may vary from actual mandi rates
          </p>
        </>
      )}
    </div>
  )
}
