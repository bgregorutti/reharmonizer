"""add melody upload tables

Revision ID: 001_melody_upload
Revises:
Create Date: 2025-12-31

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_melody_upload'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create melody_uploads table
    op.create_table(
        'melody_uploads',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('file_name', sa.String(length=255), nullable=False),
        sa.Column('file_type', sa.String(length=10), nullable=False),
        sa.Column('file_path', sa.String(length=512), nullable=False),
        sa.Column('detected_key', sa.String(length=20), nullable=True),
        sa.Column('time_signature', sa.String(length=10), nullable=True),
        sa.Column('tempo', sa.Integer(), nullable=True),
        sa.Column('measures', sa.Integer(), nullable=True),
        sa.Column('duration', sa.Float(), nullable=True),
        sa.Column('melody_notes', sa.JSON(), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_melody_uploads_id'), 'melody_uploads', ['id'], unique=False)

    # Create harmonization_results table
    op.create_table(
        'harmonization_results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('melody_upload_id', sa.Integer(), nullable=False),
        sa.Column('style', sa.String(length=20), nullable=False),
        sa.Column('chord_progression', sa.JSON(), nullable=False),
        sa.Column('pattern_applied', sa.String(length=100), nullable=True),
        sa.Column('score', sa.Float(), nullable=True),
        sa.Column('options', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_harmonization_results_id'), 'harmonization_results', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_harmonization_results_id'), table_name='harmonization_results')
    op.drop_table('harmonization_results')
    op.drop_index(op.f('ix_melody_uploads_id'), table_name='melody_uploads')
    op.drop_table('melody_uploads')
