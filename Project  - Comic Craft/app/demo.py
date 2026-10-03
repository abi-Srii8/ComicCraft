def sample_panels(name: str):
    story = [
        ("A Strange Discovery", f"{name} finds a glowing map under an old tree.", "It all began one quiet morning.", f"{name} found something magical.", "What is this glowing map?"),
        ("The Journey Begins", f"{name} walks through a bright, colorful path.", "The map showed a hidden path.", "The adventure started.", "Let's follow it!"),
        ("A Big Challenge", f"{name} reaches a wide river with a broken bridge.", "But the way was blocked.", "Every hero faces a challenge.", "I must find another way."),
        ("Clever Idea", f"{name} builds a small raft using branches.", "Courage and cleverness helped.", "The raft floated safely.", "It works!"),
        ("Happy Ending", f"{name} finds a treasure chest full of stories.", "At last, the treasure was found.", "The best treasure was the journey.", "What an amazing day!"),
    ]
    return [
        {
            "panel_number": i + 1,
            "title": t,
            "scene_description": scene,
            "caption": cap,
            "narration": nar,
            "dialogue": dia,
            "image_prompt": f"{scene}, colorful comic panel, no text",
        }
        for i, (t, scene, cap, nar, dia) in enumerate(story)
    ]