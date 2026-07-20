export function computeMetricsAtThreshold(detectorSnapshot, threshold) {
  const passing = detectorSnapshot.flagged.filter((entity) => entity.score >= threshold)
  const positiveIds = new Set(detectorSnapshot.ground_truth_positive_ids)
  const tp = passing.filter((entity) => positiveIds.has(entity.entity_id)).length
  const fp = passing.length - tp
  const groundTruthCount = detectorSnapshot.ground_truth_positive_count
  const fn = groundTruthCount - tp
  const precision = passing.length > 0 ? tp / passing.length : 0
  const recall = groundTruthCount > 0 ? tp / groundTruthCount : 1
  const f1 = precision + recall > 0 ? (2 * precision * recall) / (precision + recall) : 0
  return { precision, recall, f1, tp, fp, fn }
}

export function metricsCurve(detectorSnapshot) {
  const thresholds = Array.from(
    new Set(detectorSnapshot.flagged.map((entity) => entity.score)),
  ).sort((a, b) => a - b)
  return thresholds.map((threshold) => ({
    threshold,
    ...computeMetricsAtThreshold(detectorSnapshot, threshold),
  }))
}
