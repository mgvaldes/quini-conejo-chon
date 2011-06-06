import os.path

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class HomeHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'home.html')
        self.response.out.write(template.render(path, {}))