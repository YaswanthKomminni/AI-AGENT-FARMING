'use client'
import { useState, useRef, useEffect } from 'react'
import { sendChatMessage, textToSpeech, type ChatResponse } from '@/lib/api'
import LanguageSelector from './LanguageSelector'
import VoiceInput from './VoiceInput'
import { Bot, Sliders, Zap, Volume2, Copy, Check, Send, Sprout } from 'lucide-react'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  intent?: string
  sources?: string[]
  retrieved_docs?: number
  cached?: boolean
  timestamp: Date
}

const EXAMPLE_QUERIES = [
  'What crop should I grow this season in black soil?',
  'My tomato leaves have yellow spots. What should I do?',
  'What fertilizer should I use for rice?',
  'How much water does cotton require?',
  'Which government schemes am I eligible for?',
  'What is today\'s mandi price for onions?',
]

const INTENT_COLORS: Record<string, string> = {
  crop:       'bg-green-100 text-green-700',
  pest:       'bg-red-100 text-red-700',
  weather:    'bg-blue-100 text-blue-700',
  irrigation: 'bg-cyan-100 text-cyan-700',
  fertilizer: 'bg-yellow-100 text-yellow-700',
  market:     'bg-orange-100 text-orange-700',
  schemes:    'bg-purple-100 text-purple-700',
  general:    'bg-gray-100 text-gray-600',
}

const STATES_AND_DISTRICTS: Record<string, string[]> = {
  'Maharashtra': ['Pune', 'Nashik', 'Nagpur', 'Aurangabad', 'Solapur', 'Satara', 'Kolhapur', 'Amravati'],
  'Karnataka': ['Bangalore', 'Belagavi', 'Tumakuru', 'Mysuru', 'Mandya', 'Hassan', 'Dharwad'],
  'Punjab': ['Ludhiana', 'Amritsar', 'Jalandhar', 'Patiala', 'Bathinda', 'Ferozepur', 'Sangrur'],
  'Andhra Pradesh': ['Guntur', 'Krishna', 'East Godavari', 'West Godavari', 'Chittoor', 'Anantapur', 'Kurnool'],
  'Uttar Pradesh': ['Lucknow', 'Kanpur', 'Varanasi', 'Agra', 'Meerut', 'Bareilly', 'Gorakhpur', 'Prayagraj'],
  'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Bhavnagar', 'Jamnagar', 'Junagadh'],
  'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Tiruchirappalli', 'Salem', 'Tirunelveli', 'Vellore']
}

function formatMarkdown(text: string): string {
  return text
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>[\s\S]*?<\/li>)/g, '<ul>$1</ul>')
    .replace(/\n{2,}/g, '</p><p>')
    .replace(/^(?!<[hul])(.+)$/gm, (m) => m ? m : '')
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '0',
      role: 'assistant',
      content:
        '🌾 **Namaste! I\'m FarmWise AI**, your smart agricultural advisor.\n\n' +
        'I can help you with:\n' +
        '- 🌱 **Crop selection** — best crops for your soil and season\n' +
        '- 🪲 **Pest & disease** diagnosis and treatment\n' +
        '- 💧 **Irrigation** scheduling and water management\n' +
        '- 🌱 **Fertilizer** recommendations\n' +
        '- 💰 **Mandi prices** and market guidance\n' +
        '- 📢 **Government schemes** and subsidies\n\n' +
        'Ask me anything about farming — in English or your regional language!',
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [language, setLanguage] = useState('English')
  const [selectedState, setSelectedState] = useState('')
  const [selectedDistrict, setSelectedDistrict] = useState('')
  const [soilPh, setSoilPh] = useState('')
  const [npkNitrogen, setNpkNitrogen] = useState('')
  const [npkPhosphorus, setNpkPhosphorus] = useState('')
  const [npkPotassium, setNpkPotassium] = useState('')
  const [farmSize, setFarmSize] = useState('')
  const [irrigation, setIrrigation] = useState('')
  const [crop, setCrop] = useState('')
  const [season, setSeason] = useState('')
  const [soilType, setSoilType] = useState('')
  const [showContext, setShowContext] = useState(false)
  const [copiedId, setCopiedId] = useState<string | null>(null)
  const bottomRef = useRef<HTMLDivElement>(null)

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text)
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 1000)
  }

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async (text?: string) => {
    const msg = (text || input).trim()
    if (!msg || loading) return

    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: msg,
      timestamp: new Date(),
    }
    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      const locationVal = selectedDistrict && selectedState 
        ? `${selectedDistrict}, ${selectedState}` 
        : selectedState || selectedDistrict || undefined

      const response: ChatResponse = await sendChatMessage({
        message: msg,
        language,
        location: locationVal,
        state: selectedState || undefined,
        crop: crop || undefined,
        season: season || undefined,
        soil_type: soilType || undefined,
        translate_input: language !== 'English',
        soil_ph: soilPh ? parseFloat(soilPh) : undefined,
        npk_nitrogen: npkNitrogen ? parseInt(npkNitrogen) : undefined,
        npk_phosphorus: npkPhosphorus ? parseInt(npkPhosphorus) : undefined,
        npk_potassium: npkPotassium ? parseInt(npkPotassium) : undefined,
        farm_size: farmSize ? parseFloat(farmSize) : undefined,
        irrigation: irrigation || undefined,
      })

      const botMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.answer,
        intent: response.intent,
        sources: response.sources,
        retrieved_docs: response.retrieved_docs,
        cached: (response as any).cached,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, botMsg])
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: 'assistant',
          content:
            '⚠️ **Connection Error**: Could not reach the AI service.\n\n' +
            'Please ensure the backend server is running on port 8000.',
          timestamp: new Date(),
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  const playAudio = async (text: string) => {
    try {
      const blob = await textToSpeech(text, language)
      const url = URL.createObjectURL(blob)
      const audio = new Audio(url)
      audio.play()
      audio.onended = () => URL.revokeObjectURL(url)
    } catch {
      console.warn('TTS not available')
    }
  }

  return (
    <div className="flex gap-4 h-[calc(100vh-180px)]">
      {/* Chat Panel */}
      <div className="flex-1 flex flex-col bg-white/95 backdrop-blur-md rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.02)] border border-emerald-100/60 overflow-hidden">
        {/* Chat Header */}
        <div className="flex items-center justify-between px-5 py-3.5 bg-gradient-to-r from-emerald-800 to-emerald-700 text-white border-b border-emerald-900/10">
          <div className="flex items-center gap-2">
            <Bot className="w-5 h-5 text-emerald-300" />
            <div>
              <p className="font-bold text-sm tracking-wide">FarmWise AI Advisor</p>
              <p className="text-[10px] text-emerald-200 font-medium">IBM Granite + RAG • {language}</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <LanguageSelector value={language} onChange={setLanguage} />
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex animate-slide-up ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              {msg.role === 'assistant' && (
                <div className="w-8 h-8 rounded-full bg-emerald-700 flex items-center justify-center text-white mr-2 flex-shrink-0 mt-1 shadow-sm">
                  <Sprout className="w-4 h-4 text-emerald-100" />
                </div>
              )}
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 shadow-[0_2px_8px_rgba(0,0,0,0.01)] ${
                  msg.role === 'user'
                    ? 'bg-emerald-700 text-white rounded-tr-none'
                    : 'bg-gray-50 border border-gray-100 rounded-tl-none'
                }`}
              >
                {msg.role === 'assistant' ? (
                  <div
                    className="prose text-sm text-gray-800"
                    dangerouslySetInnerHTML={{ __html: formatMarkdown(msg.content) }}
                  />
                ) : (
                  <div className="flex justify-between items-start gap-3">
                    <p className="text-sm">{msg.content}</p>
                    <button
                      onClick={() => handleCopy(msg.content, msg.id)}
                      className="text-xs text-green-300 hover:text-white transition-colors flex-shrink-0 mt-0.5"
                      title="Copy Question"
                    >
                      {copiedId === msg.id ? <Check className="w-3.5 h-3.5 text-emerald-300" /> : <Copy className="w-3.5 h-3.5" />}
                    </button>
                  </div>
                )}

                {/* Assistant metadata & action buttons (Copy / Speak) */}
                {msg.role === 'assistant' && (
                  <div className="mt-2 pt-2 border-t border-gray-100 flex flex-wrap gap-2 items-center">
                    {msg.intent && (
                      <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${INTENT_COLORS[msg.intent] || INTENT_COLORS.general}`}>
                        {msg.intent}
                      </span>
                    )}
                    {msg.cached && (
                      <span className="text-xs px-2 py-0.5 rounded-full bg-yellow-50 text-yellow-700 font-medium">
                        cached
                      </span>
                    )}
                    {msg.retrieved_docs ? (
                      <span className="text-xs text-gray-400">
                        {msg.retrieved_docs} sources
                      </span>
                    ) : null}
                    {msg.sources?.map((src) => (
                      <span key={src} className="text-xs text-blue-600 bg-blue-50 px-2 py-0.5 rounded-full">
                        {src}
                      </span>
                    ))}
                    
                    <button
                      onClick={() => handleCopy(msg.content, msg.id)}
                      className="ml-auto text-xs text-gray-400 hover:text-green-600 transition-colors flex-shrink-0"
                      title="Copy Answer"
                    >
                      {copiedId === msg.id ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
                    </button>
                    <button
                      onClick={() => playAudio(msg.content)}
                      className="text-xs text-gray-400 hover:text-green-600 transition-colors"
                      title="Listen"
                    >
                      <Volume2 className="w-4 h-4" />
                    </button>
                  </div>
                )}

                <p className="text-xs text-gray-300 mt-1">
                  {msg.timestamp.toLocaleTimeString()}
                </p>
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex items-center gap-2 animate-fade-in">
              <div className="w-8 h-8 rounded-full bg-emerald-700 flex items-center justify-center text-white shadow-sm">
                <Sprout className="w-4 h-4 text-emerald-100 animate-pulse" />
              </div>
              <div className="bg-gray-50 border border-gray-100 rounded-2xl rounded-tl-none px-4 py-3">
                <div className="flex items-center gap-3">
                  <div className="flex gap-1">
                    <span className="w-2 h-2 bg-green-400 rounded-full animate-bounce [animation-delay:0ms]" />
                    <span className="w-2 h-2 bg-green-400 rounded-full animate-bounce [animation-delay:150ms]" />
                    <span className="w-2 h-2 bg-green-400 rounded-full animate-bounce [animation-delay:300ms]" />
                  </div>
                  <span className="text-xs text-gray-400">IBM Granite thinking...</span>
                </div>
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-100 p-4 space-y-3">
          {/* Example queries */}
          <div className="flex gap-2 overflow-x-auto pb-1">
            {EXAMPLE_QUERIES.slice(0, 3).map((q) => (
              <button
                key={q}
                onClick={() => sendMessage(q)}
                className="text-xs text-green-700 bg-green-50 px-3 py-1 rounded-full border border-green-200 whitespace-nowrap hover:bg-green-100 transition-colors"
              >
                {q.length > 35 ? q.slice(0, 35) + '…' : q}
              </button>
            ))}
          </div>

          {/* Text input */}
          <div className="flex gap-2">
            <VoiceInput language={language} onResult={(text) => setInput(text)} />
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage()}
              placeholder="Ask about crops, pests, weather, prices…"
              className="flex-1 border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white/50"
              disabled={loading}
            />
            <button
              onClick={() => sendMessage()}
              disabled={loading || !input.trim()}
              className="bg-emerald-700 text-white px-5 py-2.5 rounded-xl text-sm font-semibold hover:bg-emerald-800 disabled:opacity-40 disabled:cursor-not-allowed transition-all duration-300 flex items-center gap-1.5 shadow-[0_4px_10px_rgba(16,185,129,0.15)]"
            >
              <Send className="w-4 h-4" />
              Send
            </button>
          </div>
        </div>
      </div>

      <div className="w-72 hidden lg:flex flex-col gap-3 overflow-y-auto max-h-full pr-1">
        <div className="card-premium rounded-2xl p-5">
          <h3 className="font-bold text-gray-800 text-sm mb-3 flex items-center gap-2">
            <Sliders className="w-4 h-4 text-emerald-600" />
            Farming Context
          </h3>
          <div className="space-y-3">
            <div>
              <label className="text-xs text-gray-500 font-medium block mb-1">State</label>
              <select
                value={selectedState}
                onChange={(e) => {
                  setSelectedState(e.target.value)
                  setSelectedDistrict('')
                }}
                className="w-full border border-gray-200 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-green-500 bg-white/50"
              >
                <option value="">Select State</option>
                {Object.keys(STATES_AND_DISTRICTS).map((state) => (
                  <option key={state} value={state}>
                    {state}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="text-xs text-gray-500 font-medium block mb-1">District</label>
              <select
                value={selectedDistrict}
                onChange={(e) => setSelectedDistrict(e.target.value)}
                disabled={!selectedState}
                className="w-full border border-gray-200 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-green-500 bg-white/50 disabled:opacity-50"
              >
                <option value="">{selectedState ? 'Select District' : 'Select State first'}</option>
                {selectedState &&
                  STATES_AND_DISTRICTS[selectedState].map((district) => (
                    <option key={district} value={district}>
                      {district}
                    </option>
                  ))}
              </select>
            </div>
            <div>
              <label className="text-xs text-gray-500 font-medium block mb-1">Crop</label>
              <input
                value={crop}
                onChange={(e) => setCrop(e.target.value)}
                placeholder="e.g., Rice, Wheat, Cotton"
                className="w-full border border-gray-200 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-green-500 bg-white/50"
              />
            </div>
            <div>
              <label className="text-xs text-gray-500 font-medium block mb-1">Season</label>
              <select
                value={season}
                onChange={(e) => setSeason(e.target.value)}
                className="w-full border border-gray-200 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-green-500 bg-white/50"
              >
                <option value="">Select season</option>
                <option value="kharif">Kharif (June–Oct)</option>
                <option value="rabi">Rabi (Nov–Mar)</option>
                <option value="zaid">Zaid (Apr–Jun)</option>
              </select>
            </div>
            <div>
              <label className="text-xs text-gray-500 font-medium block mb-1">Soil Type</label>
              <select
                value={soilType}
                onChange={(e) => setSoilType(e.target.value)}
                className="w-full border border-gray-200 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-green-500 bg-white/50"
              >
                <option value="">Select soil type</option>
                <option value="alluvial">Alluvial</option>
                <option value="black">Black Cotton</option>
                <option value="red">Red Soil</option>
                <option value="laterite">Laterite</option>
                <option value="sandy">Sandy</option>
              </select>
            </div>
            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="text-xs text-gray-500 font-medium block mb-1">Soil pH</label>
                <input
                  type="number"
                  step="0.1"
                  value={soilPh}
                  onChange={(e) => setSoilPh(e.target.value)}
                  placeholder="pH"
                  className="w-full border border-gray-200 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-green-500 bg-white/50"
                  min="0"
                  max="14"
                />
              </div>
              <div>
                <label className="text-xs text-gray-500 font-medium block mb-1">Farm Size (Ac)</label>
                <input
                  type="number"
                  step="0.5"
                  value={farmSize}
                  onChange={(e) => setFarmSize(e.target.value)}
                  placeholder="Acres"
                  className="w-full border border-gray-200 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-green-500 bg-white/50"
                  min="0"
                />
              </div>
            </div>
            <div>
              <label className="text-xs text-gray-500 font-medium block mb-1">NPK Values (N - P - K)</label>
              <div className="grid grid-cols-3 gap-1">
                <input
                  type="number"
                  value={npkNitrogen}
                  onChange={(e) => setNpkNitrogen(e.target.value)}
                  placeholder="N"
                  className="w-full border border-gray-200 rounded-lg px-2 py-1.5 text-xs text-center focus:outline-none focus:ring-1 focus:ring-green-500 bg-white/50"
                  min="0"
                />
                <input
                  type="number"
                  value={npkPhosphorus}
                  onChange={(e) => setNpkPhosphorus(e.target.value)}
                  placeholder="P"
                  className="w-full border border-gray-200 rounded-lg px-2 py-1.5 text-xs text-center focus:outline-none focus:ring-1 focus:ring-green-500 bg-white/50"
                  min="0"
                />
                <input
                  type="number"
                  value={npkPotassium}
                  onChange={(e) => setNpkPotassium(e.target.value)}
                  placeholder="K"
                  className="w-full border border-gray-200 rounded-lg px-2 py-1.5 text-xs text-center focus:outline-none focus:ring-1 focus:ring-green-500 bg-white/50"
                  min="0"
                />
              </div>
            </div>
            <div>
              <label className="text-xs text-gray-500 font-medium block mb-1">Irrigation Method</label>
              <select
                value={irrigation}
                onChange={(e) => setIrrigation(e.target.value)}
                className="w-full border border-gray-200 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-1 focus:ring-green-500 bg-white/50"
              >
                <option value="">Select irrigation</option>
                <option value="drip">Drip Irrigation</option>
                <option value="sprinkler">Sprinkler Irrigation</option>
                <option value="borewell">Borewell Flood</option>
                <option value="canal">Canal Irrigation</option>
                <option value="rainfed">Rainfed (No Irrigation)</option>
              </select>
            </div>
          </div>
          <p className="text-[10px] text-gray-400 mt-4 leading-normal">
            Providing context improves AI recommendation accuracy.
          </p>
        </div>

        {/* Quick Queries */}
        <div className="card-premium rounded-2xl p-5">
          <h3 className="font-bold text-gray-800 text-sm mb-3 flex items-center gap-2">
            <Zap className="w-4 h-4 text-amber-500" />
            Quick Queries
          </h3>
          <div className="space-y-2">
            {EXAMPLE_QUERIES.slice(3).map((q) => (
              <button
                key={q}
                onClick={() => sendMessage(q)}
                className="w-full text-left text-xs text-gray-600 bg-gray-50/50 px-3 py-2.5 rounded-lg border border-gray-100/50 hover:bg-emerald-50 hover:border-emerald-200 hover:text-emerald-700 transition-colors"
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
