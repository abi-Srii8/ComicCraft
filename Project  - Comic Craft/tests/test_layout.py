from app.layout_builder import (
    build_comic_layout
)


def test_layout_matches_images():

    story = [

        {

            "panel_number": 1,

            "title": "Beginning",

            "scene_description":
                "A hero enters a forest.",

            "caption":
                "The journey begins.",

            "narration":
                "The hero looks around.",

            "dialogue":
                "Hello!",

            "image_prompt":
                "A hero in a forest."
        }

    ]

    images = [
        "/static/panels/panel_1.png"
    ]

    result = build_comic_layout(
        story,
        images
    )

    assert len(result) == 1

    assert (
        result[0]["panel_number"]
        == 1
    )

    assert (
        result[0]["image_path"]
        .endswith("panel_1.png")
    )