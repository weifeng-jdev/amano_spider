import scrapy
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base

from amano_spiders.spiders.config.dbconfig import get_engine

engine = get_engine()
Base = declarative_base()
metadata = MetaData(engine)


class ChapterModel(Base):
    __tablename__ = 'chapter'
    id = Column(Integer, primary_key=True, autoincrement=True)
    comic_id = Column(String(50))
    title = Column(String(256))
    reading_url = Column(String(256))
    page_number = Column(Integer)

    def __init__(self, items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])


class ChapterItem(scrapy.Item):
    comic_id = scrapy.Field()
    title = scrapy.Field()
    reading_url = scrapy.Field()
    page_number = scrapy.Field()


Base.metadata.create_all(engine)
