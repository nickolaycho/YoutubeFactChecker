from fastapi import APIRouter, HTTPException
from app.core.structured_output import AnalyzeRequest, AnalyzeResponse
from app.core.fact_checker import FactChecker
import traceback

router = APIRouter()

@router.post("/v1/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    try:
        fc = FactChecker(video_url=str(req.url))
        return fc.result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=422, detail=f"{type(e).__name__}: {e}")
