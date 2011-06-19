from google.appengine.ext import webapp

from ca_utils import render_template

class LoadLoginForm(webapp.RequestHandler):
    def get(self):
        render_template(self, 'login.html', {})