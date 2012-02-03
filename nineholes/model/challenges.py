# -*- coding: utf-8 -*-
"""Challenge model module."""

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, String
#from sqlalchemy.orm import relation, backref

from nineholes.model import DeclarativeBase, metadata, DBSession
from uuid import uuid4

proper_uuid = lambda: str(uuid4()).replace('-','')

class Challenge(DeclarativeBase):
    __tablename__ = 'challenges'
    
    #{ Columns
    
    id = Column(String(36), primary_key=True, default=proper_uuid)
    
    title = Column(Unicode(255), nullable=False)

    description = Column(Unicode, nullable=True)

    # If set then this is probably an imported key
    challenge_key = Column(String(36), default=None, nullable=True)
    
    start_file = Column(String, nullable=True)
    final_file = Column(String, nullable=True)

    vimrc = Column(String, nullable=True)
    #}


class Entry(DeclarativeBase):
    __tablename__ = 'entries'

    #{ Columns

    id = Column(String(36), primary_key=True, default=(lambda:str(uuid4())))

    user_id = Column(Integer, ForeignKey("tg_user.user_id"), nullable=False)
    user = relation('User', backref='entries')

    challenge_id = Column(String(36), ForeignKey("challenges.id"), nullable=False)
    challenge = relation('Challenge', backref='entries')

    solution = Column(Unicode, nullable=True)
    #}
