from sqlalchemy import create_engine
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


def get_engine():
    url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(settings.get('DB_USERNAME'), settings.get('DB_PASSWORD'),
                                                               settings.get('DB_HOST'), settings.get('DB_PORT'),
                                                               settings.get('DATABASE'))
    engine = create_engine(url=url, echo=True)
    return engine


__all__ = ['get_engine', 'settings']
