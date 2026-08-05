// ── Category colors — fill, stroke, and text for each mythology figure type ──
// Shared between FamilyTreePage (tree node rendering) and FigureInfoPanel
// (info panel accent color) so both stay in sync from one source of truth.
export const CATEGORY_COLORS = {
  primordial: { fill: '#e7b85a', stroke: '#c48a5a', text: '#f3e9d9' },
  titan:      { fill: '#7a3d26', stroke: '#c48a5a', text: '#f3e9d9' },
  olympian:   { fill: '#9fb8c0', stroke: '#3f525a', text: '#f3e9d9' },
  underworld: { fill: '#3f525a', stroke: '#b8ab97', text: '#f3e9d9' },
  hero:       { fill: '#cfae6d', stroke: '#7a3d26', text: '#f3e9d9' },
  minor_god:  { fill: '#a15732', stroke: '#c48a5a', text: '#f3e9d9' },
  nymph:      { fill: '#c48a5a', stroke: '#8c4b2b', text: '#f3e9d9' },
  mortal:     { fill: '#b8ab97', stroke: '#f3e9d9', text: '#f3e9d9' },
  muse:       { fill: '#897477', stroke: '#f3e9d9', text: '#f3e9d9' },
}