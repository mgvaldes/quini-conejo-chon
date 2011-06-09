import os.path
import sys

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from gaesessions import get_current_session

from create_football_pool import CreateFootballPoolStepOne, CreateFootballPoolStepTwo

from session import LoginHandler, LogoutHandler, FacebookLoginHandler, GoogleLoginHandler

"""
Handler inicial que maneja el metodo de autenticacion del usuario.
Puede ser a traves de el metodo de autenticacion de appengine o
de Facebook.
"""
class MainHandler(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        
        template_values = {
            'error': ''   
        }
        
        """
        Manejo de sesion
        """
        if session.has_key('msg'):
            del session['msg'] # only show the message once

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
            
application = webapp.WSGIApplication([('/', MainHandler),
                                      ('/home', LoginHandler),
                                      ('/auth/facebook', FacebookLoginHandler),
                                      ('/auth/google', GoogleLoginHandler),
                                      ('/logout', LogoutHandler),
                                      ('/create/step1', CreateFootballPoolStepOne),
                                      ('/create/step2', CreateFootballPoolStepTwo)],
                                     debug=True)

def main():
    sys.path.append(os.path.join(os.path.dirname(__file__), "models"))
    run_wsgi_app(application)

if __name__ == "__main__":
    main()