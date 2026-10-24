"""FastAPI app for the Admissions Review Platform.

Just a health check for now (Phase 1: foundation) — upload/extraction/
validation/decision endpoints are added in later phases as each pipeline
stage is built.

Run:
    uvicorn admissions_platform.api.main:app --reload --port 8010
"""
from fastapi import FastAPI

app = FastAPI(
    title="Admissions Review Platform API",
    description=(
        "Automates university admission eligibility review from transcript upload through "
        "a human-reviewed decision. Portfolio/educational project using synthetic data only — "
        "no real applicant data, and not affiliated with any real university."
    ),
    version="0.1.0",
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
