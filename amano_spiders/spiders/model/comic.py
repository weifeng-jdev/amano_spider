import scrapy
from sqlalchemy import Column, Integer, MetaData, String, Text, Date, Float, JSON
from sqlalchemy.orm import declarative_base

from amano_spiders.spiders.config.dbconfig import get_engine

engine = get_engine()
Base = declarative_base()
metadata = MetaData(engine)


class ComicModel(Base):
    __tablename__ = "comic"
    id = Column(Integer, primary_key=True, autoincrement=True)
    comic_id = Column(String(50))
    comic_name = Column(String(50))
    detail_url = Column(String(256))
    cover_url = Column(String(256))
    author = Column(String(20))
    category = Column(String(50))
    state = Column(Integer)
    score = Column(Float)
    tags = Column(JSON)
    describe = Column(Text)
    update_time = Column(Date)
    source_site = Column(Integer)

    def __init__(self, **items):
        for key in items:
            if hasattr(items, key):
                setattr(self, key, items[key])


class ComicItem(scrapy.Item):
    comic_id = scrapy.Field()
    comic_name = scrapy.Field()
    detail_url = scrapy.Field()
    cover_url = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
    state = scrapy.Field()
    score = scrapy.Field()
    tags = scrapy.Field()
    describe = scrapy.Field()
    update_time = scrapy.Field()
    source_site = scrapy.Field()
