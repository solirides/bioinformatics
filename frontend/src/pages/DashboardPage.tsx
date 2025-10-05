const DashboardPage = () => {
  return (
    <section className="page">
      <header>
        <h2>Welcome to PGIP</h2>
        <p>
          Explore pangenome assets, annotation plugins, and provenance metrics as we
          expand the platform. This dashboard will grow to include charts and run
          status widgets.
        </p>
      </header>
      <div className="card-grid">
        <article className="card">
          <h3>Quick Links</h3>
          <ul>
            <li>View registered plugins</li>
            <li>Track workflow runs</li>
            <li>Review provenance summaries</li>
          </ul>
        </article>
        <article className="card">
          <h3>Next Up</h3>
          <p>Connect the dashboard to backend metrics and add real-time charts.</p>
        </article>
      </div>
    </section>
  );
};

export default DashboardPage;
