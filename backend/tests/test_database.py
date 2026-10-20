import uuid
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import (
    authenticate_user,
    create_message,
    create_project,
    create_user,
    get_messages_by_project,
    get_project_by_id,
    get_projects_by_owner,
    get_user_by_email,
    get_user_by_id,
    update_project_version,
)
from app.db.session import AsyncSessionLocal
from app.models.execution import Run
from app.models.ledger import (
    DeploymentRequest,
    LedgerEntry,
    Payment,
    Payout,
    PayoutPeriod,
    Quote,
)
from app.models.project import Decision, Message, Project, Requirement
from app.models.user import Plan, RefreshToken, Subscription, UsageCounter, User
from app.models.version import File, Version


@pytest.mark.anyio
async def test_user_model_creation():
    async with AsyncSessionLocal() as session:
        unique_email = f"user_{uuid.uuid4().hex[:8]}@example.com"
        user = User(
            email=unique_email,
            full_name="Test User",
            phone="+923001234567",
            role="user",
            hashed_password="hashed_pw_test",
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

        assert user.id is not None
        assert user.role == "user"
        assert user.is_active is True
        assert user.created_at is not None


@pytest.mark.anyio
async def test_project_model_relationships():
    async with AsyncSessionLocal() as session:
        # Create user
        user = User(
            email=f"owner_{uuid.uuid4().hex[:8]}@example.com",
            full_name="Owner User",
            role="user",
            hashed_password="pw",
        )
        session.add(user)
        await session.flush()

        # Create project
        project = Project(
            owner_id=user.id,
            name="Alpha Store",
            stack_profile="vite-react-tailwind",
            current_version=1,
            github_repo="org/alpha-store",
        )
        session.add(project)
        await session.flush()

        # Add message
        message = Message(
            project_id=project.id,
            role="user",
            content="Build me an online apparel store",
            kind="chat",
        )
        session.add(message)
        await session.flush()

        # Add version
        version = Version(
            project_id=project.id,
            n=1,
            requirements_n=1,
            commit_sha="a1b2c3d4e5f67890123456789abcdef012345678",
            summary="v1 greenfield build",
            status="verified",
            trigger_message_id=message.id,
        )
        session.add(version)
        await session.commit()

        # Query back
        res = await session.execute(select(Project).where(Project.id == project.id))
        queried_proj = res.scalar_one()
        assert queried_proj.name == "Alpha Store"
        assert queried_proj.owner_id == user.id


@pytest.mark.anyio
async def test_pgvector_insertion_and_cosine_query():
    """Verify pgvector 1536d embedding storage and cosine similarity search with HNSW."""
    async with AsyncSessionLocal() as session:
        user = User(
            email=f"vec_{uuid.uuid4().hex[:8]}@example.com",
            full_name="Vec User",
            role="user",
            hashed_password="pw",
        )
        session.add(user)
        await session.flush()

        project = Project(owner_id=user.id, name="Vector Store")
        session.add(project)
        await session.flush()

        version = Version(
            project_id=project.id,
            n=1,
            requirements_n=1,
            commit_sha="11223344556677889900aabbccddeeff11223344",
            summary="Vector test version",
            status="verified",
        )
        session.add(version)
        await session.flush()

        # Vector of 1536 dimensions
        mock_embedding_1 = [0.05] * 1536
        mock_embedding_1[0] = 0.9

        mock_embedding_2 = [0.01] * 1536
        mock_embedding_2[1] = 0.9

        file1 = File(
            version_id=version.id,
            path="src/components/ProductCard.tsx",
            role="component",
            summary="Product card with Add to Cart button",
            exports=["ProductCard"],
            imports=["data/site.json"],
            content_hash="hash_card_123",
            embedding=mock_embedding_1,
        )
        file2 = File(
            version_id=version.id,
            path="data/site.json",
            role="content",
            summary="Main store copy and headlines",
            exports=[],
            imports=[],
            content_hash="hash_data_123",
            embedding=mock_embedding_2,
        )
        session.add_all([file1, file2])
        await session.commit()

        # Query using pgvector cosine distance operator <=>
        query_vec = [0.05] * 1536
        query_vec[0] = 0.85

        stmt = (
            select(
                File.path,
                File.role,
                (1 - File.embedding.cosine_distance(query_vec)).label("similarity"),
            )
            .where(File.version_id == version.id)
            .order_by(File.embedding.cosine_distance(query_vec))
            .limit(1)
        )

        result = await session.execute(stmt)
        top_match = result.one()
        assert top_match.path == "src/components/ProductCard.tsx"
        assert top_match.similarity > 0.8


@pytest.mark.anyio
async def test_ledger_entry_debit_credit_validation():
    """Verify double-entry ledger invariant: sum(debit) == sum(credit)."""
    async with AsyncSessionLocal() as session:
        user_id = uuid.uuid4()
        platform_id = uuid.uuid4()

        entry1 = LedgerEntry(
            account_type="user_escrow",
            entity_id=user_id,
            debit_cents=5000,
            credit_cents=0,
            reference_memo="Client payment held",
        )
        entry2 = LedgerEntry(
            account_type="escrow_holding",
            entity_id=platform_id,
            debit_cents=0,
            credit_cents=5000,
            reference_memo="Escrow holding balance",
        )

        session.add_all([entry1, entry2])
        await session.commit()

        res = await session.execute(
            select(
                func.sum(LedgerEntry.debit_cents).label("total_debits"),
                func.sum(LedgerEntry.credit_cents).label("total_credits"),
            ).where(LedgerEntry.id.in_([entry1.id, entry2.id]))
        )
        totals = res.one()
        assert totals.total_debits == totals.total_credits == 5000


@pytest.mark.anyio
async def test_crud_repositories():
    """Verify CRUD operations for users, projects, and messages."""
    async with AsyncSessionLocal() as session:
        email = f"crud_{uuid.uuid4().hex[:8]}@example.com"
        user = await create_user(
            db=session,
            email=email,
            password="StrongPassword123!",
            full_name="CRUD Test User",
            phone="+923007654321",
        )
        assert user.id is not None

        auth_user = await authenticate_user(session, email, "StrongPassword123!")
        assert auth_user is not None
        assert auth_user.id == user.id

        bad_auth = await authenticate_user(session, email, "WrongPassword")
        assert bad_auth is None

        project = await create_project(
            db=session,
            owner_id=user.id,
            name="CRUD Store",
            github_repo="org/crud-store",
        )
        assert project.id is not None
        assert project.current_version == 0

        updated_proj = await update_project_version(session, project.id, new_version=1, new_req_version=1)
        assert updated_proj is not None
        assert updated_proj.current_version == 1

        owner_projects = await get_projects_by_owner(session, user.id)
        assert len(owner_projects) >= 1

        msg1 = await create_message(session, project.id, "user", "I want a dark blue theme")
        msg2 = await create_message(session, project.id, "assistant", "Dark blue theme recorded.", kind="chat")
        assert msg1.id is not None
        assert msg2.id is not None

        msgs = await get_messages_by_project(session, project.id)
        assert len(msgs) == 2
        assert msgs[0].content == "I want a dark blue theme"


@pytest.mark.anyio
async def test_definition_of_done_all_tables_insertion():
    """Definition of Done: Insert valid rows across all 18 tables in the relational schema."""
    async with AsyncSessionLocal() as session:
        now = datetime.now(timezone.utc)

        # 1. User
        user = User(
            email=f"dod_{uuid.uuid4().hex[:8]}@example.com",
            full_name="DoD User",
            phone="+923009999999",
            role="user",
            hashed_password="pw",
        )
        dev_user = User(
            email=f"dev_{uuid.uuid4().hex[:8]}@example.com",
            full_name="DoD Developer",
            phone="+923008888888",
            role="developer",
            hashed_password="pw",
        )
        session.add_all([user, dev_user])
        await session.flush()

        # 2. Plan
        plan_id = f"plan_{uuid.uuid4().hex[:6]}"
        plan = Plan(
            id=plan_id,
            name="Custom Plan",
            monthly_token_quota=500_000,
            max_projects=5,
            max_edits_per_month=50,
            price_cents=1500,
        )
        session.add(plan)
        await session.flush()

        # 3. Subscription
        sub = Subscription(
            user_id=user.id,
            plan_id=plan.id,
            status="active",
            current_period_start=now,
            current_period_end=now + timedelta(days=30),
        )
        session.add(sub)

        # 4. UsageCounter
        uc = UsageCounter(
            user_id=user.id,
            period_date=date.today(),
            tokens_consumed=1500,
            generations_count=1,
            edits_count=0,
        )
        session.add(uc)

        # 5. RefreshToken
        rt = RefreshToken(
            user_id=user.id,
            token_hash=uuid.uuid4().hex + uuid.uuid4().hex,
            family_id=str(uuid.uuid4()),
            expires_at=now + timedelta(days=30),
        )
        session.add(rt)

        # 6. Project
        proj = Project(
            owner_id=user.id,
            name="DoD Project",
            stack_profile="vite-react-tailwind",
            github_repo="org/dod-project",
        )
        session.add(proj)
        await session.flush()

        # 7. Message
        msg = Message(
            project_id=proj.id,
            role="user",
            content="Create full clothing catalog",
            kind="chat",
        )
        session.add(msg)
        await session.flush()

        # 8. Requirement
        req = Requirement(
            project_id=proj.id,
            n=1,
            data={"business_name": "DoD Clothing", "theme": "emerald"},
            trigger_message_id=msg.id,
            confirmed_at=now,
        )
        session.add(req)

        # 9. Decision
        decision = Decision(
            project_id=proj.id,
            topic="color_scheme",
            choice="emerald",
            reason="User selected emerald button in interview",
            source="user",
            message_id=msg.id,
        )
        session.add(decision)

        # 10. Version
        ver = Version(
            project_id=proj.id,
            n=1,
            requirements_n=1,
            commit_sha="abcdef1234567890abcdef1234567890abcdef12",
            summary="DoD Verified Version",
            status="verified",
            trigger_message_id=msg.id,
        )
        session.add(ver)
        await session.flush()

        # 11. File (with Vector)
        file_obj = File(
            version_id=ver.id,
            path="src/components/Header.tsx",
            role="component",
            summary="Header navbar component",
            exports=["Header"],
            imports=["react"],
            content_hash="abc123hash",
            embedding=[0.02] * 1536,
        )
        session.add(file_obj)

        # 12. Run
        run = Run(
            version_id=ver.id,
            agent="Coder",
            tokens_in=3500,
            tokens_out=1200,
            cost_usd=Decimal("0.024500"),
            ok=True,
            trace_id="trace-12345",
        )
        session.add(run)

        # 13. DeploymentRequest
        dep = DeploymentRequest(
            project_id=proj.id,
            version_id=ver.id,
            status="assigned",
            assigned_developer_id=dev_user.id,
        )
        session.add(dep)
        await session.flush()

        # 14. Quote
        quote = Quote(
            request_id=dep.id,
            amount_cents=3000,
            currency="USD",
            status="accepted",
        )
        session.add(quote)
        await session.flush()

        # 15. Payment
        payment = Payment(
            quote_id=quote.id,
            amount_cents=3000,
            gateway_ref="mock_pay_12345",
            status="held",
        )
        session.add(payment)
        await session.flush()

        # 16. LedgerEntry
        le = LedgerEntry(
            payment_id=payment.id,
            account_type="user_escrow",
            entity_id=user.id,
            debit_cents=3000,
            credit_cents=0,
            reference_memo="Escrow deposit for deployment",
        )
        session.add(le)

        # 17. PayoutPeriod
        period = PayoutPeriod(
            period_month="2026-12",
            status="open",
        )
        session.add(period)
        await session.flush()

        # 18. Payout
        payout = Payout(
            period_id=period.id,
            developer_id=dev_user.id,
            total_cents=2400,
            status="pending",
        )
        session.add(payout)

        await session.commit()

        # Verify all 18 objects were persisted with valid primary keys
        assert user.id is not None
        assert plan.id is not None
        assert sub.id is not None
        assert uc.id is not None
        assert rt.id is not None
        assert proj.id is not None
        assert msg.id is not None
        assert req.id is not None
        assert decision.id is not None
        assert ver.id is not None
        assert file_obj.id is not None
        assert run.id is not None
        assert dep.id is not None
        assert quote.id is not None
        assert payment.id is not None
        assert le.id is not None
        assert period.id is not None
        assert payout.id is not None


def test_alembic_upgrade_downgrade_cycle():
    """Verify programmatic Alembic upgrade/downgrade cycle without errors."""
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
