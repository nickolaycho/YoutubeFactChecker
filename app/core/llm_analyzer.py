import json
from openai import RateLimitError, APIError
from app.utils.utils import expo_backoff_sleep
from app.core.structured_output import AnalyzeResponse
from app.utils.openai_client import client
from app.utils.utils import enforce_no_additional_properties
from pydantic import BaseModel
from typing import Type

class LLMAnalyzer:
    def __init__(self,
        transcript: str,
        schema: Type[BaseModel]) -> None:

        self.transcript = transcript
        self.schema = schema.model_json_schema()
        self.schema = enforce_no_additional_properties(self.schema)
        self.prompt = (
            "You are a neutral scientific explainer about fitness/health. "
            "Do NOT give medical advice. Focus on evidence quality and uncertainty of the following statements. "
            "Return structured JSON only.\n\n"
            +
            transcript
        )
        self.llm_configs = {
            "model":"gpt-4.1-mini",
            "input": self.prompt,
            "max_output_tokens": 2500,
            "temperature":0.1,
            "text":{
            "format": {
                "type": "json_schema",
                "name": "analyze_response", 
                "schema": self.schema,
                "strict": True,
            }
            },
        }

    @property
    def analyze_transcript(self) -> AnalyzeResponse:
        last_err = None
        for attempt in range(5):
            try:
                resp = client.responses.create(**self.llm_configs)
                data = json.loads(resp.output_text)
                return AnalyzeResponse.model_validate(data)

            except RateLimitError as e:
                last_err = e
                expo_backoff_sleep(attempt)
            except APIError as e:
                # transient server-side
                last_err = e
                expo_backoff_sleep(attempt)

        raise RuntimeError(f"OpenAI request failed after retries: {last_err}")
