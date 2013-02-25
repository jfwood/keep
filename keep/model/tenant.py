# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# Copyright 2011 Justin Santa Barbara
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Generic Node base class for all workers that run on hosts."""

from base import Base
from sqlalchemy import Table, Column, String
from sqlalchemy import Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base, declared_attr


class Tenant(Base):
    """
    Tenants are users that wish to store secret information within Cloud Keep.
    """

    tenant_id = Column(String)
    # secrets = relationship('Secret', secondary=_secrets)

    def __init__(self, tenant_id):
        self.tenant_id = tenant_id
#    def __init__(self, tenant_id, secrets=[]):
#        self.tenant_id = tenant_id
#        self.secrets = secrets

