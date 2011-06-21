import base64
import cgi
import Cookie
import email.utils
import hashlib
import hmac
import logging
import time
import urllib
import simplejson as json

from google.appengine.api import users
from google.appengine.ext import webapp

from gaesessions import get_current_session

from models.ca_models import CAFacebookUser, CANativeUser, CAUser
from ca_utils import render_template, save_session_info, get_top_scorers, get_top_users_global_ranking, get_last_jackpot

FACEBOOK_APP_ID = "176955699024734"
FACEBOOK_APP_SECRET = "b7d8f9f20519d0d54a2bc96569f6c15f"

"""
Handler que se encarga de redirigir a la pagina correspondiente
segun la opcion escogida por el usuario para autenticarse
"""
class LoginHandler(webapp.RequestHandler):
    def post(self):
        session = get_current_session()
        
        if session.is_active():
            session.terminate()
            
        accept = self.request.get('accept')
        google = self.request.get('google')
        
        """
        Login con autenticacion nativa
        """
        if accept:
            logging.debug('Login with native credentials')
            
            email = self.request.get('email')
            password = self.request.get('password')
            
            if email and password:
                logging.debug('Checking credentials')
                
                user = CANativeUser.all().filter("email =", email).fetch(1)
    
                if user:
                    if user[0].password == password:
                        logging.debug('Username and password correct. Login successfull')
                        
                        ca_user = CAUser.all().filter("native_user", user[0]).fetch(1)
                        
                        if ca_user:
                            logging.debug('User registered with Native account. Login successfull')
                            ca_user = ca_user[0] 
                        else:
                            ca_user = CAUser(google_user=user[0], type=0)
                            ca_user.put()

                        save_session_info(ca_user)
                        
#                        template_values = {
#                            'session_status': True,
#                            'user': session['active_user'],
#                            'top_scorers': get_top_scorers(),
#                            'top_users': get_top_users_global_ranking(),
#                            'last_jackpot': get_last_jackpot()
#                        }
                        
#                        render_template(self, 'create_step1.html', template_values)
                        self.redirect('/create/step1')
                    else:
                        logging.debug('Incorrect password. . Login failed')
                        
                        template_values = {
                            'error': 'Clave incorrecta. Intente de nuevo'
                        }
    
                        render_template(self, 'login.html', template_values)
                else:
                    logging.debug('Incorrect username. Login failed')
                    
                    template_values = {
                        'error': 'Usuario incorrecto. Intente de nuevo'
                    }
    
                    render_template(self, 'login.html', template_values)
            else:
                logging.debug('Username o password missing. Login failed')
                    
                template_values = {
                    'error': 'Usuario o clave faltantes. Intente de nuevo'
                }
                
                render_template(self, 'login.html', template_values)
        else:
            """
            Login con autenticacion de google o facebook
            """
            if google:
                logging.debug('GOOGLE')
                logging.debug('Login with Google')
                self.redirect(users.create_login_url('/auth/google'))
            else:
                logging.debug('FACEBOOK')
                logging.debug('Login with Facebook')
                self.redirect("/auth/facebook")

"""
Handler que se encarga de hacer el login en google y redirigir a la
pagina con el permiso e informacion del usuario logueado
"""
class GoogleLoginHandler(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        
        if session.is_active():
            session.terminate()
        
        user = users.get_current_user()
        ca_user = CAUser.all().filter("google_user", user).fetch(1)
        
        if ca_user:
            logging.debug('User registered with Google account. Login successfull')
            ca_user = ca_user[0]
        else:
            ca_user = CAUser(google_user=user, type=0)
            ca_user.put()
            
        save_session_info(ca_user)
        
#        template_values = {
#            'session_status': True,
#            'user': session['active_user'],
#            'top_scorers': get_top_scorers(),
#            'top_users': get_top_users_global_ranking(),
#            'last_jackpot': get_last_jackpot()
#        }
#                
#        render_template(self, 'create_step1.html', template_values)
        self.redirect('/create/step1')

"""
Handler que se encarga de hacer el login en facebook y redirigir a la
pagina con el permiso e informacion del usuario logueado
"""
class FacebookLoginHandler(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        
        if session.is_active():
            session.terminate()
        
        verification_code = self.request.get("code")
        
        args = dict(client_id=FACEBOOK_APP_ID,
                    redirect_uri=self.request.path_url)
        
        if verification_code:
            args["client_secret"] = FACEBOOK_APP_SECRET
            args["code"] = self.request.get("code")
            response = cgi.parse_qs(urllib.urlopen("https://graph.facebook.com/oauth/access_token?" +
                                                   urllib.urlencode(args)).read())
            
            access_token = response["access_token"][-1]

            # Download the user profile and cache a local instance of the
            # basic profile info
            profile = json.load(urllib.urlopen("https://graph.facebook.com/me?" + urllib.urlencode(dict(access_token=access_token))))

            user = CAFacebookUser(key_name=str(profile["id"]),
                                  id=str(profile["id"]),
                                  name=profile["name"],
                                  access_token=access_token)

            ca_user = CAUser.all().filter("facebook_user", user).fetch(1)
            
            if ca_user:
                logging.debug('User registered with Facebook account. Login successfull')
                ca_user = ca_user[0]
            else:
                user.put()
                ca_user = CAUser(facebook_user=user, type=1)
                ca_user.put()
                
            save_session_info(ca_user)
            
#            template_values = {
#                'session_status': True,
#                'user': session.get('active_user'),
#                'top_scorers': get_top_scorers(),
#                'top_users': get_top_users_global_ranking(),
#                'last_jackpot': get_last_jackpot()
#            }
        
            set_cookie(self.response, "fb_user",
                       str(profile["id"]),
                       expires=time.time() + 30 * 86400)
            
#            render_template(self, 'create_step1.html', template_values)

            self.redirect('/create/step1')
        else:
            self.redirect("https://graph.facebook.com/oauth/authorize?" +
                          urllib.urlencode(args))

class LogoutHandler(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        
        if session.is_active():
            session.terminate()
        
        set_cookie(self.response, "fb_user", "", expires=time.time() - 86400)
        self.redirect(users.create_logout_url("/"))

def set_cookie(response, name, value, domain=None, path="/", expires=None):
    """Generates and signs a cookie for the give name/value"""
    timestamp = str(int(time.time()))
    value = base64.b64encode(value)
    signature = cookie_signature(value, timestamp)
    cookie = Cookie.BaseCookie()
    cookie[name] = "|".join([value, timestamp, signature])
    cookie[name]["path"] = path
    
    if domain:
        cookie[name]["domain"] = domain
        
    if expires:
        cookie[name]["expires"] = email.utils.formatdate(expires,
                                                         localtime=False,
                                                         usegmt=True)
        
    response.headers._headers.append(("Set-Cookie", cookie.output()[12:]))

def parse_cookie(value):
    """Parses and verifies a cookie value from set_cookie"""
    if not value:
        return None
    
    parts = value.split("|")
    
    if len(parts) != 3:
        return None
    
    if cookie_signature(parts[0], parts[1]) != parts[2]:
        logging.warning("Invalid cookie signature %r", value)
        return None
    
    timestamp = int(parts[1])
    
    if timestamp < time.time() - 30 * 86400:
        logging.warning("Expired cookie %r", value)
        return None
    
    try:
        return base64.b64decode(parts[0]).strip()
    except:
        return None

def cookie_signature(*parts):
    """Generates a cookie signature.
    We use the Facebook app secret since it is different for every app (so
    people using this example don't accidentally all use the same secret).
    """
    hash = hmac.new(FACEBOOK_APP_SECRET, digestmod=hashlib.sha1)
    
    for part in parts:
        hash.update(part)
        
    return hash.hexdigest()
