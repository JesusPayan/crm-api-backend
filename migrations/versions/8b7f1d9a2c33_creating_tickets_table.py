"""creating tickets table

Revision ID: 8b7f1d9a2c33
Revises: 30d6cd38a105
Create Date: 2025-09-10 23:45:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b7f1d9a2c33'   # <- este ID debe ser único
down_revision = '30d6cd38a105'  # <- último ID válido en tu proyecto
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tickets',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='open'),
        sa.Column('priority', sa.String(length=50), nullable=False, server_default='medium'),
        sa.Column('client_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['client_id'], ['client_sumary.id'], name='fk_ticket_client'),
    )


def downgrade():
    op.drop_table('tickets')