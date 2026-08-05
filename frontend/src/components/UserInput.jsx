import { useState, useRef } from 'react'

export default function UserInput({ onSend, isLoading }) {
  const [message, setMessage] = useState('')
  const inputRef = useRef(null)

  const handleSend = () => {
    const trimmed = message.trim()
    if (!trimmed || isLoading) return
    onSend(trimmed)
    setMessage('')
    inputRef.current?.focus()
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div
      className="flex items-center gap-2 px-4 py-3 rounded-full"
      onClick={() => inputRef.current?.focus()}
      style={{
        background:           '#dfa644',
        backdropFilter:       'blur(16px)',
        WebkitBackdropFilter: 'blur(16px)',
        border:               'none',
        boxShadow:            'none',
        cursor:               'text',
      }}
    >
      <input
        ref={inputRef}
        type="text"
        value={message}
        onChange={e => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask Homer about the Greek Mythology..."
        disabled={isLoading}
        className="flex-1 bg-transparent outline-none font-crimson text-lg
          italic placeholder:italic placeholder:text-amber-700"
        style={{
          color:          '#bb753c',
          caretColor:     '#bb753c',
          pointerEvents:  'auto',
        }}
      />

      
    </div>
  )
}