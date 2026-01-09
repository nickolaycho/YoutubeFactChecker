import json
from openai import RateLimitError, APIError
from app.utils.retry import expo_backoff_sleep
from app.core.structured_output import AnalyzeResponse
from app.utils.openai_client import client
from app.utils.retry import enforce_no_additional_properties

def analyze_transcript(transcript: str) -> AnalyzeResponse:
    schema = AnalyzeResponse.model_json_schema()
    print("Schema: ", schema)
    schema = enforce_no_additional_properties(schema)
    print("Enforced schema:", schema)

    prompt = (
        "You are a neutral scientific explainer about fitness/health. "
        "Do NOT give medical advice. Focus on evidence quality and uncertainty of the following statements. "
        "Return structured JSON only.\n\n"+
        transcript
    )

    last_err = None
    for attempt in range(5):
        try:
            resp = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt,
                max_output_tokens=1200,
                temperature=0.1,
                text={
                "format": {
                    "type": "json_schema",
                    "name": "analyze_response", 
                    "schema": schema,
                    "strict": True,
                }
            },
            )
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
