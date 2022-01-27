from sqlalchemy import Table, MetaData, Integer, Column, String
from sqlalchemy.future import Engine
from sqlalchemy.orm import registry

mapper = registry()
Base = mapper.generate_base()

class GuildConfigs(Base):
    __tablename__ = "guild_configs"
    guild = Column(Integer, primary_key=True)
    prefix = Column(String, nullable=False, default="!")



def setup(engine: Engine):
    mapper.metadata.create_all(engine)
