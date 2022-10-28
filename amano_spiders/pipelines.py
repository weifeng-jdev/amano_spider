# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy.orm import Session

from amano_spiders.spiders.config.dbconfig import get_engine
from amano_spiders.spiders.model.chapter import ChapterItem, ChapterModel
from amano_spiders.spiders.model.comic import ComicItem
from amano_spiders import comic_id_dict


class AmanoSpidersPipeline:
    def process_item(self, item, spider):
        return item


class ComicSpiderPipeline:
    def process_item(self, item, spider):
        if isinstance(item, ComicItem):
            try:
                # save or update
                id = item.commit_item(get_engine())
                comic_id = item.comic_id
                comic_id_dict[comic_id] = id
            except Exception as e:
                print(e.args)
            finally:
                return
        return item


class ChapterPipeline:
    def process_item(self, item, spider):
        if isinstance(item, ChapterItem):
            try:
                chapter = ChapterModel(item)
                with Session(bind=get_engine()) as seesion:
                    seesion.add(chapter)
                    seesion.commit()
            except Exception as e:
                print(e.args)
            finally:
                return
