# stdlib

# thirdparty
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

# project
from db.db_setup import Base


class PlayerModel(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, comment="Player ID")
    username = Column(String(32), nullable=False, comment="Username")
    created_at = Column(DateTime, nullable=False, server_default=func.now(), comment="Created At")
    updated_at = Column(DateTime, nullable=True, comment="Updated At")
