import os.path
import sys

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from create_football_pool import CreateFootballPoolStepOne, CreateFootballPoolStepTwo, SaveCreateFootbalPool
from edit_football_pool import EditFootballPoolStepTwo, SaveEditFootbalPool
from view_football_pools import ListFootballPools, ViewFootballPool
from pay_football_pool import PayFootballPool
from register import LoadRegistryForm, RegisterCANativeUser
from view_competition_groups import ListCompetitionGroups, ViewCompetitionGroup, CreateCompetitionGroup, AddMemberToCompetitionGroup, DeleteMemberFromCompetitionGroup
from group_membership_request import AcceptGroupMembershipRequest, RejectGroupMembershipRequest

from session import LoginHandler, LogoutHandler, FacebookLoginHandler, GoogleLoginHandler
from ca_utils import render_template, check_session_status, get_pending_membership_requests, get_top_scorers, get_top_users_global_ranking

from gaesessions import get_current_session

"""
Handler inicial que maneja el metodo de autenticacion del usuario.
Puede ser a traves de el metodo de autenticacion de appengine o
de Facebook.
"""
class MainHandler(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        
        check_session_status()
            
        if session.is_active():
            template_values = {
                'user': session['active_user'],
                'pending_membership_requests': get_pending_membership_requests(session['active_user']),
                'top_scorers': get_top_scorers(),
                'top_users': get_top_users_global_ranking()
            }
                        
            render_template(self, 'home.html', template_values)
        else:
            template_values = {
                'error': ''   
            }
    
            render_template(self, 'index.html', template_values)
            
application = webapp.WSGIApplication([('/', MainHandler),
                                      ('/register', LoadRegistryForm),
                                      ('/register/save', RegisterCANativeUser),
                                      ('/home', LoginHandler),
                                      ('/auth/facebook', FacebookLoginHandler),
                                      ('/auth/google', GoogleLoginHandler),
                                      ('/logout', LogoutHandler),
                                      ('/create/step1', CreateFootballPoolStepOne),
                                      ('/create/step2', CreateFootballPoolStepTwo),
                                      ('/save/create', SaveCreateFootbalPool),
                                      ('/edit/step2', EditFootballPoolStepTwo),
                                      ('/save/edit', SaveEditFootbalPool),
                                      ('/list', ListFootballPools),
                                      ('/view', ViewFootballPool),
                                      ('/pay', PayFootballPool),
                                      ('/list/groups', ListCompetitionGroups),
                                      ('/view/group', ViewCompetitionGroup),
                                      ('/create/group', CreateCompetitionGroup),
                                      ('/add/group', AddMemberToCompetitionGroup),
                                      ('/delete/group', DeleteMemberFromCompetitionGroup),
                                      ('/accept/membership', AcceptGroupMembershipRequest),
                                      ('/reject/membership', RejectGroupMembershipRequest)],
                                     debug=True)

def main():
    sys.path.append(os.path.join(os.path.dirname(__file__), "models"))
    run_wsgi_app(application)

if __name__ == "__main__":
    main()