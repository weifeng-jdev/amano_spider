from sqlalchemy import Column, Integer, MetaData, String, Text, Table, Date, Float, JSON
from amano_spiders.spiders.config.dbconfig import get_engine
from scrapy_sqlitem import SqlItem
from scrapy_sqlitem.sqlitem import SqlAlchemyItemMeta

metadata = MetaData(get_engine())


class ComicItem(SqlItem, metaclass=SqlAlchemyItemMeta):
    sqlmodel = Table("comic", metadata,
                     Column('id', Integer, primary_key=True, autoincrement=True),
                     Column('comic_id', Integer),
                     Column('comic_name', String(50)),
                     Column('detail_url', String(256)),
                     Column('cover_url', String(256)),
                     Column('author', String(20)),
                     Column('category', String(50)),
                     Column('state', Integer),
                     Column('score', Float),
                     Column("tags", JSON),
                     Column('describe', Text),
                     Column("update_time", Date),
                     )
    sqlmodel.create(checkfirst=True)
