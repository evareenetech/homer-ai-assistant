import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import homerLogo from '../assets/HOMER-logo.png'

// ── Square border component — renders a row of decorative squares ──
function SquareBorder() {
  const squareSize = 40
  const gap        = 24
  const count      = Math.ceil(window.innerWidth / (squareSize + gap)) + 1

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

export default function WelcomePage() {
  const navigate = useNavigate()

  // ── Page state ──
  const [visible, setVisible] = useState(false)
  const [hovered, setHovered] = useState(false)

  // ── Responsive breakpoint detection ──
  // Landscape mobile: phone held horizontally, height ≤ 480px
  const [isLandscapeMobile, setIsLandscapeMobile] = useState(
    window.innerWidth > window.innerHeight && window.innerHeight <= 480
  )

  // ── Update isLandscapeMobile on resize or orientation change ──
  useEffect(() => {
    const handle = () => {
      setTimeout(() => {
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

  // ── Fade in on mount ──
  useEffect(() => {
    const timer = setTimeout(() => setVisible(true), 100)
    return () => clearTimeout(timer)
  }, [])

  // ── Handle enter button — fade out then navigate to chat ──
  const handleEnter = () => {
    setVisible(false)
    setTimeout(() => navigate('/chat'), 400)
  }

  return (
    <div
      className="relative w-full h-full overflow-hidden flex flex-col"
      style={{ backgroundColor: '#ead7b8' }}
    >

      {/* ── Top square border — height adjusts per breakpoint ── */}
      <div
        className="relative z-10 overflow-hidden"
        style={{ 
          height:     window.innerWidth <= 480 && window.innerHeight > window.innerWidth ? '60px' : isLandscapeMobile ? '60px' : '100px',
          display:    'flex', 
          alignItems: 'center' 
        }}
      >
        <SquareBorder />
      </div>

      {/* ── Main content — logo and enter button, vertically centered ── */}
      <div
        className="relative z-10 flex flex-col items-center justify-center
          flex-1 px-6"
        style={{
          opacity:    visible ? 1 : 0,
          transform:  visible ? 'translateY(0)' : 'translateY(16px)',
          transition: 'opacity 0.5s ease, transform 0.5s ease',
        }}
      >
        {/* ── HOMER logo — replaces text title and subtitle ── */}
        <img
          src={homerLogo}
          alt="HOMER — Oracle of Ancient Greece"
          style={{
            width:        'clamp(280px, 55vw, 900px)',
            height:       'auto',
            marginBottom: 'clamp(16px, 4vh, 40px)',
          }}
        />

        {/* ── Enter button — navigates to chat page ── */}
        <button
          onClick={handleEnter}
          onMouseEnter={() => setHovered(true)}
          onMouseLeave={() => setHovered(false)}
          style={{
            fontFamily:    '"Cinzel", serif',
            fontSize:      '13px',
            fontWeight:    600,
            letterSpacing: '0.2em',
            color:         '#bb753c',
            background:    '#dfa644',
            borderRadius:  '999px',
            padding:       '10px 36px',
            cursor:        'pointer',
            transition:    'background 0.3s ease, transform 0.2s ease',
            transform:     hovered ? 'translateY(-2px)' : 'translateY(0)',
            border:        'none',
          }}
        >
          ENTER THE ORACLE
        </button>
      </div>

      {/* ── Bottom square border — height adjusts per breakpoint ── */}
      <div
        className="relative z-10 overflow-hidden"
        style={{ 
          height:     window.innerWidth <= 480 && window.innerHeight > window.innerWidth ? '60px' : isLandscapeMobile ? '60px' : '100px',
          display:    'flex', 
          alignItems: 'center' 
        }}
      >
        <SquareBorder />
      </div>

    </div>
  )
}