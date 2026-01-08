from pydantic import BaseModel, HttpUrl, Field
from typing import Literal, List

class AnalyzeRequest(BaseModel):
    url: HttpUrl

Assessment = Literal["supported", "inconclusive", "misleading"]
Confidence = Literal["low", "medium", "high"]

class Claim(BaseModel):
    claim: str
    assessment: Assessment
    explanation: str
    confidence: Confidence
    keywords: List[str]

class LearnMore(BaseModel):
    title: str
    url: str
    why: str

class AnalyzeResponse(BaseModel):
    summary_bullets: List[str]
    claims: List[Claim]
    learn_more: List[LearnMore]
    suggested_search_queries: List[str]
    medical_disclaimer: str
