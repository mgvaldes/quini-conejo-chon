from google.appengine.ext.appstats import recording

from gaesessions import SessionMiddleware

import os

COOKIE_KEY = '\x98\x993\x0e\x08\xd5=\x8b\x9fM\xd0P\xd3\x96\xa5P\xef!0\xc3?Q\x97\xc3\xbfx\x82\xde\xd7\x14\xd2j~{\x04\xbe*Y\x08\\\x83V\x80\x1a\xfd|\x1eY\x02\xa6\xcc<\xc1\xf5\xd3\xbe%\xecl\x18\x91\x93<\x8b'

def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app, cookie_key=COOKIE_KEY)
    app = recording.appstats_wsgi_middleware(app)
    return app

remoteapi_CUSTOM_ENVIRONMENT_AUTHENTICATION = ('HTTP_X_APPENGINE_INBOUND_APPID', ['tuquinielaca'])