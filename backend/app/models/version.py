import uuid
from datetime import datetime
from typing import List, Optional

import sqlalchemy as sa
from pgvector.sqlalchemy import Vector
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Version(Base):
    __tablename__ = "versions"
    __table_args__ = (
        UniqueConstraint("project_id", "n", name="unique_project_version"),
        CheckConstraint("status IN ('draft', 'verified', 'failed', 'rolled_back')", name="check_version_status"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid()
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    n: Mapped[int] = mapped_column(Integer, nullable=False)
    parent_n: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    requirements_n: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_message_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("messages.id"), nullable=True
    )
    commit_sha: Mapped[str] = mapped_column(String(40), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="draft", server_default="draft")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="versions")
    files: Mapped[List["File"]] = relationship("File", back_populates="version", cascade="all, delete-orphan")
    runs: Mapped[List["Run"]] = relationship("Run", back_populates="version", cascade="all, delete-orphan")
    deployment_requests: Mapped[List["DeploymentRequest"]] = relationship("DeploymentRequest", back_populates="version")


class File(Base):
    __tablename__ = "files"
    __table_args__ = (
        UniqueConstraint("version_id", "path", name="unique_version_file_path"),
        CheckConstraint(
            "role IN ('component', 'content', 'page', 'style', 'config', 'api')",
            name="check_file_role",
        ),
        Index(
            "idx_files_embedding",
            "embedding",
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid()
    )
    version_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("versions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    path: Mapped[str] = mapped_column(String(500), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    exports: Mapped[List[str]] = mapped_column(
        ARRAY(String), nullable=False, default=list, server_default="{}"
    )
    imports: Mapped[List[str]] = mapped_column(
        ARRAY(String), nullable=False, default=list, server_default="{}"
    )
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    embedding: Mapped[Optional[List[float]]] = mapped_column(Vector(1536), nullable=True)

    version: Mapped["Version"] = relationship("Version", back_populates="files")
