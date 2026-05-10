from fastapi import FastAPI

app = FastAPI(title="MOS Phase 1 API")

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "mos-phase1-backend"
    }