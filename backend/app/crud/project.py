import uuid
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project


async def get_project_by_id(
    db: AsyncSession, project_id: uuid.UUID
) -> Optional[Project]:
    """Retrieve a project by its primary UUID."""
    return await db.get(Project, project_id)


async def get_projects_by_owner(
    db: AsyncSession, owner_id: uuid.UUID
) -> List[Project]:
    """List all projects owned by a specific user, sorted by creation date."""
    stmt = (
        select(Project)
        .where(Project.owner_id == owner_id)
        .order_by(Project.created_at.desc())
    )
    res = await db.execute(stmt)
    return list(res.scalars().all())


async def create_project(
    db: AsyncSession,
    owner_id: uuid.UUID,
    name: str,
    stack_profile: str = "vite-react-tailwind",
    github_repo: str = "",
) -> Project:
    """Create and persist a new project."""
    project = Project(
        owner_id=owner_id,
        name=name.strip(),
        stack_profile=stack_profile,
        github_repo=github_repo.strip(),
        current_version=0,
        current_req_version=0,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


async def update_project_version(
    db: AsyncSession,
    project_id: uuid.UUID,
    new_version: int,
    new_req_version: Optional[int] = None,
) -> Optional[Project]:
    """Update active code and requirements version pointers."""
    project = await get_project_by_id(db, project_id)
    if not project:
        return None
    project.current_version = new_version
    if new_req_version is not None:
        project.current_req_version = new_req_version
    await db.commit()
    await db.refresh(project)
    return project
