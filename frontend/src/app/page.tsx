'use client'
import ChatInterface from '@/components/ChatInterface'
import WeatherWidget from '@/components/WeatherWidget'
import MarketPrices from '@/components/MarketPrices'
import FarmingCards from '@/components/FarmingCards'
import { useState } from 'react'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'chat' | 'weather' | 'market' | 'schemes'>('chat')

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">
      {/* Header */}
      <header className="bg-green-700 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-3xl">🌾</span>
            <div>
              <h1 className="text-xl font-bold tracking-tight">FarmWise AI</h1>
              <p className="text-green-200 text-xs">Powered by IBM Granite + RAG</p>
            </div>
          </div>
          <div className="flex items-center gap-2 text-xs text-green-200">
            <span className="w-2 h-2 rounded-full bg-green-300 inline-block animate-pulse" />
            AI Agent Active
          </div>
        </div>
      </header>

      {/* Tab Navigation */}
      <nav className="bg-white border-b border-green-100 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 flex gap-1 py-2 overflow-x-auto">
          {[
            { id: 'chat',    label: '💬 Ask Advisor',    desc: 'AI Chat' },
            { id: 'weather', label: '🌦 Weather',         desc: 'Forecast' },
            { id: 'market',  label: '💰 Mandi Prices',    desc: 'Markets' },
            { id: 'schemes', label: '📢 Govt Schemes',    desc: 'Subsidies' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as typeof activeTab)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all whitespace-nowrap ${
                activeTab === tab.id
                  ? 'bg-green-700 text-white shadow'
                  : 'text-gray-600 hover:bg-green-50 hover:text-green-700'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        {activeTab === 'chat' && <ChatInterface />}
        {activeTab === 'weather' && <WeatherWidget />}
        {activeTab === 'market' && <MarketPrices />}
        {activeTab === 'schemes' && <FarmingCards />}
      </main>

      {/* Footer */}
      <footer className="text-center text-xs text-gray-400 py-6 border-t border-green-100 mt-8">
        <p>FarmWise AI • Powered by IBM Granite LLM + RAG • For informational purposes only</p>
        <p className="mt-1">Always consult local agriculture officials for critical farming decisions</p>
      </footer>
    </div>
  )
}
