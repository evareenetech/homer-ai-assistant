import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import * as d3 from 'd3'
import { homerApi } from '../services/api'
import FigureInfoPanel from '../components/FigureInfoPanel'
import iconOracle from '../assets/icon-oracle.jpeg'
import { CATEGORY_COLORS } from '../constants/categoryColors'

// ── Views — each view defines a family tree perspective ──

const VIEWS = [
  {
    id:         'chaos_lineage',
    label:      'Divine Lineage',
    desc:       'From Chaos to the Olympians',
    categories: ['primordial', 'titan', 'olympian', 'underworld', 'minor_god'],
    rootNode:   'Chaos',
    arrowFill:  '#e7b85a',
    arrowStroke:'#c48a5a',
    titleColor: '#e7b85a',
    descColor:  '#c48a5a',
  },
  {
    id:         'titans',
    label:      'Titans',
    desc:       'The elder gods of the cosmos',
    categories: ['primordial', 'titan', 'minor_god'],
    rootNode:   'Chaos',
    arrowFill:  '#7a3d26',
    arrowStroke:'#c48a5a',
    titleColor: '#c48a5a',
    descColor:  '#8c4b2b',
  },
  {
    id:         'olympians',
    label:      'Olympians',
    desc:       'The twelve gods of Olympus',
    categories: ['olympian', 'titan', 'underworld', 'minor_god'],
    rootNode:   'Zeus',
    arrowFill:  '#9fb8c0',
    arrowStroke:'#3f525a',
    titleColor: '#9fb8c0',
    descColor:  '#718b95',
  },
  {
    id:         'minor_gods',
    label:      'Minor Gods',
    desc:       'The lesser deities of the pantheon',
    categories: ['minor_god', 'olympian', 'titan'],
    rootNode:   'Ares',
    arrowFill:  '#8c4b2b',
    arrowStroke:'#c48a5a',
    titleColor: '#c48a5a',
    descColor:  '#8c4b2b',
  },
  {
    id:         'muses',
    label:      'Muses',
    desc:       'The nine goddesses of inspiration',
    categories: ['muse', 'titan', 'olympian'],
    rootNode:   'Zeus',
    arrowFill:  '#897477',
    arrowStroke:'#7e5a54',
    titleColor: '#897477',
    descColor:  '#7e5a54',
  },
  {
    id:         'nymphs',
    label:      'Nymphs',
    desc:       'The divine spirits of nature',
    categories: ['nymph', 'primordial', 'titan', 'olympian'],
    rootNode:   'Nereus',
    arrowFill:  '#c48a5a',
    arrowStroke:'#8c4b2b',
    titleColor: '#c48a5a',
    descColor:  '#8c4b2b',
  },
  {
    id:         'heroes',
    label:      'Heroes',
    desc:       'The great mortal champions',
    categories: ['hero', 'mortal', 'nymph', 'olympian'],
    rootNode:   'Zeus',
    arrowFill:  '#cfae6d',
    arrowStroke:'#8c4b2b',
    titleColor: '#8c4b2b',
    descColor:  '#8c4b2b',
  },
]

// ── renderTree — builds the D3 SVG family tree ──
function renderTree({ svgEl, nodes, edges, selected, onNodeClick, rootNode, categories, viewId }) {
  d3.select(svgEl).selectAll('*').remove()

  const colors = CATEGORY_COLORS

  // ── Filter nodes by category, then include parents of visible nodes ──
  const visibleIds = new Set(
    nodes.filter(n => categories.includes(n.category)).map(n => n.id)
  )

  const parentEdges = edges.filter(e => e.relationship === 'parent')
  parentEdges.forEach(e => {
    if (visibleIds.has(e.target)) visibleIds.add(e.source)
  })

  const visibleNodes = nodes.filter(n => visibleIds.has(n.id))
  const visibleEdges = parentEdges.filter(
    e => visibleIds.has(e.source) && visibleIds.has(e.target)
  )

  // ── Build child and parent maps for depth calculation ──
  const childMap  = {}
  const parentMap = {}
  visibleNodes.forEach(n => { childMap[n.id] = []; parentMap[n.id] = [] })
  visibleEdges.forEach(e => {
    if (childMap[e.source])  childMap[e.source].push(e.target)
    if (parentMap[e.target]) parentMap[e.target].push(e.source)
  })

  // ── Find root nodes — nodes with no parents ──
  let roots
  if (rootNode && visibleIds.has(rootNode)) {
    roots = [rootNode]
  } else {
    roots = visibleNodes.filter(n => parentMap[n.id].length === 0).map(n => n.id)
  }

  // ── BFS to calculate depth of each node ──
  const depth = {}
  const queue = [...roots]
  roots.forEach(r => (depth[r] = 0))
  while (queue.length) {
    const cur = queue.shift()
    ;(childMap[cur] || []).forEach(child => {
      if (depth[child] === undefined) {
        depth[child] = depth[cur] + 1
        queue.push(child)
      }
    })
  }
  visibleNodes.forEach(n => { if (depth[n.id] === undefined) depth[n.id] = 0 })

  // ── Group nodes by depth level ──
  const levels = {}
  visibleNodes.forEach(n => {
    const d = depth[n.id]
    if (!levels[d]) levels[d] = []
    levels[d].push(n)
  })

  // ── Node dimensions and spacing ──
  const nodeW    = 110
  const nodeH    = 38
  const levelGap = 90
  const nodeGap  = 14

  // ── Calculate default positions — centered per level ──
  const positions = {}
  Object.entries(levels).forEach(([lvl, lvlNodes]) => {
    const totalW = lvlNodes.length * nodeW + (lvlNodes.length - 1) * nodeGap
    lvlNodes.forEach((n, i) => {
      positions[n.id] = {
        x: i * (nodeW + nodeGap) - totalW / 2 + nodeW / 2,
        y: parseInt(lvl) * (nodeH + levelGap),
      }
    })
  })

  // ── Apply custom row layout — overrides default positions ──
  function applyCustomLayout(allRows) {
    const allNames = new Set(allRows.flat())
    ;[...visibleIds].forEach(id => {
      if (!allNames.has(id)) visibleIds.delete(id)
    })
    const filteredNodes = visibleNodes.filter(n => allNames.has(n.id))
    const filteredEdges = visibleEdges.filter(
      e => allNames.has(e.source) && allNames.has(e.target)
    )
    Object.keys(positions).forEach(k => delete positions[k])
    const fixedNodeGap = 14
    allRows.forEach((row, rowIdx) => {
      const totalW = row.length * nodeW + (row.length - 1) * fixedNodeGap
      row.forEach((name, i) => {
        positions[name] = {
          x: i * (nodeW + fixedNodeGap) - totalW / 2 + nodeW / 2,
          y: rowIdx * (nodeH + levelGap),
        }
      })
    })
    visibleNodes.length = 0
    filteredNodes.forEach(n => visibleNodes.push(n))
    visibleEdges.length = 0
    filteredEdges.forEach(e => visibleEdges.push(e))
  }

  // ── Custom layout: Divine Lineage view ──
  if (viewId === 'chaos_lineage') {
    applyCustomLayout([
      ['Chaos'],
      ['Gaia'],
      ['Uranus'],
      ['Cronus', 'Rhea'],
      ['Aphrodite', 'Poseidon', 'Zeus', 'Hera', 'Demeter', 'Hestia', 'Hades'],
      ['Athena', 'Apollo', 'Artemis', 'Ares', 'Hephaestus', 'Hermes', 'Dionysus', 'Persephone'],
    ])
  }

  // ── Custom layout: Titans view ──
  if (viewId === 'titans') {
    applyCustomLayout([
      ['Chaos'],
      ['Eros', 'Tartarus', 'Gaia', 'Nyx', 'Erebus'],
      ['Uranus'],
      ['Cronus', 'Rhea', 'Oceanus','Tethys', 'Mnemosyne', 'Themis'],
      ['Clymene', 'Iapetus', 'Hyperion', 'Theia', 'Coeus', 'Phoebe'],
      ['Prometheus', 'Epimetheus', 'Atlas', 'Leto', 'Asteria'],
    ])
  }

  // ── Custom layout: Olympians view ──
  if (viewId === 'olympians') {
    applyCustomLayout([
      ['Cronus', 'Rhea'],
      ['Poseidon','Demeter','Zeus', 'Hera', 'Hestia', 'Hades'],
      ['Persephone', 'Ares','Eileithyia', 'Hephaestus', 'Hebe', 'Aphrodite'],
      ['Athena', 'Apollo', 'Artemis', 'Hermes', 'Dionysus','Nike', 'Tyche'],
    ])
  }

  // ── Custom layout: Minor Gods view ──
  if (viewId === 'minor_gods') {
    applyCustomLayout([
      ['Hyperion','Theia'],
      ['Helios', 'Selene', 'Eos'],
      ['Zeus'],
      ['Hebe', 'Eileithyia','Aphrodite', 'Ares', 'Nike', 'Tyche'],
      ['Phobos', 'Deimos','Eros', 'Eris', 'Enyo'],
    ])
  }

  // ── Custom layout: Muses view ──
  if (viewId === 'muses') {
    applyCustomLayout([
      ['Zeus', 'Mnemosyne'],
      ['Calliope', 'Clio', 'Euterpe', 'Melpomene'],
      ['Terpsichore', 'Erato', 'Polyhymnia','Urania', 'Thalia']
    ])
  }

  // ── Custom layout: Nymphs view ──
  if (viewId === 'nymphs') {
    applyCustomLayout([
      ['Oceanus', 'Tethys'],
      ['Styx', 'Eurynome', 'Nereus', 'Doris', 'Calypso'],
      ['Circe','Thetis', 'Amphitrite', 'Galatea', 'Psamathe'],
    ])
  }

  // ── Custom layout: Heroes view ──
  if (viewId === 'heroes') {
    applyCustomLayout([
      ['Alcmene', 'Zeus', 'Danae'],
      ['Heracles', 'Aeacus', 'Perseus'],
      ['Peleus', 'Thetis'],
      ['Achilles'],
    ])
  }

  // ── Calculate content bounding box ──
  const allX     = Object.values(positions).map(p => p.x)
  const allY     = Object.values(positions).map(p => p.y)
  const minX     = Math.min(...allX) - nodeW / 2 - 80
  const maxX     = Math.max(...allX) + nodeW / 2 + 80
  const minY     = Math.min(...allY) - 60
  const maxY     = Math.max(...allY) + nodeH + 80
  const contentW = maxX - minX
  const contentH = maxY - minY

  // ── Get container dimensions for scaling ──
  const container = svgEl.parentElement
  const viewW     = container.clientWidth  || window.innerWidth
  const viewH     = container.clientHeight || window.innerHeight

  // ── Scale multiplier — adjusted per breakpoint ──
  const isMobile        = viewW <= 480
  const isTablet        = viewW <= 1024
  const isLandscapeMode = viewW > viewH && viewH <= 480
  const scaleMult       = isLandscapeMode ? 0.90 : isMobile ? 1.2 : isTablet ? 0.70 : 0.85
  const scale           = Math.min(viewW / contentW, viewH / contentH, 1) * scaleMult

  const svg = d3.select(svgEl)
    .attr('width',  viewW)
    .attr('height', viewH)
    .style('cursor', 'grab')

  // ── Initial position — centers the tree horizontally ──
  const initX = viewW / 2 - (minX + contentW / 2) * scale
  const initY = isMobile ? 20 - minY * scale : 40 - minY * scale

  const g = svg.append('g')

  // ── Zoom behavior — pinch and scroll to zoom ──
  const zoom = d3.zoom()
    .scaleExtent([scale, 3])
    .on('zoom', event => { g.attr('transform', event.transform) })

  svg.call(zoom)
  svg.call(zoom.transform, d3.zoomIdentity.translate(initX, initY).scale(scale))

  // ── Expose zoom controls to window for the zoom buttons ──
  window._homerZoomIn    = () => svg.transition().duration(300).call(zoom.scaleBy, 1.3)
  window._homerZoomOut   = () => svg.transition().duration(300).call(zoom.scaleBy, 0.77)
  window._homerZoomReset = () => svg.transition().duration(400).call(
    zoom.transform, d3.zoomIdentity.translate(initX, initY).scale(scale)
  )

  // ── Find nodes connected to the selected node ──
  const connectedIds = new Set()
  if (selected) {
    visibleEdges.forEach(e => {
      if (e.source === selected) connectedIds.add(e.target)
      if (e.target === selected) connectedIds.add(e.source)
    })
  }

  // ── Draw edges — curved paths between parent and child nodes ──
  visibleEdges.forEach(edge => {
    const s = positions[edge.source]
    const t = positions[edge.target]
    if (!s || !t) return
    const x1   = s.x, y1 = s.y + nodeH / 2
    const x2   = t.x, y2 = t.y - nodeH / 2
    const midY = (y1 + y2) / 2
    const isConnected = selected && (edge.source === selected || edge.target === selected)
    const isUnrelated = selected && !isConnected

    g.append('path')
      .attr('d', `M${x1},${y1} C${x1},${midY} ${x2},${midY} ${x2},${y2}`)
      .attr('fill',         'none')
      .attr('stroke',       isConnected ? 'rgba(139,105,20,0.4)' : isUnrelated ? 'rgba(0,0,0,0.08)' : 'rgba(139,105,20,0.4)')
      .attr('stroke-width', isConnected ? 2.5 : 1.2)
      .attr('opacity',      isUnrelated ? 0.3 : 1)
  })

  // ── Draw nodes — rounded rectangles with category colors ──
  visibleNodes.forEach(node => {
    const pos         = positions[node.id]
    if (!pos) return
    const cat         = colors[node.category] || colors.mortal
    const isSelected  = node.id === selected
    const isRoot      = node.id === rootNode
    const isConnected = connectedIds.has(node.id)
    const isUnrelated = selected && node.id !== selected && !isConnected

    const nodeG = g.append('g')
      .attr('transform', `translate(${pos.x - nodeW / 2}, ${pos.y - nodeH / 2})`)
      .style('cursor', 'pointer')
      .on('click', () => onNodeClick(node.id))

    // ── Outer rectangle ──
    nodeG.append('rect')
      .attr('width',        nodeW)
      .attr('height',       nodeH)
      .attr('rx',           5)
      .attr('fill',         cat.fill)
      .attr('stroke',       cat.stroke)
      .attr('stroke-width', isSelected || isRoot ? 3 : isConnected ? 2 : 1.5)
      .attr('opacity',      isUnrelated ? 0.25 : 0.93)

    // ── Inner rectangle — decorative border inset ──
    nodeG.append('rect')
      .attr('x', 3).attr('y', 3)
      .attr('width',        nodeW - 6)
      .attr('height',       nodeH - 6)
      .attr('rx',           3)
      .attr('fill',         'none')
      .attr('stroke',       cat.stroke)
      .attr('stroke-width', 0.6)
      .attr('opacity',      0.5)

    // ── Node label — figure name in Cinzel font ──
    nodeG.append('text')
      .attr('x',                 nodeW / 2)
      .attr('y',                 nodeH / 2)
      .attr('text-anchor',       'middle')
      .attr('dominant-baseline', 'central')
      .attr('fill',              cat.text)
      .attr('font-family',       'Cinzel, serif')
      .attr('font-size',         node.id.length > 10 ? '8.5px' : '10.5px')
      .attr('font-weight',       isSelected || isConnected ? '700' : '600')
      .attr('letter-spacing',    '0.05em')
      .attr('opacity',           isUnrelated ? 0.3 : 1)
      .text(node.id.toUpperCase())

    nodeG
      .on('mouseover', null)
      .on('mouseout',  null)
  })
}

// ── Square border component — responsive to orientation changes ──
function SquareBorder() {
  const [dimensions, setDimensions] = useState({
    width:  window.innerWidth,
    height: window.innerHeight,
  })

  // ── Update dimensions on resize or orientation change ──
  useEffect(() => {
    const handleResize = () => {
      setTimeout(() => {
        setDimensions({
          width:  window.innerWidth,
          height: window.innerHeight,
        })
      }, 100)
    }
    window.addEventListener('resize', handleResize)
    window.addEventListener('orientationchange', handleResize)
    return () => {
      window.removeEventListener('resize', handleResize)
      window.removeEventListener('orientationchange', handleResize)
    }
  }, [])

  // ── Adjust square size, gap, and height based on screen dimensions ──
  const isMobileLandscape = dimensions.width > dimensions.height && dimensions.height <= 480
  const isMobilePortrait  = dimensions.width <= 480 && dimensions.height > dimensions.width
  const isDesktop         = !isMobileLandscape && !isMobilePortrait

  const squareSize = isDesktop ? 40 : isMobileLandscape ? 26 : 40
  const gap        = isDesktop ? 24 : isMobileLandscape ? 22 : 24
  const height     = isDesktop ? 100 : isMobileLandscape ? 40 : 60
  const count      = Math.ceil(dimensions.width / (squareSize + gap)) + 1

  return (
    <div
      style={{ height: `${height}px`, display: 'flex', alignItems: 'center', width: '100%' }}
    >
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
    </div>
  )
}

export default function FamilyTreePage() {
  const navigate                        = useNavigate()
  const svgRef                          = useRef(null)

  // ── Page state ──
  const [treeData,     setTreeData]     = useState(null)
  const [activeView,   setActiveView]   = useState(VIEWS[0])
  const [selected,     setSelected]     = useState(null)
  const [figureDetail, setFigureDetail] = useState(null)
  const [loading,      setLoading]      = useState(true)
  const [visible,      setVisible]      = useState(false)

  // ── Responsive breakpoint detection ──
  // Portrait mobile: width ≤ 480px
  const [isMobile,    setIsMobile]    = useState(window.innerWidth <= 480)
  // Landscape mobile: height ≤ 480px and wider than tall
  const [isLandscape, setIsLandscape] = useState(
    window.innerWidth > window.innerHeight && window.innerHeight <= 480
  )

  // ── Update isMobile on resize ──
  useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth <= 480)
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  // ── Update isLandscape on resize or orientation change ──
  useEffect(() => {
    const handle = () => {
      setTimeout(() => {
        setIsLandscape(window.innerWidth > window.innerHeight && window.innerHeight <= 480)
      }, 100)
    }
    window.addEventListener('resize', handle)
    window.addEventListener('orientationchange', handle)
    return () => {
      window.removeEventListener('resize', handle)
      window.removeEventListener('orientationchange', handle)
    }
  }, [])

  // ── Layout constants — adjusted per orientation ──
  const SQUARE_H  = isLandscape ? 40  : 60  // Square border height
  const TOPBAR_H  = isLandscape ? 40  : 80  // Title bar height
  const ZOOM_W    = 50                       // Zoom controls width

  // ── Navigate to previous view — wraps around ──
  const handlePrev = () => {
    const idx = VIEWS.findIndex(v => v.id === activeView.id)
    const prev = VIEWS[(idx - 1 + VIEWS.length) % VIEWS.length]
    handleViewChange(prev)
  }

  // ── Navigate to next view — wraps around ──
  const handleNext = () => {
    const idx = VIEWS.findIndex(v => v.id === activeView.id)
    const next = VIEWS[(idx + 1) % VIEWS.length]
    handleViewChange(next)
  }

  // ── Fetch family tree data from backend on mount ──
  useEffect(() => {
    homerApi.getFamilyTree()
      .then(data => {
        setTreeData(data)
        setLoading(false)
        setTimeout(() => setVisible(true), 100)
      })
      .catch(() => setLoading(false))
  }, [])

  // ── Re-render tree when data, selection, or view changes ──
  useEffect(() => {
    if (!treeData || !svgRef.current) return
    renderTree({
      svgEl:       svgRef.current,
      nodes:       treeData.nodes,
      edges:       treeData.edges,
      selected,
      onNodeClick: handleNodeClick,
      rootNode:    activeView.rootNode,
      categories:  activeView.categories,
      viewId:      activeView.id,
    })
  }, [treeData, selected, activeView])

  // ── Handle node click — fetch figure details ──
  const handleNodeClick = async (name) => {
    setSelected(name)
    try {
      const detail = await homerApi.getFigure(name)
      setFigureDetail(detail)
    } catch {
      setFigureDetail(null)
    }
  }

  // ── Handle view change — reset selection ──
  const handleViewChange = (view) => {
    setActiveView(view)
    setSelected(null)
    setFigureDetail(null)
  }

  return (
    <div className="relative w-full h-full overflow-hidden"
      style={{ backgroundColor: '#ead7b8' }}>

      {/* ── Top square border — hidden on landscape mobile ── */}
      {!isLandscape && (
        <div className="absolute top-0 left-0 right-0 z-10 pointer-events-none">
          <SquareBorder />
        </div>
      )}

      {/* ── Bottom square border — hidden on landscape mobile ── */}
      {!isLandscape && (
        <div className="absolute bottom-1 left-0 right-0 z-10 pointer-events-none">
          <SquareBorder />
        </div>
      )}

      {/* ── Top bar — title + navigation arrows ── */}
      <div
        className="absolute z-50 flex items-center justify-center gap-6"
        style={{
          top:    isLandscape ? '4px' : isMobile ? `${SQUARE_H}px` : `${SQUARE_H + 30}px`,
          left:   0,
          right:  0,
          height: isLandscape ? '36px' : `${TOPBAR_H}px`,
        }}
      >
        {/* ── Left arrow — navigate to previous view ── */}
        <button
          onClick={handlePrev}
          className="transition-all duration-200 hover:scale-110 active:scale-95"
          style={{
            background: 'transparent',
            border:     'none',
            cursor:     'pointer',
            padding:    0,
            flexShrink: 0,
          }}
        >
          <svg width="36" height="36" viewBox="0 0 36 36">
            <polygon
              points="30,4 6,18 30,32"
              fill={activeView.arrowFill}
              stroke={activeView.arrowStroke}
              strokeWidth="2"
            />
          </svg>
        </button>

        {/* ── View title and subtitle ── */}
        <div className="text-center">
          <h1
            className="font-cinzel font-bold tracking-widest"
            style={{
              fontSize:     isLandscape ? '0.85rem' : '1.25rem',
              color:        activeView.titleColor,
              fontWeight:   'bold',
              letterSpacing:'0.1em',
            }}
          >
            {activeView.label.toUpperCase()}
          </h1>
          <p
            className="font-crimson italic"
            style={{
              fontSize: isLandscape ? '0.7rem' : '1rem',
              color:    activeView.descColor,
            }}
          >
            {activeView.desc}
          </p>
        </div>

        {/* ── Right arrow — navigate to next view ── */}
        <button
          onClick={handleNext}
          className="transition-all duration-200 hover:scale-110 active:scale-95"
          style={{
            background: 'transparent',
            border:     'none',
            cursor:     'pointer',
            padding:    0,
            flexShrink: 0,
          }}
        >
          <svg width="36" height="36" viewBox="0 0 36 36">
            <polygon
              points="6,4 30,18 6,32"
              fill={activeView.arrowFill}
              stroke={activeView.arrowStroke}
              strokeWidth="2"
            />
          </svg>
        </button>
      </div>

      {/* ── Return button — top right, navigate back to chat ── */}
      <button
        onClick={() => navigate('/chat')}
        title="Return to Oracle"
        className="absolute z-50 flex items-center justify-center
          rounded-full transition-all duration-200 hover:scale-110 active:scale-95"
        style={{
          top:   isLandscape ? '0px' : isMobile ? '5px' : '20px',
          right: isLandscape ? '5px' : isMobile ? '5px' : '18px',
        }}
      >
        <img
          src={iconOracle}
          alt="Return to Oracle"
          style={{
            width:     isLandscape ? 52 : isMobile ? 52 : 60,
            height:    isLandscape ? 52 : isMobile ? 52 : 60,
            objectFit: 'contain',
          }}
        />
      </button>

      {/* ── Zoom controls — right edge center, hidden on mobile ── */}
      {!isMobile && <div
        className="absolute z-50 flex flex-col items-center
          py-3 gap-1 rounded-lg"
        style={{
          top:                  '50%',
          right:                '16px',
          transform:            'translateY(-50%)',
          background:           'rgba(255, 248, 220, 0.55)',
          backdropFilter:       'blur(12px)',
          WebkitBackdropFilter: 'blur(12px)',
          boxShadow:            '0 4px 24px rgba(0,0,0,0.1)',
        }}
      >
        {[
          { label: '+', fn: () => window._homerZoomIn(),    title: 'Zoom in'    },
          { label: '⟳', fn: () => window._homerZoomReset(), title: 'Reset view' },
          { label: '−', fn: () => window._homerZoomOut(),   title: 'Zoom out'   },
        ].map(({ label, fn, title }) => (
          <button
            key={label}
            onClick={fn}
            title={title}
            className="flex items-center justify-center font-cinzel
              text-lg transition-all duration-200 hover:scale-110
              active:scale-95 rounded-full"
            style={{ width: 44, height: 44, color: '#dfa644' }}
          >
            {label}
          </button>
        ))}
      </div>}

      {/* ── Tree container — holds the D3 SVG ── */}
      <div
        className="absolute overflow-hidden"
        style={{
          top:        isLandscape ? '48px'              : isMobile ? `${SQUARE_H + TOPBAR_H + 10}px` : `${SQUARE_H + TOPBAR_H + 50}px`,
          bottom:     isLandscape ? '0px'               : isMobile ? `${SQUARE_H}px`                 : `${SQUARE_H + 30}px`,
          left:       isLandscape ? '0px'               : isMobile ? '0px'                           : `${ZOOM_W}px`,
          right:      isLandscape ? '0px'               : isMobile ? '0px'                           : `${ZOOM_W}px`,
          opacity:    visible ? 1 : 0,
          transition: 'opacity 0.5s ease',
        }}
      >
        {loading && (
          <div className="flex items-center justify-center h-full">
            <p className="font-cinzel tracking-widest text-lg text-gold-light">
              Consulting the ancient records...
            </p>
          </div>
        )}
        {!loading && treeData && <svg ref={svgRef} />}
      </div>

      {/* ── Figure info panel — shown when a node is selected ── */}
      {selected && figureDetail && (
        <FigureInfoPanel
          figure={figureDetail}
          onClose={() => { setSelected(null); setFigureDetail(null) }}
          onAskHomer={name => navigate(`/chat?ask=${encodeURIComponent(name)}`)}
        />
      )}
    </div>
  )
}