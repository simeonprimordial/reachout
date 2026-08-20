import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API_BASE_URL = "http://localhost:8000";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function discover(searchQuery = query) {
    const trimmed = searchQuery.trim();
    if (!trimmed) return;

    setLoading(true);
    setError("");
    setResults([]);

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/companies?q=${encodeURIComponent(trimmed)}`
      );
      const payload = await response.json();

      if (!response.ok) {
        throw new Error(payload.detail || "Unable to search companies.");
      }

      setResults(payload.results || []);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(event) {
    event.preventDefault();
    discover();
  }

  return (
    <main className="page">
      <nav className="nav">
        <div className="brand">ReachOut</div>
        <span className="tagline">Find companies. Find the right person. Reach out.</span>
      </nav>

      <section className="hero">
        <p className="eyebrow">GLOBAL OPPORTUNITY DISCOVERY</p>
        <h1>Find companies that should know you.</h1>
        <p className="subtitle">
          Discover companies worldwide, identify relevant decision-makers, and build targeted career outreach.
        </p>

        <form className="search-box" onSubmit={handleSubmit}>
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            aria-label="Search companies"
            placeholder="Try: AI startups in Japan using AWS and Kubernetes"
          />
          <button type="submit" disabled={loading}>
            {loading ? "Searching..." : "Discover"}
          </button>
        </form>

        <div className="examples">
          <span>Try:</span>
          {["Cloud startups in Japan", "AWS companies in Germany", "DevSecOps opportunities in Singapore"].map((example) => (
            <button
              type="button"
              key={example}
              onClick={() => {
                setQuery(example);
                discover(example);
              }}
            >
              {example}
            </button>
          ))}
        </div>
      </section>

      {(loading || error || results.length > 0) && (
        <section className="results-section">
          <div className="results-heading">
            <div>
              <p className="eyebrow">DISCOVERY RESULTS</p>
              <h2>{loading ? "Searching the web..." : `${results.length} results found`}</h2>
            </div>
          </div>

          {error && <div className="status error">{error}</div>}

          {!loading && !error && results.length > 0 && (
            <div className="results-grid">
              {results.map((company) => (
                <article className="company-card" key={company.source_url}>
                  <div className="company-domain">{company.website}</div>
                  <h3>{company.name}</h3>
                  <h4>{company.title}</h4>
                  <p>{company.description || "No description available from the search result."}</p>
                  <a href={company.source_url} target="_blank" rel="noreferrer">
                    View source →
                  </a>
                </article>
              ))}
            </div>
          )}

          {!loading && !error && results.length === 0 && (
            <div className="status">No results found. Try a broader search.</div>
          )}
        </section>
      )}

      <section className="features">
        <article><strong>01</strong><h2>Discover</h2><p>Find companies beyond traditional job boards.</p></article>
        <article><strong>02</strong><h2>Identify</h2><p>Find founders, CTOs and relevant engineering leaders.</p></article>
        <article><strong>03</strong><h2>Match</h2><p>Understand why your skills could fit the company.</p></article>
        <article><strong>04</strong><h2>Reach out</h2><p>Create personalized outreach you control before sending.</p></article>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(
  <React.StrictMode><App /></React.StrictMode>
);
