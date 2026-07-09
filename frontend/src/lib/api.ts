const API_URL = process.env.NEXT_PUBLIC_API_URL || ''

export interface ChatRequest {
  message: string
  language?: string
  location?: string
  state?: string
  crop?: string
  soil_type?: string
  season?: string
  lat?: number
  lon?: number
  translate_input?: boolean
  soil_ph?: number
  npk_nitrogen?: number
  npk_phosphorus?: number
  npk_potassium?: number
  farm_size?: number
  irrigation?: string
}

export interface ChatResponse {
  answer: string
  intent: string
  sources: string[]
  retrieved_docs: number
  language: string
  live_data?: Record<string, unknown>
}

export interface WeatherData {
  current: {
    temperature_2m: number
    relative_humidity_2m: number
    precipitation: number
    condition: string
    wind_speed_10m: number
    apparent_temperature: number
  }
  forecast_7day: Array<{
    date: string
    max_temp: number
    min_temp: number
    precipitation: number
    condition: string
  }>
  farming_advisory: string[]
  city?: string
}

export interface MarketPrice {
  commodity: string
  market: string
  state: string
  modal_price: string
  min_price?: string
  max_price?: string
  date?: string
}

export async function sendChatMessage(req: ChatRequest): Promise<ChatResponse> {
  const res = await fetch(`${API_URL}/api/chat/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(req),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || 'Chat request failed')
  }
  return res.json()
}

export async function getWeatherByCity(city: string): Promise<WeatherData> {
  const res = await fetch(`${API_URL}/api/weather/city/${city.toLowerCase()}`)
  if (!res.ok) throw new Error('Weather data unavailable')
  return res.json()
}

export async function getWeatherByCoords(lat: number, lon: number): Promise<WeatherData> {
  const res = await fetch(`${API_URL}/api/weather/current?lat=${lat}&lon=${lon}`)
  if (!res.ok) throw new Error('Weather data unavailable')
  return res.json()
}

export async function getMarketPrices(commodity: string, state?: string): Promise<MarketPrice[]> {
  const params = new URLSearchParams({ commodity })
  if (state) params.set('state', state)
  const res = await fetch(`${API_URL}/api/market/prices?${params}`)
  if (!res.ok) throw new Error('Market data unavailable')
  const data = await res.json()
  return data.prices
}

export async function getSchemes(category?: string) {
  const params = category ? `?category=${category}` : ''
  const res = await fetch(`${API_URL}/api/schemes/list${params}`)
  if (!res.ok) throw new Error('Failed to fetch schemes')
  return res.json()
}

export async function getCities() {
  const res = await fetch(`${API_URL}/api/weather/cities`)
  if (!res.ok) throw new Error('Failed to fetch cities')
  return res.json()
}

export async function getExampleQueries() {
  const res = await fetch(`${API_URL}/api/chat/examples`)
  if (!res.ok) return { examples: [] }
  return res.json()
}

export async function textToSpeech(text: string, language: string): Promise<Blob> {
  const params = new URLSearchParams({ text, language })
  const res = await fetch(`${API_URL}/api/voice/tts?${params}`, { method: 'POST' })
  if (!res.ok) throw new Error('TTS failed')
  return res.blob()
}
