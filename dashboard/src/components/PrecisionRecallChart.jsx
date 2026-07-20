const WIDTH = 320
const HEIGHT = 160
const PADDING = 24

function scaleX(threshold) {
  return PADDING + ((threshold - 60) / 40) * (WIDTH - 2 * PADDING)
}

function scaleY(value) {
  return HEIGHT - PADDING - value * (HEIGHT - 2 * PADDING)
}

function toPoints(curve, key) {
  return curve.map((point) => scaleX(point.threshold) + ',' + scaleY(point[key])).join(' ')
}

export default function PrecisionRecallChart({ curve, floor }) {
  return (
    <svg width={WIDTH} height={HEIGHT} role="img" aria-label="Precision and recall versus score threshold">
      <polyline points={toPoints(curve, 'precision')} fill="none" stroke="#2563eb" strokeWidth="2" />
      <polyline points={toPoints(curve, 'recall')} fill="none" stroke="#16a34a" strokeWidth="2" />
      {floor && (
        <line
          x1={PADDING}
          x2={WIDTH - PADDING}
          y1={scaleY(floor.minimum_precision)}
          y2={scaleY(floor.minimum_precision)}
          stroke="#dc2626"
          strokeDasharray="4 4"
        />
      )}
      {curve.map((point) => (
        <circle key={'precision-' + point.threshold} cx={scaleX(point.threshold)} cy={scaleY(point.precision)} r="3" fill="#2563eb" />
      ))}
      {curve.map((point) => (
        <circle key={'recall-' + point.threshold} cx={scaleX(point.threshold)} cy={scaleY(point.recall)} r="3" fill="#16a34a" />
      ))}
    </svg>
  )
}
