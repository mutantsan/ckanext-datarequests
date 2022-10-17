"""init migration

Revision ID: 6fad95038443
Revises:
Create Date: 2022-10-17 11:23:23.024470

"""
from uuid import uuid4

import sqlalchemy as sa
from alembic import op

from ckanext.datarequests import constants

# revision identifiers, used by Alembic.
revision = '6fad95038443'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'datarequests',
        sa.Column('id', sa.UnicodeText, primary_key=True, default=uuid4),
        sa.Column('title', sa.Unicode(constants.NAME_MAX_LENGTH)),
        sa.Column('description', sa.Unicode(constants.DESCRIPTION_MAX_LENGTH), primary_key=False, default=u""),
        sa.Column('organization_id', sa.UnicodeText, primary_key=False, default=None),
        sa.Column('open_time', sa.DateTime, primary_key=False, default=None),
        sa.Column('accepted_dataset_id', sa.UnicodeText, primary_key=False, default=None),
        sa.Column('close_time', sa.DateTime, primary_key=False, default=None),
        sa.Column('closed', sa.Boolean, primary_key=False, default=False),
        sa.Column('close_circumstance', sa.Unicode(constants.CLOSE_CIRCUMSTANCE_MAX_LENGTH), primary_key=False, default=u""),
        sa.Column('approx_publishing_date', sa.DateTime, primary_key=False, default=None),
    )

    op.create_table(
        'datarequests_comments',
        sa.Column('id', sa.UnicodeText, primary_key=True, default=uuid4),
        sa.Column('user_id', sa.UnicodeText, primary_key=False, default=u""),
        sa.Column('datarequest_id', sa.UnicodeText, primary_key=True, default=uuid4),
        sa.Column('time', sa.DateTime, primary_key=True, default=u""),
        sa.Column('comment', sa.Unicode(constants.COMMENT_MAX_LENGTH), default=u""),
    )

    op.create_table(
        'datarequests_followers',
        sa.Column('id', sa.UnicodeText, primary_key=True, default=uuid4),
        sa.Column('user_id', sa.UnicodeText, primary_key=False, default=u""),
        sa.Column('datarequest_id', sa.UnicodeText, primary_key=True, default=uuid4),
        sa.Column('time', sa.DateTime, primary_key=True, default=u""),
    )


def downgrade():
    op.drop_table('datarequests')
    op.drop_table('datarequests_comments')
    op.drop_table('datarequests_followers')
