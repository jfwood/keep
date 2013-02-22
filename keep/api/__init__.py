# Copyright 2010-2011 OpenStack LLC.
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

"""
API handler for Cloud Keep
"""


import json
import falcon


class ApiResource(object):
    """
    Base class for API resources
    """
    pass


def abort(status=falcon.HTTP_500, message=None):
    """
    Helper function for aborting an API request process. Useful for error
    reporting and expcetion handling.
    """
    raise falcon.HTTPError(status, message)


def load_body(req, required=[]):
    """
    Helper function for loading an HTTP request body from JSON into a
    Python dictionary
    """
    try:
        raw_json = req.stream.read()

    except Exception:
        abort(falcon.HTTP_500, 'Read Error')

    try:
        parsed_body = json.loads(raw_json, 'utf-8')
    except ValueError as ve:
        abort(falcon.HTTP_400, 'Malformed JSON')

    return parsed_body
