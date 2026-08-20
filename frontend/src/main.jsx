import React from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

function App() {
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

        <div className="search-box">
          <input
            aria-label="Search companies"
            placeholder="Try: AI startups in Japan using AWS and Kubernetes"
          />
          <button type="button">Discover</button>
        </div>

        <div className="examples">
          <span>Try:</span>
          <button type="button">Cloud startups in Japan</button>
          <button type="button">AWS companies in Germany</button>
          <button type="button">DevSecOps opportunities in Singapore</button>
        </div>
      </section>

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
