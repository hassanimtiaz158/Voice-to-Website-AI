import pytest
from pydantic import ValidationError

from contracts.plan import FileAction, PlanContract


def test_plan_contract_file_roles_enum():
    action = FileAction(
        path="src/components/Hero.tsx",
        role="component",
        action="create",
        description="Hero banner with CTA",
        imports=["react", "lucide-react"],
        exports=["Hero"],
    )
    assert action.role == "component"
    assert action.action == "create"

    with pytest.raises(ValidationError):
        FileAction(
            path="src/components/Hero.tsx",
            role="invalid_role",  # Invalid enum value
            action="create",
            description="Hero banner",
        )

    with pytest.raises(ValidationError):
        FileAction(
            path="src/components/Hero.tsx",
            role="component",
            action="destroy",  # Invalid action enum
            description="Hero banner",
        )


def test_plan_contract_valid_lifecycle():
    plan = PlanContract(
        project_id="proj-456",
        stack_profile="vite-react-tailwind",
        files=[
            FileAction(
                path="data/site.json",
                role="content",
                action="create",
                description="Central website copy",
                exports=[],
            ),
            FileAction(
                path="src/components/Navbar.tsx",
                role="component",
                action="create",
                description="Responsive navigation bar",
                exports=["Navbar"],
            ),
        ],
        estimated_tokens=4500,
    )
    assert plan.project_id == "proj-456"
    assert len(plan.files) == 2
    assert plan.estimated_tokens == 4500

    serialized = plan.model_dump_json()
    reloaded = PlanContract.model_validate_json(serialized)
    assert reloaded == plan


def test_plan_contract_empty_files_rejected():
    with pytest.raises(ValidationError):
        PlanContract(
            project_id="proj-456",
            files=[],  # Must have at least one file
        )
