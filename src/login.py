from google.appengine.ext import webapp

from ca_utils import render_template, check_session_status, get_top_scorers, get_top_users_global_ranking, get_last_jackpot

from gaesessions import get_current_session

class LoadLoginForm(webapp.RequestHandler):
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
            
        render_template(self, 'login.html', template_values)
