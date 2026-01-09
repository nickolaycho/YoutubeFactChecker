# YouTube Health Videos Fact Checker

An MVP AI-powered service that analyzes **YouTube videos** about **fitness and health**, extracts factual claims, and provides neutral, evidence-based context with links for further reading.

>⚠️ This tool does not provide medical advice. Its goal is contextualization, not diagnosis or prescriptions.

## 🎯 What problem does it solve?

Health and fitness content on YouTube often contains:

- oversimplified claims
- cherry-picked studies
- statements presented as facts without sufficient context

This service:

- extracts checkable claims from a video
- evaluates them as **supported / inconclusive / misleading**
- explains why, with an explicit uncertainty level
- suggests reputable sources for further reading

It is designed as a **backend service**, suitable for:
- moderation tool
- reputation scoring
- content review

## 🧠 High-level architecture
```Client → FastAPI (/v1/analyze) → YouTube Transcript Fetcher → LLM Analysis (OpenAI Responses API) → Strict Structured JSON Output```

## 🧩 Output format (example)
```json
{
  "summary_bullets": [
    "The video discusses fasted cardio and fat loss."
  ],
  "claims": [
    {
      "claim": "Training fasted burns more body fat.",
      "assessment": "inconclusive",
      "explanation": "Some studies show increased fat oxidation, but no clear long-term fat loss advantage.",
      "confidence": "medium",
      "keywords": ["fasted cardio", "fat oxidation"]
    }
  ],
  "learn_more": [
    {
      "title": "Cochrane Review on Exercise and Weight Loss",
      "url": "https://www.cochranelibrary.com/",
      "why": "Systematic reviews of clinical evidence."
    }
  ],
  "suggested_search_queries": [
    "fasted cardio fat loss meta-analysis"
  ],
  "medical_disclaimer": "This analysis is for informational purposes only and is not medical advice."
}
```

## 🚀 How to run locally
0. Create a _.env_ file and write there your OpenAI API key:
> OPENAI_API_KEY=your-key-without-spaces-or-quotes

1. Activate virtual environment
> source venv/Scripts/activate

2. Install dependencies
> pip install -r requirements.txt

3. Run the API
> python -m uvicorn app.main:app --reload

4. Open Swagger UI
> http://127.0.0.1:8000/docs
Use POST /v1/analyze and provide a YouTube URL:
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

## ⚠️ Limitations (by design)

- Videos without transcripts cannot be analyzed
- The system does not browse the web in real time
- Scientific evaluation is based on general consensus, not exhaustive literature review
- Output reflects uncertainty explicitly and may be conservative
