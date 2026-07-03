import { motion } from 'framer-motion'

function buildPath(points, width = 120, height = 36) {
  if (!points || points.length === 0) return ''
  const max = Math.max(...points)
  const min = Math.min(...points)
  const range = Math.max(1, max - min)
  return points
    .map((v, i) => {
      const x = (i / (points.length - 1)) * width
      const y = height - ((v - min) / range) * height
      return `${i === 0 ? 'M' : 'L'} ${x.toFixed(2)} ${y.toFixed(2)}`
    })
    .join(' ')
}

export function Sparkline({ points = [10, 12, 8, 14, 16, 12], width = 120, height = 36, color = '#06b6d4' }) {
  const d = buildPath(points, width, height)

  return (
    <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} className="block">
      <path d={d} fill="none" stroke={color} strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

export default Sparkline
