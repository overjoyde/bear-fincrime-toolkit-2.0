import { useState } from 'react'
import { computeMetricsAtThreshold, metricsCurve } from '../lib/metrics'
import PrecisionRecallChart from './PrecisionRecallChart'

export default function DetectorTuningPanel({ name, snapshot }) {
  const [threshold, setThreshold] = useState(60)
  const metrics = computeMetricsAtThreshold(snapshot, threshold)
  const curve = metricsCurve(snapshot)
  const floor = snapshot.floor
  const passes = floor
    ? metrics.precision >= floor.minimum_precision && metrics.recall >= floor.minimum_recall
    : null

  return (
    <section>
      <h2>{name}</h2>
      <label>
        Score threshold: {threshold}
        <input
          type="range"
          min="60"
          max="100"
          value={threshold}
          onChange={(event) => setThreshold(Number(event.target.value))}
        />
      </label>
      <ul>
        <li>Precision: {(metrics.precision * 100).toFixed(1)}%</li>
        <li>Recall: {(metrics.recall * 100).toFixed(1)}%</li>
        <li>F1: {(metrics.f1 * 100).toFixed(1)}%</li>
        <li>TP: {metrics.tp}, FP: {metrics.fp}, FN: {metrics.fn}</li>
      </ul>
      <p>
        {floor
          ? 'Floor: precision >= ' + (floor.minimum_precision * 100).toFixed(0) + '%, recall >= ' +
            (floor.minimum_recall * 100).toFixed(0) + '% - ' + (passes ? 'PASS' : 'FAIL')
          : 'No floor configured for this detector.'}
      </p>
      <PrecisionRecallChart curve={curve} floor={floor} />
    </section>
  )
}
