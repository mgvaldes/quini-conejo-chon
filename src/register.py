from google.appengine.ext import webapp

from models.ca_models import CANativeUser, CAUser
from ca_utils import render_template, check_session_status, get_top_scorers, get_top_users_global_ranking, get_last_jackpot

from gaesessions import get_current_session

class LoadRegistryForm(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        
        check_session_status()
            
        if session.is_active():
            template_values = {
                'session_status': True,
                'user': session['active_user'],
                'top_scorers': get_top_scorers(),
                'top_users': get_top_users_global_ranking(),
                'last_jackpot': get_last_jackpot()
            }
        else:
            template_values = {
                'session_status': False,
                'top_scorers': get_top_scorers(),
                'top_users': get_top_users_global_ranking(),
                'last_jackpot': get_last_jackpot()
            }
            
        render_template(self, 'register.html', template_values)

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
