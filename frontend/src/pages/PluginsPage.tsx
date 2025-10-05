import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { fetchPlugins, PluginSummary } from "../api/client";

const PluginsPage = () => {
  const { data, isLoading, isError, error } = useQuery<PluginSummary[], Error>({
    queryKey: ["plugins"],
    queryFn: fetchPlugins,
    staleTime: 30_000
  });

  if (isLoading) {
    return (
      <section className="page">
        <p>Loading plugins…</p>
      </section>
    );
  }

  if (isError) {
    return (
      <section className="page">
        <p className="error">Failed to load plugins: {error.message}</p>
      </section>
    );
  }

  return (
    <section className="page">
      <header className="page-header">
        <h2>Plugin Registry</h2>
        <p>Browse registered annotation modules. This data comes directly from the backend API.</p>
      </header>

      <div className="card-grid">
  {data?.map((plugin: PluginSummary) => (
          <article key={`${plugin.name}-${plugin.version}`} className="card">
            <header>
              <h3>{plugin.name}</h3>
              <span className="version">v{plugin.version}</span>
            </header>
            <p>{plugin.description}</p>
            {plugin.tags?.length ? (
              <ul className="tag-list">
                {plugin.tags.map((tag) => (
                  <li key={tag}>{tag}</li>
                ))}
              </ul>
            ) : null}
            <footer>
              <Link to={`/plugins/${plugin.name}`} className="link-button">
                View Details
              </Link>
            </footer>
          </article>
        ))}
        {!data?.length && (
          <article className="card">
            <h3>No plugins yet</h3>
            <p>
              Register a plugin using the backend API or CLI. Once added it will appear here with
              provenance metadata.
            </p>
          </article>
        )}
      </div>
    </section>
  );
};

export default PluginsPage;
