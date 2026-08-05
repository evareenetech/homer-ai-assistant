import { CATEGORY_COLORS } from '../constants/categoryColors'

export default function FigureInfoPanel({ figure, onClose, onAskHomer }) {
  const accentColor = CATEGORY_COLORS[figure.category]?.fill || CATEGORY_COLORS.mortal.fill
  const isAphrodite = figure.name === 'Aphrodite'

  const RelationList = ({ title, items }) => {
    if (!items || items.length === 0) return null
    return (
      <div className="mb-4">
        <p
          className="font-cinzel text-xs tracking-wider mb-2"
          style={{ color: '#bb753c' }}
        >
          {title}
        </p>
        <div className="flex flex-wrap gap-2">
          {items.map(item => (
            <span
              key={item.name}
              className="font-crimson text-sm px-2 py-1 rounded cursor-default"
              style={{
                border:     '1px solid rgba(184,134,11,0.2)',
                color:      '#7a4a1e',
                background: 'rgba(0,0,0,0.05)',
              }}
            >
              {item.name}
            </span>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div
      className="absolute top-0 right-0 h-full w-80 z-50 flex flex-col
        overflow-hidden shadow-2xl"
      style={{
        background:           'rgba(255, 248, 220, 0.55)',
        backdropFilter:       'blur(12px)',
        WebkitBackdropFilter: 'blur(12px)',
        borderLeft:           `2px solid ${accentColor}`,
        animation:            'slideIn 0.3s ease forwards',
      }}
    >
      <style>{`
        @keyframes slideIn {
          from { transform: translateX(100%); opacity: 0; }
          to   { transform: translateX(0);    opacity: 1; }
        }
      `}</style>

      {/* Header */}
      <div
        className="flex items-start justify-between p-5 pb-3"
        style={{ borderBottom: `1px solid ${accentColor}50` }}
      >
        <div>
          <h2
            className="font-cinzel font-bold text-xl tracking-wider"
            style={{ color: '#bb753c' }}
          >
            {figure.name.toUpperCase()}
          </h2>
          <span
            className="font-crimson italic text-sm capitalize"
            style={{ color: accentColor }}
          >
            {figure.category.replace('_', ' ')}
          </span>
        </div>

        <button
          onClick={onClose}
          className="w-8 h-8 rounded-full flex items-center justify-center
            transition-all hover:scale-110 text-lg"
          style={{ color: '#7a4a1e' }}
        >
          ✕
        </button>
      </div>

      {/* Scrollable content */}
      <div className="flex-1 overflow-y-auto p-5 space-y-1">

        {/* Description */}
        <p
          className="font-crimson text-base leading-relaxed mb-4"
          style={{ color: '#7a4a1e' }}
        >
          {figure.description}
        </p>

        {/* Aphrodite — dual parentage note */}
        {isAphrodite && (
          <div
            className="mb-4 p-3 rounded-xl"
            style={{
              background: 'rgba(184,134,11,0.1)',
              border:     '1px solid rgba(184,134,11,0.25)',
            }}
          >
            <p
              className="font-cinzel text-xs mb-2"
              style={{ color: '#bb753c' }}
            >
              TWO TRADITIONS
            </p>
            <p
              className="font-crimson text-sm leading-relaxed"
              style={{ color: '#7a4a1e' }}
            >
              <span style={{ fontWeight: 'bold' }}>Hesiod</span> — Born from
              the sea foam when Uranus was cast into the sea. Daughter of
              Uranus with no mother.
            </p>
            <p
              className="font-crimson text-sm leading-relaxed mt-1"
              style={{ color: '#7a4a1e' }}
            >
              <span style={{ fontWeight: 'bold' }}>Homer</span> — Daughter
              of Zeus and the Titaness Dione.
            </p>
          </div>
        )}

        {/* Family relationships */}
        <RelationList title="PARENTS"  items={figure.parents}  />
        <RelationList title="CHILDREN" items={figure.children} />
        <RelationList title="SIBLINGS" items={figure.siblings} />
        <RelationList title="SPOUSE"   items={figure.spouses}  />

        {/* Classical source */}
        <div
          className="mt-4 pt-3 font-crimson italic text-sm"
          style={{
            borderTop: `1px solid ${accentColor}30`,
            color:     '#7a4a1e',
            opacity:   0.7,
          }}
        >
          Source: {figure.source}
          {isAphrodite && (
            <span
              className="block mt-1 font-crimson italic text-sm"
              style={{ color: '#7a4a1e', opacity: 0.7 }}
            >
              Also: Homer — Iliad (Zeus and Dione tradition)
            </span>
          )}
        </div>
      </div>

      {/* Ask Homer button */}
      <div
        className="p-5 pt-3"
        style={{ borderTop: `1px solid ${accentColor}30` }}
      >
        <button
          onClick={() => onAskHomer(figure.name)}
          className="w-full font-cinzel text-xs tracking-widest py-3
            rounded-full transition-all duration-300
            hover:scale-105 active:scale-95"
          style={{
            color:      '#f3e9d9',
            boxShadow:  '0 4px 24px rgba(0,0,0,0.1)',
            background: accentColor,
          }}
        >
          ASK HOMER ABOUT {figure.name.toUpperCase()}
        </button>
      </div>
    </div>
  )
}