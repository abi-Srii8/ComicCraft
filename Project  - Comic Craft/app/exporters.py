from pathlib import Path
from datetime import datetime

from fpdf import FPDF
from PIL import Image


BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_DIR = (
    BASE_DIR
    / "static"
)

EXPORTS_DIR = (
    STATIC_DIR
    / "exports"
)

EXPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def clean_text(text: str):

    return (
        text
        .encode("latin-1", "replace")
        .decode("latin-1")
    )


def get_image_path(
    image_url: str
):

    relative_path = (
        image_url
        .replace(
            "/static/",
            ""
        )
    )

    path = (
        STATIC_DIR
        / relative_path
    )

    if not path.exists():

        raise FileNotFoundError(
            f"Image not found: {path}"
        )

    return path


class ComicPDF(FPDF):

    def header(self):

        self.set_font(
            "Helvetica",
            "B",
            16
        )

        self.cell(
            0,
            10,
            "ComicCraft - AI Comic",
            align="C"
        )

        self.ln(8)


def save_pdf(layout):

    if not layout:

        raise ValueError(
            "Cannot export empty comic."
        )

    timestamp = (
        datetime.now()
        .strftime(
            "%Y%m%d_%H%M%S"
        )
    )

    filename = (
        f"comiccraft_{timestamp}.pdf"
    )

    output_path = (
        EXPORTS_DIR
        / filename
    )

    pdf = ComicPDF(
        "P",
        "mm",
        "A4"
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    for panel in layout:

        pdf.add_page()

        pdf.set_font(
            "Helvetica",
            "B",
            15
        )

        title = (
            f"Panel "
            f"{panel['panel_number']}: "
            f"{panel['title']}"
        )

        pdf.multi_cell(
            0,
            9,
            clean_text(title)
        )

        image_path = get_image_path(
            panel["image_path"]
        )

        with Image.open(
            image_path
        ) as image:

            width, height = (
                image.size
            )

        max_width = 180
        max_height = 115

        scale = min(
            max_width / width,
            max_height / height
        )

        display_width = (
            width * scale
        )

        display_height = (
            height * scale
        )

        x = (
            210 - display_width
        ) / 2

        pdf.image(

            str(image_path),

            x=x,

            y=pdf.get_y() + 3,

            w=display_width,

            h=display_height
        )

        pdf.ln(
            display_height + 8
        )

        pdf.set_font(
            "Helvetica",
            "I",
            10
        )

        pdf.multi_cell(
            0,
            6,
            clean_text(
                panel[
                    "scene_description"
                ]
            )
        )

        pdf.ln(2)

        pdf.set_font(
            "Helvetica",
            "B",
            10
        )

        pdf.multi_cell(
            0,
            6,
            "Caption"
        )

        pdf.set_font(
            "Helvetica",
            "",
            10
        )

        pdf.multi_cell(
            0,
            6,
            clean_text(
                panel["caption"]
            )
        )

        pdf.ln(2)

        pdf.set_font(
            "Helvetica",
            "B",
            10
        )

        pdf.multi_cell(
            0,
            6,
            "Narration"
        )

        pdf.set_font(
            "Helvetica",
            "",
            10
        )

        pdf.multi_cell(
            0,
            6,
            clean_text(
                panel["narration"]
            )
        )

        if panel.get("dialogue"):

            pdf.ln(2)

            pdf.set_font(
                "Helvetica",
                "B",
                10
            )

            pdf.multi_cell(
                0,
                6,
                "Dialogue"
            )

            pdf.set_font(
                "Helvetica",
                "",
                10
            )

            pdf.multi_cell(
                0,
                6,
                clean_text(
                    panel["dialogue"]
                )
            )

    pdf.output(
        str(output_path)
    )

    return (
        f"/static/exports/{filename}"
    )