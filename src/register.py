from google.appengine.ext import webapp

from models.ca_models import CANativeUser, CAUser
from ca_utils import render_template

class LoadRegistryForm(webapp.RequestHandler):
    def get(self):
        render_template(self, 'register.html', {})

class RegisterCANativeUser(webapp.RequestHandler):
    def post(self):
        name = self.request.get('name')
        email = self.request.get('email')
        password = self.request.get('password')
        
        user = CANativeUser(name=name, email=email, password=password)
        user.put()
        
        ca_user = CAUser(native_user=user, type=2)
        ca_user.put()
        
        self.redirect('/')