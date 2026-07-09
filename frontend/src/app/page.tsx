'use client'
import ChatInterface from '@/components/ChatInterface'
import WeatherWidget from '@/components/WeatherWidget'
import MarketPrices from '@/components/MarketPrices'
import FarmingCards from '@/components/FarmingCards'
import { useState } from 'react'
import { Sprout, MessageSquare, CloudSun, TrendingUp, Landmark } from 'lucide-react'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'chat' | 'weather' | 'market' | 'schemes'>('chat')

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="bg-gradient-to-r from-emerald-800 via-emerald-700 to-green-700 text-white shadow-md border-b border-emerald-900/10">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Sprout className="w-8 h-8 text-emerald-300 animate-float-soft" />
            <div>
              <h1 className="text-xl font-extrabold tracking-tight">FarmWise AI</h1>
              <p className="text-emerald-200 text-[10px] font-medium uppercase tracking-wider">IBM Granite + RAG Agricultural Hub</p>
            </div>
          </div>
          <div className="flex items-center gap-2 text-xs bg-emerald-900/40 px-3 py-1.5 rounded-full border border-emerald-500/20">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 inline-block animate-pulse" />
            <span className="font-semibold text-emerald-100">Advisor Connected</span>
          </div>
        </div>
      </header>

      {/* Tab Navigation */}
      <nav className="bg-white/80 backdrop-blur-md border-b border-emerald-100/50 sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 flex gap-2 py-3 overflow-x-auto">
          {[
            { id: 'chat',    label: 'Ask Advisor',    icon: MessageSquare },
            { id: 'weather', label: 'Weather',         icon: CloudSun },
            { id: 'market',  label: 'Mandi Prices',    icon: TrendingUp },
            { id: 'schemes', label: 'Govt Schemes',    icon: Landmark },
          ].map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as typeof activeTab)}
                className={`px-5 py-2.5 rounded-xl text-sm font-semibold transition-all duration-300 flex items-center gap-2 whitespace-nowrap btn-cinematic ${
                  activeTab === tab.id
                    ? 'bg-gradient-to-r from-emerald-600 to-green-600 text-white shadow-[0_4px_12px_rgba(16,185,129,0.2)] scale-[1.02]'
                    : 'text-gray-600 hover:bg-emerald-50 hover:text-emerald-700'
                }`}
              >
                <Icon className="w-4 h-4" />
                {tab.label}
              </button>
            )
          })}
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        <div className={activeTab === 'chat' ? 'animate-slide-up' : 'hidden'}>
          <ChatInterface />
        </div>
        <div className={activeTab === 'weather' ? 'animate-slide-up' : 'hidden'}>
          <WeatherWidget />
        </div>
        <div className={activeTab === 'market' ? 'animate-slide-up' : 'hidden'}>
          <MarketPrices />
        </div>
        <div className={activeTab === 'schemes' ? 'animate-slide-up' : 'hidden'}>
          <FarmingCards />
        </div>
      </main>

      {/* Footer */}
      <footer className="text-center text-xs text-gray-400 py-6 border-t border-green-100 mt-8">
        <p>FarmWise AI • Powered by IBM Granite LLM + RAG • For informational purposes only</p>
        <p className="mt-1">Always consult local agriculture officials for critical farming decisions</p>
      </footer>
    </div>
  )
}
