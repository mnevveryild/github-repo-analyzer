from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="GitHub Repo Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    repo_url: str
    mode: str = "code_review"


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/analyze")
def analyze(request: AnalyzeRequest):
    from src.agent import analyze_repo
    try:
        result = analyze_repo(request.repo_url, request.mode)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
