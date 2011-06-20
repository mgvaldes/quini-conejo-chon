from google.appengine.ext import webapp

from gaesessions import get_current_session

from ca_utils import check_session_status, render_template

class ProfileHandler(webapp.RequestHandler):
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
            
        render_template(self, 'profile.html', template_values)