from typing import TypedDict, List, Dict
from pydantic import BaseModel, Field


class PromptOutput(BaseModel):
    website_prompt: str = Field(description="A high-quality plain English prompt to generate a website")

class RequirementsOutput(BaseModel):
    summary: str = Field(
        description="A concise summary of what the user wants to build"
    )
    features: List[str] = Field(
        description="Core features and functionalities required for the website"
    )
    design_requirements: List[str] = Field(
        description="UI/UX, styling, layout, and visual requirements"
    )
    technical_requirements: List[str] = Field(
        description="Technical aspects such as frameworks, integrations, performance, or constraints"
    )
    pages: List[str] = Field(
        description="List of pages or sections the website should include"
    )
    extra_notes: List[str] = Field(
        description="Any additional requirements, constraints, or special instructions"
    )



class InitialState(TypedDict):
    user_input: str
    prompt_to_use_from_user: str
    requirements: RequirementsOutput