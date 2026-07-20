# RTM Model Tuning Dashboard

React + Vite scaffold for a client-side dashboard for tuning real-time transaction-monitoring (RTM) models. No backend, no data storage — everything runs in the browser.

The tuning view renders one panel per detector. Each panel has a score-threshold
slider and shows precision, recall, and F1 recomputed live against the
toolkit's synthetic ground truth, alongside a precision/recall-vs-threshold
chart with the detector's configured floor drawn as a reference line.

`dashboard/src/data/tuning-snapshot.json` is a checked-in static sample;
regenerate it by running `python dashboard/scripts/export_tuning_snapshot.py`
from the repo root.

## Getting started

```bash
npm install
npm run dev
```

## Scripts

| Command | Description |
|---|---|
| `npm run dev` | Start the dev server |
| `npm run build` | Production build |
| `npm run preview` | Preview the production build locally |
| `npm run lint` | Lint the codebase |

## License

MIT — see [LICENSE](LICENSE).
