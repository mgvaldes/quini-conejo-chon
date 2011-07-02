import os.path
import sys

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from create_football_pool import CreateFootballPoolStepOne, CreateFootballPoolStepTwo, SaveCreateFootbalPool
from edit_football_pool import EditFootballPoolStepTwo, SaveEditFootbalPool
from view_football_pools import ListFootballPoolsToView, ListFootballPoolsToPay, ViewFootballPool
from pay_football_pool import PayFootballPool
from register import LoadRegistryForm, RegisterCANativeUser
from login import LoadLoginForm
from view_competition_groups import ListCompetitionGroupsToView, ListCompetitionGroupsToRanking, ViewCompetitionGroup, CreateCompetitionGroup, AddMemberToCompetitionGroup, DeleteMemberFromCompetitionGroup
from group_membership_request import AcceptGroupMembershipRequest, RejectGroupMembershipRequest
from rules import RulesHandler
from user_profile import CAUserProfileHandler, SaveCAUserProfile
from copa_america import ViewCopaAmerica
from edit_competition_group import EditCACompetitionGroup, EditAddMemberToCompetitionGroup, EditDeleteMemberFromCompetitionGroup
from view_user_football_pool import ViewUserFootballPool
from comments import CommentHandler

from session import LoginHandler, LogoutHandler, FacebookLoginHandler, GoogleLoginHandler
from ca_utils import render_template, check_session_status

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
            if session.has_key('active_user'):
                template_values = {
                    'session_status': True,
                    'user': session['active_user']
                }
            else:
                session.terminate()
                
                template_values = {
                    'session_status': False
                }
        else:
            template_values = {
                'session_status': False
            }
            
        render_template(self, 'index.html', template_values)
        
#            template_values = {
#                'session_status': True,
#                'user': session['active_user'],
#                'top_scorers': get_top_scorers(),
#                'top_users': get_top_users_global_ranking(),
#                'last_jackpot': get_last_jackpot()
#            }
            
#            template_values = {
#                'user': session['active_user'],
#                'top_scorers': get_top_scorers(),
#                'top_users': get_top_users_global_ranking(),
#                'last_jackpot': get_last_jackpot()
#            }
#                        
#            render_template(self, 'home.html', template_values)
#        else:
#            template_values = {
#                'session_status': False,
#                'top_scorers': get_top_scorers(),
#                'top_users': get_top_users_global_ranking(),
#                'last_jackpot': get_last_jackpot()
#            }
#            template_values = {
#                'error': ''   
#            }
    
        #render_template(self, 'index.html', template_values)
        #render_template(self, 'index.html', {})
            
application = webapp.WSGIApplication([('/', MainHandler),
                                      ('/login', LoadLoginForm),
                                      ('/register', LoadRegistryForm),
                                      ('/register/save', RegisterCANativeUser),
                                      ('/home', LoginHandler),
                                      ('/auth/facebook', FacebookLoginHandler),
                                      ('/auth/google', GoogleLoginHandler),
                                      ('/logout', LogoutHandler),
                                      #('/create/step1', CreateFootballPoolStepOne),
                                      #('/create/step2', CreateFootballPoolStepTwo),
                                      ('/save/create', SaveCreateFootbalPool),
                                      #('/edit/step2', EditFootballPoolStepTwo),
                                      ('/save/edit', SaveEditFootbalPool),
                                      ('/list/football-pools/view', ListFootballPoolsToView),
                                      ('/list/football-pools/pay', ListFootballPoolsToPay),
                                      ('/view/football-pool', ViewFootballPool),
                                      ('/pay', PayFootballPool),
                                      ('/list/groups/view', ListCompetitionGroupsToView),
                                      ('/list/groups/ranking', ListCompetitionGroupsToRanking),
                                      ('/view/group', ViewCompetitionGroup),
                                      ('/create/group', CreateCompetitionGroup),
                                      ('/add/group', AddMemberToCompetitionGroup),
                                      ('/delete/group', DeleteMemberFromCompetitionGroup),
                                      ('/accept/membership', AcceptGroupMembershipRequest),
                                      ('/reject/membership', RejectGroupMembershipRequest),
                                      ('/rules', RulesHandler),
                                      ('/view/profile', CAUserProfileHandler),
                                      ('/save/profile', SaveCAUserProfile),
                                      ('/view/copa-america', ViewCopaAmerica),
                                      ('/edit/group', EditCACompetitionGroup),
                                      ('/edit/add/group', EditAddMemberToCompetitionGroup),
                                      ('/edit/delete/group', EditDeleteMemberFromCompetitionGroup),
                                      ('/view/user/football-pool', ViewUserFootballPool),
                                      ('/view/group/comment', CommentHandler)],
                                     debug=True)

def main():
    sys.path.append(os.path.join(os.path.dirname(__file__), "models"))
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
