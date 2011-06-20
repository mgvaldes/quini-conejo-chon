from google.appengine.ext import webapp
from google.appengine.ext.db import Key

from gaesessions import get_current_session

from ca_utils import check_session_status, render_template, get_total_points, update_session_time, get_pending_membership_requests, get_top_scorers, get_top_users_global_ranking, get_last_jackpot
from models.ca_models import CACompetitonGroup, CAGroupRanking, CAUser, CARequestGroupMembership, CAFootballPool

class ListCompetitionGroupsToView(webapp.RequestHandler):
    def get(self):
        update_session_time()
        session = get_current_session()
        check_session_status()
            
        if session.is_active():
            active_user = session['active_user']
            
            competition_groups = CACompetitonGroup.get(active_user.groups)
            
            template_values = {
                'session_status': True,
                'user': active_user,
                'groups': competition_groups,
                'pending_membership_requests': get_pending_membership_requests(active_user),
                'top_scorers': get_top_scorers(),
                'top_users': get_top_users_global_ranking(),
                'last_jackpot': get_last_jackpot()
            }
            
            render_template(self, 'list_competition_groups_to_view.html', template_values)
        else:
            self.redirect('/')
            
class ListCompetitionGroupsToRanking(webapp.RequestHandler):
    def get(self):
        update_session_time()
        session = get_current_session()
        check_session_status()
            
        if session.is_active():
            active_user = session['active_user']
            
            competition_groups = CACompetitonGroup.get(active_user.groups)
            
            template_values = {
                'session_status': True,
                'user': active_user,
                'groups': competition_groups,
                'pending_membership_requests': get_pending_membership_requests(active_user),
                'top_scorers': get_top_scorers(),
                'top_users': get_top_users_global_ranking(),
                'last_jackpot': get_last_jackpot()
            }
            
            render_template(self, 'list_competition_groups_to_ranking.html', template_values)
        else:
            self.redirect('/')
            
class ViewCompetitionGroup(webapp.RequestHandler):
    def post(self):
        update_session_time()
        session = get_current_session()
        check_session_status()
            
        if session.is_active():
            selected = self.request.get('selected_competition_group')
            
            edit = self.request.get('edit')
            ranking = self.request.get('ranking')
            
            if selected != "default":
                selected_competition_group_key = Key(selected)
                
                if edit:
                    self.redirect('/list/groups/view')
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
                            name = rank.football_pool.user.google_user.nickname()
                        elif rank.football_pool.user.type == 1:
                            name = rank.football_pool.user.facebook_user.name
                        else:
                            name = rank.football_pool.user.native_user.name
                            
                        group_ranking_list.append((name, rank.football_pool.name, get_total_points(rank.football_pool), selected))
                        
                    template_values = {
                        'session_status': True,
                        'user': active_user,
                        'competition_group_name': competition_group.name,
                        'group_ranking': group_ranking_list,
                        'top_scorers': get_top_scorers(),
                        'top_users': get_top_users_global_ranking(),
                        'last_jackpot': get_last_jackpot()
                    }
                    
                    render_template(self, 'ranking.html', template_values)
            else:
                if edit:
                    self.redirect('/list/groups/view')
                elif ranking:
                    self.redirect('/list/groups/ranking')
        else:
            self.redirect('/')
                
class CreateCompetitionGroup(webapp.RequestHandler):
    def get(self):
        update_session_time()
        session = get_current_session()
        check_session_status()
            
        if session.is_active():
            template_values = {
                'session_status': True,
                'user': session['active_user'],
                'searched_users': [],
                'members': [],
                'name': '',
                'last_search': str([]),
                'last_members': str([]),
                'top_scorers': get_top_scorers(),
                'top_users': get_top_users_global_ranking(),
                'last_jackpot': get_last_jackpot()
            }
            
            render_template(self, 'create_competition_group.html', template_values)
        else:
            self.redirect('/')
            
    def post(self):
        update_session_time()
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
                            nickname = user.google_user.nickname()
                            email = user.google_user.email()
                            
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
                            search_result.append((str(username), str(user.key())))
                            
                template_values = {
                    'session_status': True,
                    'user': session['active_user'],
                    'searched_users': search_result,
                    'members': eval(self.request.get('last-members')),
                    'name': self.request.get('name'),
                    'last_search': str(search_result),
                    'last_members': self.request.get('last-members'),
                    'top_scorers': get_top_scorers(),
                    'top_users': get_top_users_global_ranking(),
                    'last_jackpot': get_last_jackpot()
                }
                
                render_template(self, 'create_competition_group.html', template_values)
            elif save:
                active_user = session['active_user']                
                name = self.request.get('name')
               
                new_group = CACompetitonGroup(name=name, privacy=False)
                new_group.put()
                
                active_user.groups.append(new_group.key())
                active_user.put()
                
                active_user_football_pools = CAFootballPool.all().filter("user =", active_user).filter("privacy =", False).fetch(1000)
                
                for football_pool in active_user_football_pools:
                    if football_pool.payment:
                        members = new_group.members.fetch(10000)
                        
                        group_ranking = CAGroupRanking(football_pool=football_pool, group=new_group, rank=len(members))
                        group_ranking.put()
                
                members = eval(self.request.get('last-members'))
                
                for member in members:
                    member_key = Key(member[1])
                    user = CAUser.get(member_key)
                    
                    users = []
                    users.append(active_user.key())
                    users.append(user.key())
                    
                    request_membership = CARequestGroupMembership(users=users, status=False, group=new_group)
                    request_membership.put()
                    
                self.redirect('/list/groups/ranking')
        else:
            self.redirect('/')
            
class AddMemberToCompetitionGroup(webapp.RequestHandler):
    def get(self):
        update_session_time()
        session = get_current_session()
        check_session_status()
            
        if session.is_active():
            user_key = Key(self.request.get('user'))
            
            new_member = CAUser.get(user_key)
            
            username = []
            
            members = eval(self.request.get('last_members'))
            searched_users = eval(self.request.get('last_search')) 
                            
            if new_member.type == 0:
                username = new_member.google_user.nickname()
            elif new_member.type == 1:
                username = new_member.facebook_user.name
            else:
                username = new_member.native_user.name
                        
            if username:
                searched_users.remove((str(username), str(new_member.key())))
                members.append((str(username), str(new_member.key())))
                
            template_values = {
                'session_status': True,
                'user': session['active_user'],
                'searched_users': searched_users,
                'members': members,
                'name': self.request.get('name'),
                'last_search': str(searched_users),
                'last_members': str(members),
                'top_scorers': get_top_scorers(),
                'top_users': get_top_users_global_ranking(),
                'last_jackpot': get_last_jackpot()
            }
                    
            render_template(self, 'create_competition_group.html', template_values)
        else:
            self.redirect('/')
            
class DeleteMemberFromCompetitionGroup(webapp.RequestHandler):
    def get(self):
        update_session_time()
        session = get_current_session()
        check_session_status()
            
        if session.is_active():
            user_key = Key(self.request.get('user'))
            
            new_member = CAUser.get(user_key)
            
            username = []
            
            members = eval(self.request.get('last_members'))
            searched_users = eval(self.request.get('last_search')) 
                            
            if new_member.type == 0:
                username = new_member.google_user.nickname()
            elif new_member.type == 1:
                username = new_member.facebook_user.name
            else:
                username = new_member.native_user.name
                        
            if username:
                members.remove((str(username), str(new_member.key())))
                
            template_values = {
                'session_status': True,
                'user': session['active_user'],
                'searched_users': searched_users,
                'members': members,
                'name': self.request.get('name'),
                'last_search': str(searched_users),
                'last_members': str(members),
                'top_scorers': get_top_scorers(),
                'top_users': get_top_users_global_ranking(),
                'last_jackpot': get_last_jackpot()
            }
                    
            render_template(self, 'create_competition_group.html', template_values)
        else:
            self.redirect('/')