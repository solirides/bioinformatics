import { NavLink, Route, Routes } from "react-router-dom";

import DashboardPage from "./pages/DashboardPage";
import PluginDetailPage from "./pages/PluginDetailPage";
import PluginsPage from "./pages/PluginsPage";

const App = () => {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h1 className="logo">PGIP</h1>
        <nav>
          <NavLink to="/" end>
            Dashboard
          </NavLink>
          <NavLink to="/plugins">Plugins</NavLink>
        </nav>
      </aside>
      <main className="main-content">
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/plugins" element={<PluginsPage />} />
          <Route path="/plugins/:name" element={<PluginDetailPage />} />
          <Route path="*" element={<DashboardPage />} />
        </Routes>
      </main>
    </div>
  );
};

export default App;
