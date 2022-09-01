"""empty message

Revision ID: 7190dab1b927
Revises: 
Create Date: 2022-08-31 18:31:28.348257

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7190dab1b927'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('fixtures', 'livestream',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('season', 'season_tag',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    op.alter_column('teams', 'cat_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('teams', 'subcat_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.create_foreign_key(None, 'teams', 'sub_categories', ['subcat_id'], ['sub_id'])
    op.create_foreign_key(None, 'teams', 'categories', ['cat_id'], ['cat_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'teams', type_='foreignkey')
    op.drop_constraint(None, 'teams', type_='foreignkey')
    op.alter_column('teams', 'subcat_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('teams', 'cat_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('season', 'season_tag',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
    op.alter_column('fixtures', 'livestream',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###
