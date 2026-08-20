# ReachOut Architecture

## MVP flow

```text
React frontend
      |
      v
FastAPI backend
      |
      +---- PostgreSQL (company, people, jobs, sources)
      |
      +---- Search provider abstraction
      |         |
      |         +---- Brave Search (initial provider)
      |
      +---- AI service (analysis, matching, outreach)
```

## Principles

1. Search providers are replaceable; ReachOut is not coupled to one provider.
2. Public sources are stored with provenance and verification timestamps.
3. Search results are cached/enriched so repeated searches do not require repeated web requests.
4. The MVP avoids unnecessary microservices and infrastructure complexity.
5. Users remain in control of outreach; ReachOut drafts messages but does not automatically spam contacts.
