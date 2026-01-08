import time
import random

def expo_backoff_sleep(attempt: int,
    base: float = 0.5,
    cap: float = 8.0) -> None:
    
    delay = min(cap, base * (2 ** attempt))
    delay = delay * (0.8 + 0.4 * random.random())  # jitter
    time.sleep(delay)

def enforce_no_additional_properties(schema: dict) -> dict:
    """
    Recursively enforce additionalProperties=false on all object schemas,
    including those under $defs / definitions.
    Required by OpenAI Structured Outputs with strict=true.
    """
    if not isinstance(schema, dict):
        return schema

    # If this is an object schema, close it
    if schema.get("type") == "object":
        schema["additionalProperties"] = False
        for prop in schema.get("properties", {}).values():
            enforce_no_additional_properties(prop)

    # Arrays
    if schema.get("type") == "array":
        enforce_no_additional_properties(schema.get("items"))

    # Combinators
    for key in ("anyOf", "oneOf", "allOf"):
        if key in schema:
            for subschema in schema[key]:
                enforce_no_additional_properties(subschema)

    # IMPORTANT: handle definitions / $defs (this was missing)
    for key in ("$defs", "definitions"):
        if key in schema and isinstance(schema[key], dict):
            for subschema in schema[key].values():
                enforce_no_additional_properties(subschema)

    return schema


