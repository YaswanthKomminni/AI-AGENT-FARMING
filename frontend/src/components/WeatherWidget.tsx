'use client'
import { useState, useEffect } from 'react'
import { getWeatherByCity, type WeatherData } from '@/lib/api'

const CITIES = [
  'Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata',
  'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow',
  'Patna', 'Bhopal', 'Nagpur', 'Chandigarh', 'Indore',
]

const WMO_EMOJI: Record<string, string> = {
  'Clear sky': '☀️', 'Mainly clear': '🌤️', 'Partly cloudy': '⛅',
  'Overcast': '☁️', 'Fog': '🌫️', 'Light drizzle': '🌦️',
  'Moderate drizzle': '🌧️', 'Heavy drizzle': '🌧️',
  'Slight rain': '🌧️', 'Moderate rain': '🌧️', 'Heavy rain': '⛈️',
  'Thunderstorm': '⛈️', 'Slight snow': '🌨️',
}

function WeatherIcon({ condition }: { condition: string }) {
  return <span className="text-2xl">{WMO_EMOJI[condition] || '🌡️'}</span>
}

export default function WeatherWidget() {
  const [selectedCity, setSelectedCity] = useState('Pune')
  const [weather, setWeather] = useState<WeatherData | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const fetchWeather = async (city: string) => {
    setLoading(true)
    setError('')
    try {
      const data = await getWeatherByCity(city)
      setWeather(data)
    } catch (e) {
      setError('Failed to load weather data. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchWeather(selectedCity)
  }, [selectedCity])

  return (
    <div className="space-y-4">
      {/* City selector */}
      <div className="card-premium rounded-2xl p-5">
        <div className="flex flex-wrap gap-2">
          {CITIES.map((city) => (
            <button
              key={city}
              onClick={() => setSelectedCity(city)}
              className={`px-4 py-2 rounded-full text-xs font-semibold transition-all duration-300 ${
                selectedCity === city
                  ? 'bg-gradient-to-r from-emerald-600 to-green-600 text-white shadow-[0_4px_10px_rgba(16,185,129,0.2)] scale-[1.02]'
                  : 'bg-gray-100 text-gray-600 hover:bg-green-50 hover:text-green-700'
              }`}
            >
              {city}
            </button>
          ))}
        </div>
      </div>

      {loading && (
        <div className="card-premium rounded-2xl p-12 text-center">
          <div className="text-3xl mb-2 animate-bounce">🌤️</div>
          <p className="text-gray-500 text-sm font-medium">Loading weather data…</p>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-2xl p-4 text-red-600 text-sm">
          {error}
        </div>
      )}

      {weather && !loading && (
        <>
          {/* Current conditions */}
          <div className="bg-gradient-to-br from-green-700 to-teal-700 text-white rounded-2xl shadow-sm p-6">
            <div className="flex justify-between items-start">
              <div>
                <h2 className="text-2xl font-bold">
                  {weather.city || selectedCity}
                </h2>
                <p className="text-green-200 text-sm">{weather.current.condition}</p>
                <div className="mt-4 flex items-end gap-2">
                  <span className="text-6xl font-light">{weather.current.temperature_2m}°</span>
                  <span className="text-lg mb-2">C</span>
                </div>
                <p className="text-green-200 text-xs mt-1">Feels like {weather.current.apparent_temperature}°C</p>
              </div>
              <WeatherIcon condition={weather.current.condition} />
            </div>

            <div className="grid grid-cols-3 gap-4 mt-6 pt-4 border-t border-green-600">
              <div className="text-center">
                <p className="text-green-200 text-xs">Humidity</p>
                <p className="font-bold">{weather.current.relative_humidity_2m}%</p>
              </div>
              <div className="text-center">
                <p className="text-green-200 text-xs">Rain</p>
                <p className="font-bold">{weather.current.precipitation} mm</p>
              </div>
              <div className="text-center">
                <p className="text-green-200 text-xs">Wind</p>
                <p className="font-bold">{weather.current.wind_speed_10m} km/h</p>
              </div>
            </div>
          </div>

          {/* Farming Advisories */}
          {weather.farming_advisory.length > 0 && (
            <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4">
              <h3 className="font-semibold text-amber-800 text-sm mb-2">🌾 Farming Advisories</h3>
              <ul className="space-y-2">
                {weather.farming_advisory.map((adv, i) => (
                  <li key={i} className="text-sm text-amber-900 flex items-start gap-2">
                    <span className="mt-0.5 flex-shrink-0">•</span>
                    <span>{adv}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* 7-day forecast */}
          <div className="card-premium rounded-2xl p-5">
            <h3 className="font-bold text-gray-800 text-sm mb-3">📅 7-Day Forecast</h3>
            <div className="grid grid-cols-7 gap-2">
              {weather.forecast_7day.map((day, i) => (
                <div key={day.date} className="text-center">
                  <p className="text-xs text-gray-500 mb-1">
                    {i === 0 ? 'Today' : new Date(day.date).toLocaleDateString('en', { weekday: 'short' })}
                  </p>
                  <WeatherIcon condition={day.condition} />
                  <p className="text-xs font-semibold text-gray-800 mt-1">{day.max_temp}°</p>
                  <p className="text-xs text-gray-400">{day.min_temp}°</p>
                  {day.precipitation > 0 && (
                    <p className="text-xs text-blue-500 mt-0.5">{day.precipitation}mm</p>
                  )}
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  )
}
