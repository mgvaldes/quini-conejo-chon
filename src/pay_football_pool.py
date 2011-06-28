import datetime

from google.appengine.ext import webapp
from google.appengine.ext.db import Key
from google.appengine.ext import db

from gaesessions import get_current_session

from ca_utils import check_session_status, render_template, update_session_time, get_top_scorers, get_top_users_global_ranking, get_last_jackpot
from models.ca_models import CAFootballPool, CAPayment, CACompetitonGroup, CAGroupRanking, CAUser,\
    CARecommendation

class PayFootballPool(webapp.RequestHandler):
    def post(self):
        update_session_time()
        session = get_current_session()
        check_session_status()
        
        if session.is_active():
            search_user = self.request.get('search_user')
            
            if search_user:
                active_user = session['active_user']
                search_term = self.request.get('search')
                search_result = []
                
                if search_term:
                    users = CAUser.all().fetch(10000)

                    for user in users:
                        if active_user.key() != user.key():
                            username = []
                            
                            if user.type == 0:
                                nickname = user.google_user.nickname()
                                email = user.google_user.email()

                                if (search_term.lower() in str(nickname).lower()) or (search_term.lower() in str(email).lower()):
                                    username = nickname + ' ' + email
                            elif user.type == 1:
                                name = user.facebook_user.name

                                if search_term.lower() in str(name).lower():
                                    username = name
                            else:
                                name = user.native_user.name
                                email = user.native_user.email

                                if (search_term.lower() in str(name).lower()) or (search_term.lower() in str(email).lower()):
                                    username = name + ' ' + email

                            if username:
                                search_result.append((str(username), str(user.key())))
                                
                template_values = {
                    'session_status': True,
                    'user': session['active_user'],
                    'searched_users': search_result,
                    'top_scorers': get_top_scorers(),
                    'top_users': get_top_users_global_ranking(),
                    'last_jackpot': get_last_jackpot(),
                    'selected_football_pool_key': self.request.get('selected_football_pool_key'),
                    'selected_user': ''
                }
                
                render_template(self, 'pay_football_pool.html', template_values)                    
            else:
                selected_user = self.request.get('user_key')
                
                if selected_user:
                    users = []
                    
                    users.append(Key(selected_user))
                    users.append(session['active_user'].key())
                    
                    recommendation = CARecommendation(users=users)
                    recommendation.put()
                
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
                    
    
                    groups = active_user.groups
                    
                    for group_key in groups:
                        group = CACompetitonGroup.get(group_key)
                        
                        if group:
                            members = group.members.fetch(10000)
                        
                            group_ranking = CAGroupRanking(football_pool=selected_football_pool, group=group, rank=len(members))
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