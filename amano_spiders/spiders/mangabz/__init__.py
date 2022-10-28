from sqlalchemy.orm import Session

from amano_spiders.spiders.config.dbconfig import get_engine
from amano_spiders.spiders.model.source_site import SourceSite, SourceSiteModel

def mangabz_site_info():
    with Session(get_engine()) as session:
        source_site = session.query(SourceSiteModel).filter(SourceSiteModel.site_name == 'mangabz').one()
    return source_site