import json
import falcon

from keep.api import ApiResource, load_body, abort
from keep.model.util import find_tenant
from keep.model.tenant import Tenant


def _tenant_not_found():
    abort(falcon.HTTP_404, 'Unable to locate tenant.')


def _tenant_already_exists():
    abort(falcon.HTTP_400, 'Tenant already exists.')

def format_tenant(tenant):
    if not isinstance(tenant, dict):
        tenant = tenant.__dict__

    return {'id': tenant['id'],
            'tenant_id': tenant['tenant_id']}


class VersionResource(ApiResource):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({'v1': 'current'})


class TenantResource(ApiResource):

    def __init__(self, db_session):
        self.db = db_session

    def on_post(self, req, resp):
        body = load_body(req)
        tenant_id = body['tenant_id']

        tenant = find_tenant(self.db, tenant_id=tenant_id)

        if tenant:
            abort(falcon.HTTP_400, 'Tenant with tenant_id {0} '
                                   'already exists'.format(tenant_id))

        new_tenant = Tenant(tenant_id)
        self.db.add(new_tenant)
        self.db.commit()

        resp.status = falcon.HTTP_201
        resp.set_header('Location', '/v1/{0}'.format(tenant_id))

