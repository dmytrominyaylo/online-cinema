from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = 'f28acf922216'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('orders',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('total_amount', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('price_at_order', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('status', sa.Enum('successful', 'canceled', 'refunded', name='paymentstatus'), nullable=False),
    sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('external_payment_id', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payment_items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('payment_id', sa.Integer(), nullable=False),
    sa.Column('order_item_id', sa.Integer(), nullable=False),
    sa.Column('price_at_payment', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.ForeignKeyConstraint(['order_item_id'], ['order_items.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['payment_id'], ['payments.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('payment_items')
    op.drop_table('payments')
    op.drop_table('order_items')
    op.drop_table('orders')
