import datetime

from google.appengine.ext import webapp
from google.appengine.ext.db import Key
from google.appengine.ext import db

from gaesessions import get_current_session

from ca_utils import check_session_status, render_template, update_session_time, get_top_scorers, get_top_users_global_ranking, get_last_jackpot
from models.ca_models import CAFootballPool, CAPayment, CACompetitonGroup, CAGroupRanking

class PayFootballPool(webapp.RequestHandler):
    def post(self):
        update_session_time()
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
                
                active_user_football_pools = CAFootballPool.all().filter("user =", active_user).filter("privacy =", False).fetch(1000)
                
                for football_pool in active_user_football_pools:
                    if football_pool.payment:
                        groups = active_user.groups
                        
                        for group_key in groups:
                            group = CACompetitonGroup.get(group_key)
                            
                            if group:
                                members = group.members.fetch(10000)
                            
                                group_ranking = CAGroupRanking(football_pool=football_pool, group=group, rank=len(members))
                                group_ranking.put()
                
                global_competition_group = CACompetitonGroup.all().filter("privacy =", True).fetch(1)[0]
                
                if global_competition_group.key() not in active_user.groups: 
                    active_user.groups.append(global_competition_group.key())
                    active_user.put()
                    
                    members = global_competition_group.members.fetch(10000)
                
                    group_ranking = CAGroupRanking(football_pool=selected_football_pool, group=global_competition_group, rank=len(members))
                    group_ranking.put()
                
#                template_values = {
#                    'session_status': True,
#                    'user': session['active_user'],
#                    'football_pools': active_user_football_pools,
#                    'message':'Su pago fue registrado exitosamente',
#                    'top_scorers': get_top_scorers(),
#                    'top_users': get_top_users_global_ranking(),
#                    'last_jackpot': get_last_jackpot()
#                } 
#                
#                render_template(self, 'list_football_pools_to_pay.html', template_values)
                template_values = {
                    'session_status': True,
                    'user': session['active_user'],
                    'football_pools': active_user_football_pools,
                    'message':'Su pago fue registrado exitosamente',
                    'top_scorers': get_top_scorers(),
                    'top_users': get_top_users_global_ranking(),
                    'last_jackpot': get_last_jackpot()
                } 
                
                render_template(self, 'list_football_pools_to_view.html', template_values)
        else:
            self.redirect('/')