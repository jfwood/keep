import falcon

from keep.apiresources import *

from config import config
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from keep.model.tenant import Base

"""
Locally scoped db session
"""
_Session = scoped_session(sessionmaker())
_engine = None


def db_session():
    return _Session


def _engine_from_config(configuration):
    configuration = dict(configuration)
    url = configuration.pop('url')

    return create_engine(url, **configuration)


def init_tenant_model():
    _engine = _engine_from_config(config['sqlalchemy'])
    Base.metadata.create_all(_engine)
    _Session.bind = _engine


# Initialize the data model
init_tenant_model()

# Resources
versions = VersionResource()
tenant = TenantResource(db_session())

# Routing
application = api = falcon.API()

api.add_route('/', versions)
api.add_route('/v1/tenant', tenant)

