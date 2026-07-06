'use client'
import { useState, useRef } from 'react'

const STT_LANG_CODES: Record<string, string> = {
  Hindi: 'hi-IN', Tamil: 'ta-IN', Telugu: 'te-IN',
  Kannada: 'kn-IN', Bengali: 'bn-IN', Marathi: 'mr-IN',
  Gujarati: 'gu-IN', Punjabi: 'pa-IN', Malayalam: 'ml-IN',
  English: 'en-IN',
}

interface VoiceInputProps {
  language: string
  onResult: (text: string) => void
}

export default function VoiceInput({ language, onResult }: VoiceInputProps) {
  const [listening, setListening] = useState(false)
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const recognitionRef = useRef<any>(null)

  const toggle = () => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const SR: any =
      (typeof window !== 'undefined' &&
        ((window as any).SpeechRecognition || (window as any).webkitSpeechRecognition)) ||
      null

    if (!SR) {
      alert('Voice input is not supported in this browser. Please use Chrome.')
      return
    }

    if (listening) {
      recognitionRef.current?.stop()
      setListening(false)
      return
    }

    const recognition = new SR()
    recognition.lang = STT_LANG_CODES[language] || 'en-IN'
    recognition.continuous = false
    recognition.interimResults = false

    recognition.onstart  = () => setListening(true)
    recognition.onend    = () => setListening(false)
    recognition.onerror  = () => setListening(false)
    recognition.onresult = (event: any) => {
      const text = event.results[0][0].transcript
      onResult(text)
    }

    recognitionRef.current = recognition
    recognition.start()
  }

  return (
    <button
      onClick={toggle}
      title={listening ? 'Stop listening' : `Start voice input (${language})`}
      className={`p-2.5 rounded-xl transition-all ${
        listening
          ? 'bg-red-500 text-white animate-pulse'
          : 'bg-gray-100 text-gray-500 hover:bg-green-100 hover:text-green-700'
      }`}
    >
      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
        <path
          fillRule="evenodd"
          d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z"
          clipRule="evenodd"
        />
      </svg>
    </button>
  )
}
