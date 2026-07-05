"""Initial schema

Revision ID: 20260704_0001
Revises:
Create Date: 2026-07-04
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "20260704_0001"
down_revision = None
branch_labels = None
depends_on = None


def run_enum(name: str, values: list[str]) -> sa.Enum:
    return sa.Enum(*values, name=name)


def upgrade() -> None:
    product_category = run_enum(
        "product_category",
        ["tops", "bottoms", "dresses", "shoes", "bags", "jewelry", "accessories"],
    )
    outfit_status = run_enum("outfit_status", ["draft", "generated", "published"])
    board_status = run_enum("board_status", ["queued", "generated", "failed"])
    campaign_type = run_enum("campaign_type", ["daily", "weekly", "seasonal"])
    schedule_status = run_enum("schedule_status", ["draft", "scheduled", "published", "failed"])

    bind = op.get_bind()
    product_category.create(bind, checkfirst=True)
    outfit_status.create(bind, checkfirst=True)
    board_status.create(bind, checkfirst=True)
    campaign_type.create(bind, checkfirst=True)
    schedule_status.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("category", product_category, nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("image_url", sa.String(length=1024), nullable=False),
        sa.Column("affiliate_link", sa.String(length=1024), nullable=False),
        sa.Column("color", sa.String(length=128), nullable=False),
        sa.Column("style_tags", sa.JSON(), nullable=False),
        sa.Column("brand", sa.String(length=255), nullable=False),
        sa.Column("occasion_tags", sa.JSON(), nullable=False),
        sa.Column("color_palette", sa.JSON(), nullable=False),
        sa.Column("aesthetic", sa.String(length=128), nullable=False),
        sa.Column("season", sa.String(length=64), nullable=False),
        sa.Column("ai_summary", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "outfits",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("keywords", sa.JSON(), nullable=False),
        sa.Column("pinterest_seo_title", sa.String(length=255), nullable=False),
        sa.Column("pinterest_description", sa.Text(), nullable=False),
        sa.Column("suggested_board_name", sa.String(length=255), nullable=False),
        sa.Column("aesthetic", sa.String(length=128), nullable=False),
        sa.Column("season", sa.String(length=64), nullable=False),
        sa.Column("occasion", sa.String(length=64), nullable=False),
        sa.Column("status", outfit_status, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "outfit_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("outfit_id", sa.Integer(), sa.ForeignKey("outfits.id", ondelete="CASCADE"), nullable=False),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("slot", sa.String(length=64), nullable=False),
    )
    op.create_table(
        "generated_boards",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("outfit_id", sa.Integer(), sa.ForeignKey("outfits.id"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("image_url", sa.String(length=1024), nullable=False),
        sa.Column("storage_key", sa.String(length=255), nullable=False),
        sa.Column("status", board_status, nullable=False),
        sa.Column("width", sa.Integer(), nullable=False),
        sa.Column("height", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "pinterest_boards",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("remote_id", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "pinterest_pins",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("generated_board_id", sa.Integer(), sa.ForeignKey("generated_boards.id"), nullable=False),
        sa.Column("pinterest_board_id", sa.Integer(), sa.ForeignKey("pinterest_boards.id"), nullable=False),
        sa.Column("remote_id", sa.String(length=255), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("impressions", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("clicks", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("saves", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("outbound_clicks", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "scheduled_posts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("generated_board_id", sa.Integer(), sa.ForeignKey("generated_boards.id"), nullable=False),
        sa.Column("pinterest_board_id", sa.Integer(), sa.ForeignKey("pinterest_boards.id"), nullable=True),
        sa.Column("campaign_type", campaign_type, nullable=False),
        sa.Column("scheduled_for", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", schedule_status, nullable=False),
        sa.Column("caption", sa.Text(), nullable=False),
        sa.Column("hashtags", sa.JSON(), nullable=False),
        sa.Column("affiliate_earnings", sa.Float(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("scheduled_posts")
    op.drop_table("pinterest_pins")
    op.drop_table("pinterest_boards")
    op.drop_table("generated_boards")
    op.drop_table("outfit_items")
    op.drop_table("outfits")
    op.drop_table("products")
    op.drop_table("users")

