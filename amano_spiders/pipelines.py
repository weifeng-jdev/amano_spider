# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from amano_spiders.spiders.config.dbconfig import get_engine

class AmanoSpidersPipeline:
    def process_item(self, item, spider):
        return item

class Dmzj2Pipeline:
    def process_item(self, item, spider):
        try:
            item.commit_item(get_engine())
        except Exception as e:
            print(e.args)
        return item