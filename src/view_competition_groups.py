from google.appengine.ext import webapp
from google.appengine.ext.db import Key

from gaesessions import get_current_session

from ca_utils import check_session_status, render_template
from models.ca_models import CACompetitonGroup, CAGroupRanking, CAUser

class ListCompetitionGroups(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        
        check_session_status()
            
        if session.is_active():
            active_user = session['active_user']
            
            competition_groups = CACompetitonGroup.get(active_user.groups)
            
            template_values = {
                'groups': competition_groups
            }
            
            render_template(self, 'list_competition_groups.html', template_values)
        else:
            self.redirect('/')
            
class ViewCompetitionGroup(webapp.RequestHandler):
    def post(self):
        session = get_current_session()
        
        check_session_status()
            
        if session.is_active():
            selected_competition_group_key = Key(self.request.get('selected_competition_group'))
            
            edit = self.request.get('edit')
            ranking = self.request.get('ranking')
            
            if edit:
                print ''
            elif ranking:
                competition_group = CACompetitonGroup.get(selected_competition_group_key)
                
                group_ranking = CAGroupRanking.all().filter("group =", selected_competition_group_key).fetch(10000)
                
                active_user = session['active_user']
                active_user_football_pools = active_user.football_pools
                
                active_user_football_pools_keys = []
                for football_pool in active_user_football_pools: 
                    active_user_football_pools_keys.append(football_pool.key())
                
                group_ranking_list = []
                
                for rank in group_ranking:
                    if rank.football_pool.key() in active_user_football_pools_keys:
                        selected = True
                    else:
                        selected = False
                    
                    if rank.football_pool.user.type == 0:
                        name = rank.football_pool.user.google_user
                    elif rank.football_pool.user.type == 1:
                        name = rank.football_pool.user.facebook_user.name
                    else:
                        name = rank.football_pool.user.native_user.name
                        
                    group_ranking_list.append((name, rank.football_pool.name, 0, selected))
                    
                template_values = {
                    'competition_group_name': competition_group.name,
                    'group_ranking': group_ranking_list
                }
                
                render_template(self, 'ranking.html', template_values)
        else:
            self.redirect('/')
                
class CreateCompetitionGroup(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        
        check_session_status()
            
        if session.is_active():
            template_values = {
                'searched_users': [],
                'members': [],
                'name': ''
            }
            
            render_template(self, 'create_competition_group.html', template_values)
        else:
            self.redirect('/')
            
    def post(self):
        session = get_current_session()
        
        check_session_status()
            
        if session.is_active():
            search_user = self.request.get('search_user')
            save = self.request.get('save')
            
            if search_user:
                active_user = session['active_user']
                
                search_term = self.request.get('search')
                
                users = CAUser.all().fetch(10000)
                search_result = []
                
                for user in users:
                    if active_user.key() != user.key():
                        username = []
                        
                        if user.type == 0:
                            nickname = user.google_user
                            email = user.google_user.email
                            
                            if (search_term.lower() in str(nickname).lower()) or (search_term.lower() in str(email).lower()):
                                username = nickname
                        elif user.type == 1:
                            name = user.facebook_user.name
                            
                            if search_term.lower() in str(name).lower():
                                username = name
                        else:
                            name = user.native_user.name
                            email = user.native_user.email
                            
                            if (search_term.lower() in str(name).lower()) or (search_term.lower() in str(email).lower()):
                                username = name
                    
                        if username:
                            search_result.append((username, user.key()))
                    
                template_values = {
                    'searched_users': search_result,
                    'members': [],
                    'name': self.request.get('name')
                }
                
                render_template(self, 'create_competition_group.html', template_values)
            elif save:
               print ''
        else:
            self.redirect('/')
            