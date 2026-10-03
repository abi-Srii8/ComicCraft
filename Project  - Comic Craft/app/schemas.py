from pydantic import AliasChoices, BaseModel, Field, field_validator


class PromptRequest(BaseModel):

    # "story_prompt" or "prompt" - rendu name um work aagum
    story_prompt: str = Field(
        ...,
        min_length=5,
        max_length=2000,
        validation_alias=AliasChoices("story_prompt", "prompt")
    )

    character_name: str = Field(
        default="Hero",
        min_length=1,
        max_length=80
    )

    setting: str = Field(
        default="Fantasy world",
        min_length=1,
        max_length=120
    )

    tone: str = Field(
        default="Adventurous",
        min_length=1,
        max_length=50
    )

    art_style: str = Field(
        default="comic book",
        min_length=1,
        max_length=80
    )

    language: str = Field(
        default="English",
        max_length=50
    )

    @field_validator(
        "story_prompt",
        "character_name",
        "setting",
        "tone",
        "art_style"
    )
    @classmethod
    def remove_spaces(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "Value cannot be empty."
            )

        return value


class PanelOutline(BaseModel):

    panel_number: int

    title: str

    scene_description: str

    image_prompt: str


class OutlineResponse(BaseModel):

    panels: list[PanelOutline]


class PanelStory(BaseModel):

    panel_number: int

    title: str

    scene_description: str

    caption: str

    narration: str

    dialogue: str

    image_prompt: str


class StoryResponse(BaseModel):

    panels: list[PanelStory]