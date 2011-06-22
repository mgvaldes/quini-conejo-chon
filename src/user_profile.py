from google.appengine.ext import webapp

from gaesessions import get_current_session

from ca_utils import check_session_status, render_template, get_top_scorers, get_top_users_global_ranking, get_last_jackpot, get_total_points
from models.ca_models import CAFootballPool, CANativeUser

class CAUserProfileHandler(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        
        check_session_status()
            
        if session.is_active():
            active_user = session['active_user']
            
            active_user_football_pools = CAFootballPool.all().filter("user =", active_user).filter("privacy =", False).fetch(1000)
            
            football_pools_info = []
            
            for football_pool in active_user_football_pools:
                if not football_pool.payment:
                    football_pools_info.append((football_pool.name, 'Por Pagar', '-'))
                else:
                    if football_pool.payment.status:
                        football_pools_info.append((football_pool.name, 'Pagada', str(get_total_points(football_pool))))
                    else:
                        football_pools_info.append((football_pool.name, 'Esperando Confirmaci&oacute;n de Pago', '-'))
            
            template_values = {
                'session_status': True,
                'user': session['active_user'],
                'football_pools_info': football_pools_info,
                'top_scorers': get_top_scorers(),
                'top_users': get_top_users_global_ranking(),
                'last_jackpot': get_last_jackpot()
            }
            
            render_template(self, 'user_profile.html', template_values)
        else:
            self.redirect('/')
            
class SaveCAUserProfile(webapp.RequestHandler):
    def post(self):
        session = get_current_session()
        
        check_session_status()
            
        if session.is_active():
            save = self.request.get('save')
            
            active_user = session['active_user']
            message = ''
            
            if active_user.type == 2:
                if save:
                    native_user = CANativeUser.get(active_user.native_user.key())
                    
                    native_user.name = self.request.get('name')
                    native_user.email = self.request.get('email')
                    native_user.password = self.request.get('password')
                    native_user.put()
                    
                    active_user.native_user = native_user
                    active_user.put()
                    
                    session['active_user'] = active_user
                    message = 'Sus datos fueron actualizados exitosamente' 
                    
            active_user_football_pools = CAFootballPool.all().filter("user =", active_user).filter("privacy =", False).fetch(1000)
            
            template_values = {
                'session_status': True,
                'user': session['active_user'],
                'football_pools': active_user_football_pools,
                'message': message,
                'top_scorers': get_top_scorers(),
                'top_users': get_top_users_global_ranking(),
                'last_jackpot': get_last_jackpot()
            }
                    
            render_template(self, 'list_football_pools_to_view.html', template_values)
        else:
            self.redirect('/')