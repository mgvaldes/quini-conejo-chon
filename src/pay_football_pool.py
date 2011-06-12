import datetime

from google.appengine.ext import webapp
from google.appengine.ext.db import Key
from google.appengine.ext import db

from gaesessions import get_current_session

from ca_utils import check_session_status, render_template
from models.ca_models import CAFootballPool, CAPayment, CACompetitonGroup, CAGroupRanking

class PayFootballPool(webapp.RequestHandler):
    def post(self):
        session = get_current_session()
        
        check_session_status()
            
        if session.is_active():
            payment_number = self.request.get('payment_number')
            bank = self.request.get('bank')
            payment_type = self.request.get('payment_type')
            
            if payment_type == 'deposit':
                type = False
            elif payment_type == 'transfer':
                type = True
                
            payment = CAPayment(bank=bank, type=type, date=datetime.datetime.now(), status=False, payment_number=payment_number)
            payment.put()
            
            selected_football_pool_key = Key(self.request.get('selected_football_pool_key'))
            selected_football_pool = CAFootballPool.get(selected_football_pool_key)
            selected_football_pool.payment = payment
            selected_football_pool.put()
            
            if session.has_key('active_user'):
                active_user = session['active_user']
                
                global_competition_group = CACompetitonGroup.all().filter("privacy =", True).fetch(1)[0]
                
                active_user.groups.append(global_competition_group.key())
                active_user.put()
                
                members = global_competition_group.members.fetch(10000)
            
                group_ranking = CAGroupRanking(football_pool=selected_football_pool, group=global_competition_group, rank=len(members))
                group_ranking.put()
                
                active_user_football_pools = CAFootballPool.all().filter("user =", active_user).filter("privacy =", False).fetch(1)
                
                template_values = {
                    'football_pools': active_user_football_pools,
                    'message':'Su pago fue registrado exitosamente'
                } 
                
                render_template(self, 'list_football_pools.html', template_values)
        else:
            self.redirect('/')