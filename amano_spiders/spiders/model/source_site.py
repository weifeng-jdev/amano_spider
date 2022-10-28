from scrapy_sqlitem import SqlItem
from sqlalchemy import Integer, String, Column, MetaData
from sqlalchemy.ext.declarative import declarative_base

from amano_spiders.spiders.config.dbconfig import get_engine

engine = get_engine()
Base = declarative_base()
metadata = MetaData(engine)


class SourceSiteModel(Base):
    __tablename__ = 'source_site'
    id = Column(Integer, primary_key=True, autoincrement=True)
    site_name = Column(String(50))
    domain = Column(String(256))


class SourceSite(SqlItem):
    sqlmodel = SourceSiteModel


Base.metadata.create_all(engine)