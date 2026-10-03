import time

from google import genai
from google.genai import types

from app.config import settings
from app.schemas import OutlineResponse


def get_client():
    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to your .env file."
        )
    return genai.Client(api_key=settings.gemini_api_key)


def generate_outline(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str
):
    prompt = f"""
Create a coherent {settings.panel_count}-panel comic outline.

Story idea:
{story_prompt}

Main character:
{character_name}

Setting:
{setting}

Tone:
{tone}

Art style:
{art_style}

Requirements:

1. Create exactly {settings.panel_count} panels.
2. Number panels from 1 to {settings.panel_count}.
3. Create a clear beginning.
4. Develop the story in the middle.
5. Include a climax.
6. Finish with a satisfying ending.
7. Keep the same main character throughout.
8. Provide a visual scene description.
9. Provide an image generation prompt.
10. Do not put readable text or dialogue inside the image prompt.
11. Keep the story family-friendly.
"""

    client = get_client()
    response = None
    max_tries = 6

    for attempt in range(max_tries):
        try:
            response = client.models.generate_content(
                model=settings.gemini_flash_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=OutlineResponse,
                    temperature=0.8,
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
        raise RuntimeError("Gemini did not return a valid comic outline.")

    panels = response.parsed.panels

    if len(panels) != settings.panel_count:
        raise RuntimeError(
            f"Expected {settings.panel_count} panels "
            f"but received {len(panels)}."
        )

    return [panel.model_dump() for panel in panels]