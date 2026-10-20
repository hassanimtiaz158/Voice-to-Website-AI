import pytest
from pydantic import ValidationError

from contracts.requirements import (
    ColorPalette,
    NavItem,
    RequirementsContract,
    SiteFeature,
)


def test_requirements_contract_valid_json():
    data = {
        "project_id": "proj-123",
        "version_n": 1,
        "business_name": "Lahore Leather Goods",
        "business_type": "Retail Apparel",
        "locale": "ur",
        "palette": {
            "primary": "#1E3A8A",
            "secondary": "#F59E0B",
            "background": "#FFFFFF",
            "text": "#111827",
        },
        "navigation": [
            {"label": "Home", "target_section": "hero"},
            {"label": "Products", "target_section": "catalog"},
            {"label": "Contact", "target_section": "contact"},
        ],
        "features": [
            {
                "name": "WhatsApp Ordering",
                "description": "Direct WhatsApp button for order placement",
                "priority": "must_have",
            }
        ],
        "hero_headline": "Premium Handcrafted Leather in Lahore",
        "hero_subheadline": "Export quality jackets, wallets and bags delivered to your door.",
        "contact_phone": "+923001234567",
        "contact_email": "sales@lahoreleather.com",
        "social_links": {"instagram": "https://instagram.com/lahoreleather"},
    }

    req = RequirementsContract.model_validate(data)
    assert req.project_id == "proj-123"
    assert req.version_n == 1
    assert req.palette.primary == "#1E3A8A"
    assert len(req.navigation) == 3
    assert req.features[0].priority == "must_have"

    # Test serialization to JSON and back
    serialized = req.model_dump_json()
    reconstructed = RequirementsContract.model_validate_json(serialized)
    assert reconstructed == req


def test_requirements_contract_invalid_color_hex():
    with pytest.raises(ValidationError) as exc_info:
        ColorPalette(
            primary="not-a-hex",
            secondary="#F59E0B",
            background="#FFFFFF",
            text="#111827",
        )
    assert "Invalid hex color code" in str(exc_info.value)


def test_requirements_contract_empty_navigation():
    with pytest.raises(ValidationError):
        RequirementsContract(
            project_id="proj-123",
            version_n=1,
            business_name="Test Store",
            business_type="Retail",
            palette=ColorPalette(
                primary="#112233",
                secondary="#445566",
                background="#ffffff",
                text="#000000",
            ),
            navigation=[],  # Must have at least 1
            hero_headline="Headline",
            hero_subheadline="Subheadline",
        )


def test_requirements_contract_invalid_version_number():
    with pytest.raises(ValidationError):
        RequirementsContract(
            project_id="proj-123",
            version_n=0,  # Must be >= 1
            business_name="Test Store",
            business_type="Retail",
            palette=ColorPalette(
                primary="#112233",
                secondary="#445566",
                background="#ffffff",
                text="#000000",
            ),
            navigation=[NavItem(label="Home", target_section="hero")],
            hero_headline="Headline",
            hero_subheadline="Subheadline",
        )
