from pathlib import Path
import re

from PIL import Image, ImageDraw

from app.config import settings


BASE_DIR = Path(__file__).resolve().parent.parent

PANELS_DIR = (
    BASE_DIR
    / "static"
    / "panels"
)

PANELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def safe_filename(text: str):

    text = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "_",
        text
    )

    text = text.strip("_")

    return text[:60] or "panel"


def generate_huggingface_image(
    prompt: str
):

    if not settings.hf_token:

        raise RuntimeError(
            "HF_TOKEN is missing. "
            "Add it to your .env file."
        )

    from huggingface_hub import InferenceClient

    client = InferenceClient(
        api_key=settings.hf_token
    )

    image = client.text_to_image(

        prompt=prompt,

        model=settings.hf_image_model,

        width=settings.image_width,

        height=settings.image_height,

        num_inference_steps=settings.image_steps,
    )

    return image


def generate_local_image(
    prompt: str
):

    import torch

    from diffusers import (
        StableDiffusionPipeline
    )

    if torch.cuda.is_available():

        dtype = torch.float16

    else:

        dtype = torch.float32

    pipeline = (
        StableDiffusionPipeline
        .from_pretrained(
            settings.local_image_model,
            torch_dtype=dtype
        )
    )

    if torch.cuda.is_available():

        pipeline = pipeline.to("cuda")

    result = pipeline(

        prompt,

        width=settings.image_width,

        height=settings.image_height,

        num_inference_steps=settings.image_steps
    )

    return result.images[0]


def generate_placeholder_image(
    prompt: str,
    panel_number: int
):

    image = Image.new(

        "RGB",

        (
            settings.image_width,
            settings.image_height
        ),

        "white"
    )

    draw = ImageDraw.Draw(image)

    draw.rectangle(

        (
            15,
            15,
            settings.image_width - 15,
            settings.image_height - 15
        ),

        outline="black",

        width=4
    )

    draw.text(

        (40, 40),

        f"ComicCraft - Panel {panel_number}",

        fill="black"
    )

    draw.text(

        (40, 100),

        prompt[:200],

        fill="black"
    )

    return image


def generate_image(
    prompt: str,
    panel_number: int
):

    final_prompt = f"""
{prompt}

Comic illustration.
Consistent character design.
Cinematic composition.
Expressive characters.
Clean line art.
Detailed background.
Vivid colors.
High quality.
No readable text.
No watermark.
"""

    provider = (
        settings.image_provider
        .lower()
    )

    if provider == "hf":

        image = generate_huggingface_image(
            final_prompt
        )

    elif provider == "local":

        image = generate_local_image(
            final_prompt
        )

    elif provider == "placeholder":

        image = generate_placeholder_image(
            prompt,
            panel_number
        )

    else:

        raise RuntimeError(
            "IMAGE_PROVIDER must be "
            "hf, local, or placeholder."
        )

    filename = (
        f"panel_{panel_number}_"
        f"{safe_filename(prompt)}.png"
    )

    path = PANELS_DIR / filename

    image.convert("RGB").save(
        path,
        "PNG"
    )

    return (
        f"/static/panels/{filename}"
    )