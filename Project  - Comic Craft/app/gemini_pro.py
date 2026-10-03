import time

from google import genai
from google.genai import types

from app.config import settings
from app.schemas import StoryResponse


def get_client():
    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to your .env file."
        )
    return genai.Client(api_key=settings.gemini_api_key)


def generate_story(
    outline,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str
):
    prompt = f"""
Expand this comic outline into a complete comic script.

Main character:
{character_name}

Setting:
{setting}

Tone:
{tone}

Art style:
{art_style}

For every panel provide:

- panel number
- title
- scene description
- caption
- narration
- dialogue
- image prompt

Rules:

1. Preserve the original panel order.
2. Keep the character consistent.
3. Make the story flow naturally.
4. Use short readable narration.
5. Dialogue should sound natural.
6. If a panel does not need dialogue, return an empty string.
7. Do not put dialogue inside image prompts.
8. Keep the story family-friendly.

Comic outline:

{outline}
"""

    client = get_client()
    response = None
    max_tries = 6

    for attempt in range(max_tries):
        try:
            response = client.models.generate_content(
                model=settings.gemini_pro_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=StoryResponse,
                    temperature=0.9,
                ),
            )
            break
        except Exception as e:
            busy = any(
    word in str(e)
    for word in ("503", "429", "disconnected", "timed out", "Connection")
)
            if busy and attempt < max_tries - 1:
                wait = 10 * (attempt + 1)
                print(f"Gemini busy. Retry {attempt + 1} after {wait}s...")
                time.sleep(wait)
                continue
            raise

    if not response or not response.parsed:
        raise RuntimeError("Gemini did not return a valid comic script.")

    panels = response.parsed.panels

    if len(panels) != settings.panel_count:
        raise RuntimeError(
            f"Expected {settings.panel_count} story panels "
            f"but received {len(panels)}."
        )

    return [panel.model_dump() for panel in panels]