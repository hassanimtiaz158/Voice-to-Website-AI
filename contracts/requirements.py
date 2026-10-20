import re
from typing import Dict, List, Literal, Optional
from pydantic import BaseModel, Field, field_validator

HEX_COLOR_REGEX = re.compile(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")


class ColorPalette(BaseModel):
    primary: str = Field(description="Hex color code for primary branding")
    secondary: str = Field(description="Hex color code for accents")
    background: str = Field(description="Light or dark background hex")
    text: str = Field(description="Contrasting text hex")

    @field_validator("primary", "secondary", "background", "text")
    @classmethod
    def validate_hex(cls, v: str) -> str:
        v = v.strip()
        if not HEX_COLOR_REGEX.match(v):
            raise ValueError(f"Invalid hex color code: '{v}'. Must be valid 3 or 6 digit hex code starting with #")
        return v


class NavItem(BaseModel):
    label: str = Field(min_length=1, max_length=50)
    target_section: str = Field(min_length=1, max_length=50)


class SiteFeature(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    priority: Literal["must_have", "nice_to_have"] = "must_have"


class RequirementsContract(BaseModel):
    project_id: str = Field(min_length=1)
    version_n: int = Field(ge=1, description="Requirements version sequence starting at 1")
    business_name: str = Field(min_length=1, max_length=150)
    business_type: str = Field(min_length=1, max_length=100)
    locale: Literal["en", "ur"] = Field(default="en", description="Default display language: 'en' or 'ur'")
    palette: ColorPalette
    navigation: List[NavItem] = Field(min_length=1, description="List of navigation items")
    features: List[SiteFeature] = Field(default_factory=list)
    hero_headline: str = Field(min_length=1)
    hero_subheadline: str = Field(min_length=1)
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    social_links: Dict[str, str] = Field(default_factory=dict)
