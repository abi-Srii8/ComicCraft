def build_comic_layout(
    story_panels,
    image_paths
):

    if len(story_panels) != len(image_paths):

        raise ValueError(
            "Number of story panels and images "
            "must be equal."
        )

    layout = []

    for panel, image_path in zip(
        story_panels,
        image_paths
    ):

        layout.append({

            "panel_number":
                panel["panel_number"],

            "title":
                panel["title"],

            "image_path":
                image_path,

            "scene_description":
                panel["scene_description"],

            "caption":
                panel["caption"],

            "narration":
                panel["narration"],

            "dialogue":
                panel["dialogue"],

            "image_prompt":
                panel["image_prompt"],
        })

    return layout