// Presentational only — kept separate from app/page.tsx (an async Server
// Component that does the actual fetch) so this piece can be unit tested
// synchronously with Testing Library.
export default function HomeContent({ apiOnline, apiBaseUrl }: { apiOnline: boolean; apiBaseUrl: string }) {
  return (
    <main className="mx-auto max-w-3xl flex-1 px-6 py-16">
      <div className="mb-3 inline-flex items-center gap-2 rounded-full border border-[var(--border-strong)] bg-[var(--gold-soft)] px-3 py-1 text-xs font-medium text-[var(--navy)]">
        Portfolio project &middot; synthetic data only
      </div>
      <h1 className="font-display text-4xl font-semibold text-[var(--navy)]">Admissions Review Platform</h1>
      <p className="mt-4 max-w-xl text-[var(--text-secondary)]">
        Automates the first pass of transfer-admission eligibility review: transcript extraction, multi-agent
        validation, handbook-rules checking, and course-catalog verification — producing a draft recommendation
        a human admissions officer reviews before anything is final.
      </p>

      <div className="panel mt-8 flex items-center gap-3 p-4">
        <span
          data-testid="status-dot"
          className={`h-2.5 w-2.5 rounded-full ${apiOnline ? "bg-[var(--status-good)]" : "bg-[var(--status-bad)]"}`}
        />
        <span className="text-sm text-[var(--text-secondary)]">
          API ({apiBaseUrl}) is <strong>{apiOnline ? "online" : "unreachable"}</strong>
        </span>
      </div>

      {!apiOnline && (
        <pre className="mt-4 overflow-x-auto rounded-lg border border-[var(--border)] bg-white p-3 text-xs text-[var(--text-secondary)]">
          export PYTHONPATH=src{"\n"}uvicorn admissions_platform.api.main:app --port 8010
        </pre>
      )}

      <p className="mt-10 text-xs text-[var(--text-muted)]">
        Foundation phase: data model, synthetic transcript/handbook generators, and the LLM client interface are
        built and tested. Upload, extraction, validation, and the review workflow land in the next phases.
      </p>
    </main>
  );
}
