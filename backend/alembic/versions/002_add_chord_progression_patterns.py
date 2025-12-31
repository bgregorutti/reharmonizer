"""add chord progression patterns table

Revision ID: 002_chord_progressions
Revises: 001_melody_upload
Create Date: 2025-12-31

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_chord_progressions'
down_revision = '001_melody_upload'
branch_labels = None
depends_on = None


def upgrade():
    # Create chord_progression_patterns table
    op.create_table(
        'chord_progression_patterns',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('style', sa.String(length=20), nullable=False),
        sa.Column('roman_numeral_sequence', sa.JSON(), nullable=False),
        sa.Column('example_chords', sa.JSON(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('usage_context', sa.Text(), nullable=True),
        sa.Column('popularity_score', sa.Float(), nullable=True),
        sa.Column('min_length', sa.Integer(), nullable=True),
        sa.Column('max_length', sa.Integer(), nullable=True),
        sa.Column('is_repeatable', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chord_progression_patterns_id'), 'chord_progression_patterns', ['id'], unique=False)
    op.create_index(op.f('ix_chord_progression_patterns_style'), 'chord_progression_patterns', ['style'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_chord_progression_patterns_style'), table_name='chord_progression_patterns')
    op.drop_index(op.f('ix_chord_progression_patterns_id'), table_name='chord_progression_patterns')
    op.drop_table('chord_progression_patterns')
