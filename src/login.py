from google.appengine.ext import webapp

from ca_utils import render_template, check_session_status

from gaesessions import get_current_session

class LoadLoginForm(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        
        check_session_status()
            
        if session.is_active():
            template_values = {
                'session_status': True,
                'user': session['active_user']
            }
        else:
            template_values = {
                'session_status': False
            }
            
        render_template(self, 'login.html', template_values)