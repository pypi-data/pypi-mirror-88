# encoding: utf-8

u"""
============================================================
Changes the uri by modifying, removing or adding parameters
------------------------------------------------------------
Filter: string to match in uri e.g. google
Parameters: new value e.g. .co.uk
------------------------------------------------------------
"""

import requests
import logging_helper
from pyhttpintercept.intercept.handlers.support import (decorate_uri_modifier_for_json_parameters,
                                                        decorate_uri_modifier_for_filter)
from urlparse import urlparse, urlunparse
logging = logging_helper.setup_logging()


@decorate_uri_modifier_for_json_parameters
@decorate_uri_modifier_for_filter
def modify(uri,
           modifier):
    if modifier.filter in uri:
        parsed_uri = requests.utils.urlparse(uri)
        params = dict(param.split('=') for param in parsed_uri.query.split('&'))
        params.update(modifier.parameters['params'])
        params = u'&'.join([u"{k}={v}".format(k=k, v=v) for k, v in params.items() if v])
        uri = urlunparse((parsed_uri.scheme,
                          parsed_uri.netloc,
                          parsed_uri.path,
                          parsed_uri.params,
                          params,
                          parsed_uri.fragment))
    return uri
