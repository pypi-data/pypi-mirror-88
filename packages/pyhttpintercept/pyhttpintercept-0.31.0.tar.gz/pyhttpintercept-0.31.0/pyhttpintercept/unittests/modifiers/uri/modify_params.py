# encoding: utf-8

import logging_helper
from pyhttpintercept.helpers import run_ad_hoc_uri_modifier
from pyhttpintercept.intercept.modifiers.uri import modify_params as module_to_test
from simpil import SimpilImage

logging = logging_helper.setup_logging()

params = {"paramtoremove": '',
          "p2":            "v2",
          "p3":            "v3"}

uri = run_ad_hoc_uri_modifier(module=module_to_test,
                              uri=u'http://user:pass@www.hostname.com:8080/some_method?p1=v1&p2=x&paramtoremove=whatever#hash',
                              filter=u'some_method',
                              params=params)

print(uri)
assert '/some_method?' in uri
assert 'p1=v1' in uri
assert 'p2=v2' in uri
assert 'p3=v3' in uri
assert 'paramtoremove' not in uri
assert '&' in uri
assert uri.startswith('http://user:pass@www.hostname.com:8080')
assert uri.endswith('#hash')

# ---------------------

uri = run_ad_hoc_uri_modifier(module=module_to_test,
                              uri=u'http://www.hostname.com/some_method?p1=v1&p2=x&paramtoremove=whatever#hash',
                              filter=u'some_method',
                              params=params)

print(uri)
assert '/some_method' in uri
assert 'p1=v1' in uri
assert 'p2=v2' in uri
assert 'p3=v3' in uri
assert '&' in uri
assert uri.startswith('http://www.hostname.com/')
assert uri.endswith('#hash')

# ---------------------

params = {"paramtoremove": '',
          "p1":            "",
          "p2":            ""}

uri = run_ad_hoc_uri_modifier(module=module_to_test,
                              uri=u'http://www.hostname.com/some_method?p1=v1&p2=x&paramtoremove=whatever#hash',
                              filter=u'some_method',
                              params=params)


print(uri)
assert '/some_method?' not in uri
assert '/some_method' in uri
assert 'p1=v1' not in uri
assert 'p2=v2' not in uri
assert 'p3=v3' not in uri
assert 'paramtoremove' not in uri
assert '&' not in uri
assert uri.startswith('http://www.hostname.com/')
assert uri.endswith('#hash')

