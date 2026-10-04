from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    lead_status = postgresql.ENUM(
        "NEW", "CONTACTED", "WON", "LOST",
        name="leadstatus",
        create_type=False,
    )
    lead_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "sales_representatives",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_sales_representatives_name", "sales_representatives", ["name"])

    op.create_table(
        "leads",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("meta_lead_id", sa.String(120), nullable=False, unique=True),
        sa.Column("campaign", sa.String(160), nullable=False),
        sa.Column("ad_cost", sa.Numeric(12, 2), nullable=False),
        sa.Column("status", lead_status, nullable=False),
        sa.Column("representative_id", sa.Uuid(), sa.ForeignKey("sales_representatives.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_leads_meta_lead_id", "leads", ["meta_lead_id"])
    op.create_index("ix_leads_campaign", "leads", ["campaign"])
    op.create_index("ix_leads_representative_id", "leads", ["representative_id"])

    op.create_table(
        "sales",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("lead_id", sa.Uuid(), sa.ForeignKey("leads.id"), nullable=False, unique=True),
        sa.Column("revenue", sa.Numeric(12, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_sales_lead_id", "sales", ["lead_id"])


def downgrade():
    op.drop_table("sales")
    op.drop_table("leads")
    op.drop_table("sales_representatives")
    postgresql.ENUM(name="leadstatus").drop(op.get_bind(), checkfirst=True)
