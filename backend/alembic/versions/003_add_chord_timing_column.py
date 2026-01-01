"""add chord_timing column to harmonization_results

Revision ID: 003_chord_timing
Revises: 002_chord_progressions
Create Date: 2026-01-01

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003_chord_timing'
down_revision = '002_chord_progressions'
branch_labels = None
depends_on = None


def upgrade():
    # Add chord_timing column to harmonization_results table
    op.add_column(
        'harmonization_results',
        sa.Column('chord_timing', sa.JSON(), nullable=True)
    )


def downgrade():
    # Remove chord_timing column
    op.drop_column('harmonization_results', 'chord_timing')
