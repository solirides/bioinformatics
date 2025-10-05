# PGIP Frontend

The frontend is a Vite + React + TypeScript application that surfaces plugin metadata, provenance details, and (later) graph-aware visualizations. This initial shell focuses on wiring the project, fetching data from the backend, and sketching the navigation layout.

## Getting Started

```powershell
npm install
npm run dev
```

The development server defaults to http://localhost:5173 and proxies API calls to `VITE_API_URL` (defaults to http://localhost:8000). Override the backend target via:

```powershell
$env:VITE_API_URL = "http://localhost:8000"
npm run dev
```

## Available Pages

- **Dashboard** – Landing page outlining project goals and upcoming widgets.
- **Plugin Registry** – Lists plugins from the FastAPI backend using React Query.
- **Plugin Detail** – Displays manifest information, inputs/outputs, and provenance.

## Tech Stack

- React 18 with React Router
- Vite for development/build tooling
- React Query for data fetching and caching
- Axios for API requests

## Next UI Iterations

- Integrate design system tokens and theming
- Add charts/visualizations for pipeline health and benchmarking results
- Create shared components (tables, badges, copy-to-clipboard, etc.)
- Implement authentication-aware navigation once backend supports it
