import { useState, useEffect, useRef } from 'react'
import { useLocation } from 'react-router-dom'
import { homerApi } from '../services/api'
import UserInput from '../components/UserInput'
import welcomeQuote from '../assets/welcome-quote.png'
import { useNavigate } from 'react-router-dom'
import iconTree from '../assets/icon-tree.jpeg'


function MessageBubble({ message }) {
  const isHomer = message.role === 'assistant'

  // ── Bubble style — glass effect for user messages and desktop Homer ──
  const bubbleStyle = {
    backdropFilter:       'blur(16px)',
    WebkitBackdropFilter: 'blur(16px)',
    borderRadius:         '20px',
    background:           'rgba(255, 248, 220, 0.4)',
    border:               '1px solid rgba(184, 135, 11, 0)',
    boxShadow:            '0 4px 16px rgba(0,0,0,0.07)',
  }

  // ── Detect mobile portrait for bubble styling ──
  const isMobile = window.innerWidth <= 480

  return (
    // ── Message row — Homer left, user right ──
    <div className={`flex items-start gap-3 mb-5
      ${isHomer ? 'justify-start' : 'justify-end'}`}>

      {/* Homer messages on mobile have no bubble — plain text only */}
      <div
        className="px-5 py-4"
        style={{
          ...(isHomer && isMobile ? {} : bubbleStyle),
          maxWidth: isMobile ? '100%' : '42rem',
        }}
      >
        {/* ── Typing indicator — shown while Homer is composing ── */}
        {isHomer && message.content === '' ? (
          <div className="flex items-center gap-2">
            <span className="font-crimson italic text-base text-amber-900">
              Homer is composing
            </span>
            <span className="flex gap-1">
              {[0, 1, 2].map(i => (
                <span
                  key={i}
                  className="w-1.5 h-1.5 rounded-full bg-gold-light"
                  style={{
                    animation: `bounce 1.2s ease-in-out ${i * 0.2}s infinite`
                  }}
                />
              ))}
            </span>
            <style>{`
              @keyframes bounce {
                0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
                40% { transform: translateY(-5px); opacity: 1; }
              }
            `}</style>
          </div>
        ) : (
          // ── Message text — slightly smaller on mobile ──
          <p className="font-crimson leading-relaxed whitespace-pre-wrap text-amber-900"
            style={{ fontSize: window.innerWidth <= 480 ? '0.95rem' : '1rem' }}>
            {message.content}
          </p>
        )}

        {/* ── Citations — shown below Homer's message when available ── */}
        {isHomer && message.citations && message.citations.length > 0 && (
          <p
            className="mt-3 pt-2 font-crimson italic text-sm"
            style={{
              borderTop: '1px solid rgba(184,134,11,0.2)',
              color:     'rgba(120,80,20,0.6)',
            }}
          >
            Sources: {message.citations.join(' · ')}
          </p>
        )}
      </div>
    </div>
  )
}

// ── Square border component — renders a row of squares ──
function SquareBorder({ availableWidth }) {
  const squareSize = 40
  const gap        = 24
  const count      = Math.ceil(availableWidth / (squareSize + gap)) + 1

  return (
    <div className="flex items-center" style={{ gap: `${gap}px` }}>
      {Array.from({ length: count }).map((_, i) => (
        <div
          key={i}
          style={{
            width:           squareSize,
            height:          squareSize,
            minWidth:        squareSize,
            backgroundColor: '#708b94',
          }}
        />
      ))}
    </div>
  )
}

export default function ChatPage() {
  // ── Chat state ──
  const [messages,   setMessages]   = useState([])
  const [isLoading,  setIsLoading]  = useState(false)
  const [sessionId,  setSessionId]  = useState(null)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [visible,    setVisible]    = useState(false)

  // ── Responsive breakpoint detection ──
  // Portrait mobile: phone held vertically, width ≤ 480px
  const [isPortraitMobile,  setIsPortraitMobile]  = useState(
    window.innerWidth <= 480 && window.innerHeight > window.innerWidth
  )
  // Landscape mobile: phone held horizontally, height ≤ 480px
  const [isLandscapeMobile, setIsLandscapeMobile] = useState(
    window.innerWidth > window.innerHeight && window.innerHeight <= 480
  )

  const navigate     = useNavigate()
  const bottomRef    = useRef(null)
  const location     = useLocation()
  const hasAutoSent  = useRef(false)
  const streamingIdx = useRef(-1)

  // ── Fade in on mount ──
  useEffect(() => {
    const t = setTimeout(() => setVisible(true), 50)
    return () => clearTimeout(t)
  }, [])

  // ── Update breakpoint states on resize or orientation change ──
  useEffect(() => {
    const handle = () => {
      setTimeout(() => {
        setIsPortraitMobile(window.innerWidth <= 480 && window.innerHeight > window.innerWidth)
        setIsLandscapeMobile(window.innerWidth > window.innerHeight && window.innerHeight <= 480)
      }, 100)
    }
    window.addEventListener('resize', handle)
    window.addEventListener('orientationchange', handle)
    return () => {
      window.removeEventListener('resize', handle)
      window.removeEventListener('orientationchange', handle)
    }
  }, [])

  // ── Auto scroll to latest message ──
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // ── Auto send message if redirected from family tree page ──
  useEffect(() => {
    const params = new URLSearchParams(location.search)
    const ask    = params.get('ask')
    if (ask && !hasAutoSent.current) {
      hasAutoSent.current = true
      window.history.replaceState({}, '', '/chat')
      setTimeout(() => handleSend(`Tell me about ${ask}`), 100)
    }
  }, [])

  // ── Handle sending a message to Homer via streaming API ──
  const handleSend = (message) => {
    if (isLoading) return

    // Add user message and empty Homer placeholder immediately
    setMessages(prev => [
      ...prev,
      { role: 'user',      content: message, citations: [] },
      { role: 'assistant', content: '',       citations: [] },
    ])

    setIsLoading(true)
    setIsSpeaking(false)

    setMessages(prev => {
      streamingIdx.current = prev.length - 1
      return prev
    })

    homerApi.chatStream(
      message,
      sessionId,

      // ── On each streamed token — append to Homer's message ──
      (token) => {
        setIsLoading(false)
        setIsSpeaking(true)
        setMessages(prev => {
          const idx = prev.length - 1
          if (idx < 0 || prev[idx].role !== 'assistant') return prev
          const updated = [...prev]
          updated[idx] = {
            ...updated[idx],
            content: updated[idx].content + token
          }
          return updated
        })
      },

      // ── On stream complete — attach citations and session id ──
      (citations, newSessionId) => {
        setIsLoading(false)
        setMessages(prev => {
          const idx = prev.length - 1
          if (idx < 0 || prev[idx].role !== 'assistant') return prev
          const updated = [...prev]
          updated[idx] = {
            ...updated[idx],
            citations: citations || []
          }
          return updated
        })
        if (newSessionId) setSessionId(newSessionId)
        setTimeout(() => setIsSpeaking(false), 3000)
      },

      // ── On error — show fallback message ──
      (error) => {
        console.error('[Chat error]', error)
        setIsLoading(false)
        setMessages(prev => {
          const idx = prev.length - 1
          if (idx < 0 || prev[idx].role !== 'assistant') return prev
          const updated = [...prev]
          updated[idx] = {
            ...updated[idx],
            content: updated[idx].content.trim()
              ? updated[idx].content
              : 'The oracle is silent... Please ensure the backend is running.',
            citations: []
          }
          return updated
        })
      }
    )
  }

  // ── Show welcome quote when no messages yet ──
  const showWelcome = messages.length === 0 && !isLoading

  return (
    <div
      className="relative w-full h-full overflow-hidden"
      style={{ opacity: visible ? 1 : 0, transition: 'opacity 0.4s ease' }}
    >
      {/* ── Background — parchment color ── */}
      <div
        className="absolute inset-0"
        style={{ backgroundColor: '#ead7b8' }}
      />

      {/* ── Family tree nav button — top right corner ── */}
      <button
        onClick={() => navigate('/family-tree')}
        title="View Family Tree"
        className="absolute z-50 flex items-center justify-center
          rounded-full transition-all duration-200 hover:scale-110 active:scale-95"
        style={{
          top:   isPortraitMobile ? '5px' : isLandscapeMobile ? '5px' : '20px',
          right: isPortraitMobile ? '5px' : isLandscapeMobile ? '5px' : '16px',
        }}
      >
        <img
          src={iconTree}
          alt="View Family Tree"
          style={{
            width:     isPortraitMobile ? 52 : isLandscapeMobile ? 52 : 60,
            height:    isPortraitMobile ? 52 : isLandscapeMobile ? 52 : 60,
            objectFit: 'contain',
          }}
        />
      </button>

      {/* ── Main layout — full height flex column ── */}
      <div className="relative z-10 flex h-full flex-cb"
              style={{
                paddingTop: '5rem',
              }}>

        {/* ── Chat area — scrollable messages + input bar ── */}
        <div className="flex flex-col flex-1 h-full"
          style={{
            paddingLeft:  isPortraitMobile ? '0px' : window.innerWidth <= 480 ? '16px' : '8px',
            paddingRight: isPortraitMobile ? '0px' : '0px',
          }}>

          {/* ── Scrollable message list ── */}
          <div className="flex-1 overflow-y-auto px-4"
              style={{
                paddingTop:    isPortraitMobile ? '0px' : window.innerWidth <= 480 ? '20px' : '20px',
                paddingBottom: '100px',
              }}>

            {/* ── Welcome quote image — shown before first message ── */}
            {showWelcome && (
              <div
                className="absolute inset-0 flex items-center justify-center
                  pointer-events-none"
              >
                <img
                  src={welcomeQuote}
                  alt="What wisdom do you seek from the depths of antiquity?"
                  style={{
                    width:  'clamp(400px, 55vw, 800px)',
                    height: 'auto',
                  }}
                />
              </div>
            )}

            {/* ── Message bubbles — constrained to centered column on desktop ── */}
            <div style={{
              width:       window.innerWidth >= 1025 ? '55%' : '100%',
              marginLeft:  window.innerWidth >= 1025 ? 'auto' : '0',
              marginRight: window.innerWidth >= 1025 ? 'auto' : '0',
            }}>
              {messages.map((msg, i) => (
                <MessageBubble key={i} message={msg} />
              ))}
            </div>

            {/* ── Scroll anchor — auto scrolls to latest message ── */}
            <div ref={bottomRef} />
          </div>

          {/* ── Input bar — centered, responsive width ── */}
          <div className={isPortraitMobile ? 'pb-16 pt-2 flex justify-center' : 'pb-6 pt-2 flex justify-center'}
            style={{
              paddingLeft:   isPortraitMobile ? '52px' : '0',
              paddingRight:  isPortraitMobile ? '52px' : '0',
              paddingBottom: isPortraitMobile ? '10px' : isLandscapeMobile ? '5px' : '24px',
            }}
          >
            <div style={{ width: isPortraitMobile ? '100%' : window.innerWidth >= 1025 ? '55%' : '75%' }}>
              <UserInput
                onSend={handleSend}
                isLoading={isLoading}
              />
            </div>
          </div>
        </div>
      </div>

      {/* ── Left square strip — flanks the input bar on the left ── */}
      <div
        className="absolute z-0 overflow-hidden pointer-events-none"
        style={{
          bottom:     isPortraitMobile ? '0px' : isLandscapeMobile ? '5px' : '24px',
          left:       0,
          width:      window.innerWidth <= 480 && window.innerHeight > window.innerWidth ? '52px' : 'calc(27.5%)',
          height:     isPortraitMobile ? '70px' : '52px',
          display:    'flex',
          alignItems: 'center',
        }}
      >
        <SquareBorder availableWidth={window.innerWidth <= 480 && window.innerHeight > window.innerWidth ? 40 : window.innerWidth * 0.30} />
      </div>

      {/* ── Right square strip — flanks the input bar on the right ── */}
      <div
        className="absolute z-0 overflow-hidden pointer-events-none"
        style={{
          bottom:         isPortraitMobile ? '0px' : isLandscapeMobile ? '5px' : '24px',
          right:          0,
          width:          window.innerWidth <= 480 && window.innerHeight > window.innerWidth ? '52px' : 'calc(27.5%)',
          height:         isPortraitMobile ? '70px' : '52px',
          display:        'flex',
          alignItems:     'center',
          justifyContent: 'flex-end',
        }}
      >
        <SquareBorder availableWidth={window.innerWidth <= 480 && window.innerHeight > window.innerWidth ? 40 : window.innerWidth * 0.30} />
      </div>

      {/* ── Top square strip — full width decorative border ── */}
      <div
        className="absolute z-0 overflow-hidden pointer-events-none"
        style={{
          top:        window.innerWidth <= 480 && window.innerHeight > window.innerWidth ? '0px' : window.innerWidth > window.innerHeight && window.innerHeight <= 480 ? '10px' : '24px',
          left:       0,
          right:      0,
          height:     window.innerWidth <= 480 && window.innerHeight > window.innerWidth ? '60px' : window.innerWidth > window.innerHeight && window.innerHeight <= 480 ? '40px' : '52px',
          display:    'flex',
          alignItems: 'center',
        }}
      >
        <SquareBorder availableWidth={window.innerWidth} />
      </div>

    </div>
  )
}