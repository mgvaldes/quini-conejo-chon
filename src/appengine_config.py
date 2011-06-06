from gaesessions import SessionMiddleware
import os

def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app, cookie_key=os.urandom(64))
    return app

remoteapi_CUSTOM_ENVIRONMENT_AUTHENTICATION = ('HTTP_X_APPENGINE_INBOUND_APPID', ['tuquinielaca'])