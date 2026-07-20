import snapshot from './data/tuning-snapshot.json'
import DetectorTuningPanel from './components/DetectorTuningPanel'

function App() {
  return (
    <main>
      <h1>RTM Model Tuning Dashboard</h1>
      <p>
        Drag each detector's score threshold to see precision, recall, and F1
        recompute live against the toolkit's synthetic ground truth.
      </p>
      {Object.entries(snapshot).map(([name, detectorSnapshot]) => (
        <DetectorTuningPanel key={name} name={name} snapshot={detectorSnapshot} />
      ))}
    </main>
  )
}

export default App
