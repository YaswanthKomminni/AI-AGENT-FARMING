'use client'

const LANGUAGES = [
  'English', 'Hindi', 'Tamil', 'Telugu', 'Kannada',
  'Bengali', 'Marathi', 'Gujarati', 'Punjabi', 'Malayalam',
]

export default function LanguageSelector({
  value,
  onChange,
}: {
  value: string
  onChange: (lang: string) => void
}) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="bg-green-800 text-white text-xs px-2 py-1.5 rounded-lg border border-green-600 focus:outline-none focus:ring-1 focus:ring-green-400 cursor-pointer"
    >
      {LANGUAGES.map((lang) => (
        <option key={lang} value={lang}>
          {lang}
        </option>
      ))}
    </select>
  )
}
