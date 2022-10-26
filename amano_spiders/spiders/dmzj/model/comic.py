from sqlalchemy import Column, Integer, MetaData, String, Text, Table
from amano_spiders.spiders.config.dbconfig import get_engine
from scrapy_sqlitem import SqlItem
from scrapy_sqlitem.sqlitem import SqlAlchemyItemMeta

metadata = MetaData(get_engine())

class ComicItem(SqlItem, metaclass=SqlAlchemyItemMeta):
    sqlmodel = Table("comic", metadata,
                        Column('id', Integer, primary_key = True, autoincrement = True),
                        Column('comic_name', String(50)),
                        Column('detail_url',Text),
                        Column('cover_url', Text)
                    )
    sqlmodel.create(checkfirst = True)