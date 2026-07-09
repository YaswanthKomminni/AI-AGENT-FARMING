'use client'
import { useState, useEffect } from 'react'
import { getWeatherByCity, type WeatherData } from '@/lib/api'
import { 
  Sun, CloudSun, Cloud, CloudFog, CloudRain, CloudLightning, CloudSnow, 
  Thermometer, Droplets, Wind, Sprout, Calendar, AlertTriangle, Loader2 
} from 'lucide-react'

const CITIES = [
  'Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Kolkata',
  'Hyderabad', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow',
  'Patna', 'Bhopal', 'Nagpur', 'Chandigarh', 'Indore',
]

interface WeatherIconProps {
  condition: string
  className?: string
}

function WeatherIcon({ condition, className = "w-6 h-6 text-emerald-600" }: WeatherIconProps) {
  switch (condition) {
    case 'Clear sky':
      return <Sun className={`${className} text-amber-500`} />
    case 'Mainly clear':
    case 'Partly cloudy':
      return <CloudSun className={`${className} text-emerald-500`} />
    case 'Overcast':
      return <Cloud className={`${className} text-slate-500`} />
    case 'Fog':
      return <CloudFog className={`${className} text-slate-400`} />
    case 'Light drizzle':
    case 'Moderate drizzle':
    case 'Heavy drizzle':
    case 'Slight rain':
    case 'Moderate rain':
      return <CloudRain className={`${className} text-blue-500`} />
    case 'Heavy rain':
    case 'Thunderstorm':
      return <CloudLightning className={`${className} text-blue-600`} />
    case 'Slight snow':
      return <CloudSnow className={`${className} text-sky-400`} />
    default:
      return <Thermometer className={`${className} text-orange-500`} />
  }
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
    <div className="space-y-4 animate-slide-up">
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
        <div className="card-premium rounded-2xl p-12 text-center flex flex-col items-center justify-center">
          <Loader2 className="w-8 h-8 text-emerald-600 animate-spin mb-2" />
          <p className="text-gray-500 text-sm font-medium">Loading weather data…</p>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-2xl p-4 text-red-600 text-sm flex items-center gap-2">
          <AlertTriangle className="w-4 h-4" />
          <span>{error}</span>
        </div>
      )}

      {weather && !loading && (
        <>
          {/* Current conditions */}
          <div className="bg-gradient-to-br from-emerald-800 to-teal-800 text-white rounded-2xl shadow-md p-6">
            <div className="flex justify-between items-start">
              <div>
                <h2 className="text-2xl font-bold tracking-tight">
                  {weather.city || selectedCity}
                </h2>
                <p className="text-emerald-200 text-sm font-medium">{weather.current.condition}</p>
                <div className="mt-4 flex items-end gap-2">
                  <span className="text-6xl font-light">{weather.current.temperature_2m}°</span>
                  <span className="text-lg mb-2">C</span>
                </div>
                <p className="text-emerald-200 text-xs mt-1">Feels like {weather.current.apparent_temperature}°C</p>
              </div>
              <WeatherIcon condition={weather.current.condition} className="w-12 h-12 text-white" />
            </div>

            <div className="grid grid-cols-3 gap-4 mt-6 pt-4 border-t border-emerald-700/50">
              <div className="text-center">
                <p className="text-emerald-200 text-xs flex items-center justify-center gap-1">
                  <Droplets className="w-3.5 h-3.5" /> Humidity
                </p>
                <p className="font-bold text-sm mt-1">{weather.current.relative_humidity_2m}%</p>
              </div>
              <div className="text-center">
                <p className="text-emerald-200 text-xs flex items-center justify-center gap-1">
                  <CloudRain className="w-3.5 h-3.5" /> Rain
                </p>
                <p className="font-bold text-sm mt-1">{weather.current.precipitation} mm</p>
              </div>
              <div className="text-center">
                <p className="text-emerald-200 text-xs flex items-center justify-center gap-1">
                  <Wind className="w-3.5 h-3.5" /> Wind
                </p>
                <p className="font-bold text-sm mt-1">{weather.current.wind_speed_10m} km/h</p>
              </div>
            </div>
          </div>

          {/* Farming Advisories */}
          {weather.farming_advisory.length > 0 && (
            <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4 flex items-start gap-3">
              <Sprout className="w-5 h-5 text-amber-700 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-bold text-amber-800 text-sm mb-2">Farming Advisories</h3>
                <ul className="space-y-2">
                  {weather.farming_advisory.map((adv, i) => (
                    <li key={i} className="text-xs text-amber-900 flex items-start gap-1.5">
                      <span className="flex-shrink-0 mt-0.5">•</span>
                      <span>{adv}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {/* 7-day forecast */}
          <div className="card-premium rounded-2xl p-5">
            <h3 className="font-bold text-gray-800 text-sm mb-3 flex items-center gap-2">
              <Calendar className="w-4 h-4 text-emerald-600" />
              7-Day Forecast
            </h3>
            <div className="grid grid-cols-7 gap-2 overflow-x-auto">
              {weather.forecast_7day.map((day, i) => (
                <div key={day.date} className="text-center min-w-[50px] flex flex-col items-center">
                  <p className="text-[10px] text-gray-500 mb-1 font-medium">
                    {i === 0 ? 'Today' : new Date(day.date).toLocaleDateString('en', { weekday: 'short' })}
                  </p>
                  <WeatherIcon condition={day.condition} className="w-5 h-5 my-1" />
                  <p className="text-xs font-semibold text-gray-800 mt-1">{day.max_temp}°</p>
                  <p className="text-[10px] text-gray-400">{day.min_temp}°</p>
                  {day.precipitation > 0 && (
                    <p className="text-[9px] text-blue-500 mt-0.5 font-medium">{day.precipitation}mm</p>
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
