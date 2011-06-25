from google.appengine.ext import webapp
from google.appengine.api.users import User

from models.ca_models import CANativeUser, CAUser
from ca_utils import render_template, check_session_status, get_top_scorers, get_top_users_global_ranking, get_last_jackpot, update_session_time

from gaesessions import get_current_session

class LoadRegistryForm(webapp.RequestHandler):
    def get(self):
        update_session_time()
        session = get_current_session()
        check_session_status()
            
        if session.is_active():
            if session.has_key('active_user'):
                template_values = {
                    'session_status': True,
                    'user': session['active_user'],
                    'top_scorers': get_top_scorers(),
                    'top_users': get_top_users_global_ranking(),
                    'last_jackpot': get_last_jackpot(),
                    'error': ''
                }
            else:
                session.terminate()
                
                template_values = {
                    'session_status': False,
                    'top_scorers': get_top_scorers(),
                    'top_users': get_top_users_global_ranking(),
                    'last_jackpot': get_last_jackpot(),
                    'error': ''
                }
        else:
            template_values = {
                'session_status': False,
                'top_scorers': get_top_scorers(),
                'top_users': get_top_users_global_ranking(),
                'last_jackpot': get_last_jackpot(),
                'error': ''
            }
            
        render_template(self, 'register.html', template_values)

class RegisterCANativeUser(webapp.RequestHandler):
    def post(self):
        name = self.request.get('name')
        email = self.request.get('email')
        password = self.request.get('password')
        
        existing_google_user = CAUser.all().filter("google_user !=", None).fetch(10000)
        exists = False
        
        for user in existing_google_user:
            if user.google_user.email() == email:
                exists = True
                break
        
        if not exists:
            existing_user = CANativeUser.all().filter("email =", email).fetch(10000)
            
            if not existing_user:
                user = CANativeUser(name=name, email=email, password=password)
                user.put()
                
                ca_user = CAUser(native_user=user, type=2)
                ca_user.put()
            
                self.redirect('/login')
            else:
                template_values = {
                    'session_status': False,
                    'top_scorers': get_top_scorers(),
                    'top_users': get_top_users_global_ranking(),
                    'last_jackpot': get_last_jackpot(),
                    'error': 'Ya existe un usuario registrado con este correo electr&oacute;nico. Int&eacute;ntalo de nuevo'
                }
                
                render_template(self, 'register.html', template_values)
        else:
            template_values = {
                'session_status': False,
                'top_scorers': get_top_scorers(),
                'top_users': get_top_users_global_ranking(),
                'last_jackpot': get_last_jackpot(),
                'error': 'Ya existe un usuario registrado con este correo electr&oacute;nico. Int&eacute;ntalo de nuevo'
            }
            
            render_template(self, 'register.html', template_values)
