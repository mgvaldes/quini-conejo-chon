import os.path
import sys

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from create_football_pool import CreateFootballPoolStepOne, CreateFootballPoolStepTwo, SaveFootbalPool
from view_football_pools import ListFootballPools, ViewFootballPool
from pay_football_pool import PayFootballPool
from register import LoadRegistryForm, RegisterCANativeUser
from view_competition_groups import ListCompetitionGroups, ViewCompetitionGroup, CreateCompetitionGroup

from session import LoginHandler, LogoutHandler, FacebookLoginHandler, GoogleLoginHandler
from ca_utils import render_template

"""
Handler inicial que maneja el metodo de autenticacion del usuario.
Puede ser a traves de el metodo de autenticacion de appengine o
de Facebook.
"""
class MainHandler(webapp.RequestHandler):
    def get(self):
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
                                      ('/save', SaveFootbalPool),
                                      ('/list', ListFootballPools),
                                      ('/view', ViewFootballPool),
                                      ('/pay', PayFootballPool),
                                      ('/list/groups', ListCompetitionGroups),
                                      ('/view/group', ViewCompetitionGroup),
                                      ('/create/group', CreateCompetitionGroup)],
                                     debug=True)

def main():
    sys.path.append(os.path.join(os.path.dirname(__file__), "models"))
    run_wsgi_app(application)

if __name__ == "__main__":
    main()