# encoding: utf-8
import logging
from uuid import uuid4

from sqlalchemy import or_, func, UnicodeText, DateTime, Unicode, Boolean, Column
from sqlalchemy.ext.declarative import declarative_base

import ckan.model as model

from ckanext.datarequests import constants

log = logging.getLogger(__name__)
Base = declarative_base()


class DataRequest(Base):
    __tablename__ = u'datarequests'

    id = Column(UnicodeText, primary_key=True, default=uuid4)
    user_id = Column(UnicodeText, primary_key=False, default=u'')
    title = Column(Unicode(constants.NAME_MAX_LENGTH), primary_key=True, default=u'')
    description = Column(Unicode(constants.DESCRIPTION_MAX_LENGTH), primary_key=False, default=u'')
    organization_id = Column(UnicodeText, primary_key=False, default=None)
    open_time = Column(DateTime, primary_key=False, default=None)
    accepted_dataset_id = Column(UnicodeText, primary_key=False, default=None)
    close_time = Column(DateTime, primary_key=False, default=None)
    closed = Column(Boolean, primary_key=False, default=False)
    close_circumstance = Column(Unicode(constants.CLOSE_CIRCUMSTANCE_MAX_LENGTH), primary_key=False, default=u'')
    approx_publishing_date = Column(DateTime, primary_key=False, default=None)


    @classmethod
    def get(cls, **kw):
        '''Finds all the instances required.'''
        query = model.Session.query(cls).autoflush(False)
        return query.filter_by(**kw).all()

    @classmethod
    def datarequest_exists(cls, title):
        '''Returns true if there is a Data Request with the same title (case insensitive)'''
        query = model.Session.query(cls).autoflush(False)
        return query.filter(func.lower(cls.title) == func.lower(title)).first() is not None

    @classmethod
    def get_ordered_by_date(cls, organization_id=None, user_id=None, closed=None, q=None, desc=False):
        '''Personalized query'''
        query = model.Session.query(cls).autoflush(False)

        params = {}

        if organization_id is not None:
            params['organization_id'] = organization_id

        if user_id is not None:
            params['user_id'] = user_id

        if closed is not None:
            params['closed'] = closed

        if q is not None:
            search_expr = '%{0}%'.format(q)
            query = query.filter(or_(cls.title.ilike(search_expr), cls.description.ilike(search_expr)))

        order_by_filter = cls.open_time.desc() if desc else cls.open_time.asc()

        return query.filter_by(**params).order_by(order_by_filter).all()

    @classmethod
    def get_open_datarequests_number(cls):
        '''Returns the number of data requests that are open'''
        return model.Session.query(func.count(cls.id)).filter_by(closed=False).scalar()


class Comment(Base):
    __tablename__ = u'datarequests_comments'

    id = Column(UnicodeText, primary_key=True, default=uuid4)
    user_id = Column(UnicodeText, primary_key=False, default=u'')
    datarequest_id = Column(UnicodeText, primary_key=True, default=uuid4)
    time = Column(DateTime, primary_key=True, default=u'')
    comment = Column(Unicode(constants.COMMENT_MAX_LENGTH), primary_key=False, default=u'')

    @classmethod
    def get(cls, **kw):
        '''Finds all the instances required.'''
        query = model.Session.query(cls).autoflush(False)
        return query.filter_by(**kw).all()

    @classmethod
    def get_ordered_by_date(cls, datarequest_id, desc=False):
        '''Personalized query'''
        query = model.Session.query(cls).autoflush(False)
        order_by_filter = cls.time.desc() if desc else cls.time.asc()
        return query.filter_by(datarequest_id=datarequest_id).order_by(order_by_filter).all()

    @classmethod
    def get_comment_datarequests_number(cls, **kw):
        '''
        Returned the number of comments of a data request
        '''
        return model.Session.query(func.count(cls.id)).filter_by(**kw).scalar()


class DataRequestFollower(Base):
    __tablename__ = u'datarequests_followers'

    id = Column(UnicodeText, primary_key=True, default=uuid4)
    user_id = Column(UnicodeText, primary_key=False, default=u'')
    datarequest_id = Column(UnicodeText, primary_key=True, default=uuid4)
    time = Column(DateTime, primary_key=True, default=u'')

    @classmethod
    def get(cls, **kw):
        '''Finds all the instances required.'''
        query = model.Session.query(cls).autoflush(False)
        return query.filter_by(**kw).all()

    @classmethod
    def get_datarequest_followers_number(cls, **kw):
        '''
        Returned the number of followers of a data request
        '''
        return model.Session.query(func.count(cls.id)).filter_by(**kw).scalar()
