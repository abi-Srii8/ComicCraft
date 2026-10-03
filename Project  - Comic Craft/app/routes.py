import time

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import ValidationError

from .schemas import PromptRequest
from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import (
    generate_image,
    generate_placeholder_image,
    safe_filename,
    PANELS_DIR,
)
from .demo import sample_panels

router = APIRouter()


def pick(form, *names, default=""):
    for name in names:
        value = form.get(name)
        if value:
            return value
    return default


def safe_generate_image(prompt, panel_number):
    # Munnaadi generate aana image irundha adhaiye use pannum
    filename = f"panel_{panel_number}_{safe_filename(prompt)}.png"
    if (PANELS_DIR / filename).exists():
        print(f"Panel {panel_number}: saved image reuse aachu")
        return f"/static/panels/{filename}"

    # HF fail aana 3 thadava try pannum
    for attempt in range(3):
        try:
            return generate_image(prompt, panel_number)
        except Exception as e:
            print(f"Panel {panel_number} attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                time.sleep(15)

    # Kadaisi la placeholder
    print(f"Panel {panel_number}: placeholder use aachu")
    image = generate_placeholder_image(prompt, panel_number)
    placeholder = f"placeholder_{panel_number}.png"
    image.convert("RGB").save(PANELS_DIR / placeholder, "PNG")
    return f"/static/panels/{placeholder}"


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@router.post("/generate", response_class=HTMLResponse)
async def generate(request: Request):
    form = await request.form()

    try:
        data = PromptRequest(
            story_prompt=pick(form, "story_prompt", "prompt"),
            character_name=pick(form, "character_name", "character", default="Hero"),
            setting=pick(form, "setting", default="village"),
            tone=pick(form, "tone", default="adventurous"),
            art_style=pick(form, "art_style", default="comic book"),
            language=pick(form, "language", default="English"),
        )
    except ValidationError:
        raise HTTPException(
            status_code=400,
            detail="Story prompt kandippa venum (minimum 5 letters)."
        )

    try:
        try:
            outline = generate_outline(
                story_prompt=data.story_prompt,
                character_name=data.character_name,
                setting=data.setting,
                tone=data.tone,
                art_style=data.art_style,
            )

            panels = generate_story(
                outline,
                data.character_name,
                data.setting,
                data.tone,
                data.art_style,
            )
        except Exception as e:
            print("Gemini failed, using demo story:", e)
            panels = sample_panels(data.character_name)

        title = f"{data.character_name}'s Comic"

        layout = []

        for panel in panels:
            image_path = safe_generate_image(
                panel["image_prompt"],
                panel["panel_number"],
            )
            item = dict(panel)
            item["image_path"] = image_path
            layout.append(item)

        return request.app.state.templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "title": title,
                "layout": layout,
                "panels": panels,
                "pdf_path": "#"
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/test-image")
async def test_image():
    image_path = generate_image(
        "A student standing in a classroom",
        1
    )

    return {
        "message": "Image created successfully",
        "image": image_path
    }