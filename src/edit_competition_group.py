from google.appengine.ext import webapp
from google.appengine.ext.db import Key

from gaesessions import get_current_session

from ca_utils import check_session_status, render_template, get_total_points, update_session_time, get_pending_membership_requests, get_top_scorers, get_top_users_global_ranking, get_last_jackpot
from models.ca_models import CACompetitonGroup, CAUser, CAFootballPool, CAGroupRanking, CARequestGroupMembership

class EditCACompetitionGroup(webapp.RequestHandler):
    def get(self):
        update_session_time()
        session = get_current_session()
        check_session_status()
            
        if session.is_active():
            selected_competition_group_key = Key(self.request.get('id'))
            competition_group = CACompetitonGroup.get(selected_competition_group_key)
            
            members = competition_group.members.fetch(10000)
            current_members = []
            
            for user in members:
                username = ''
                
                if user.type == 0:
					username = user.google_user.nickname() + " " + user.google_user.email()
                elif user.type == 1:
                    username = user.facebook_user.name
                else:
					username = user.native_user.name + " " + user.native_user.email
            
                if username:
					current_members.append((str(username), str(user.key()), False))
            
            template_values = {
                'session_status': True,
                'user': session['active_user'],
                'searched_users': [],
                'members': current_members,
                'name': competition_group.name,
                'last_search': str([]),
                'last_members': str(current_members),
                'top_scorers': get_top_scorers(),
                'top_users': get_top_users_global_ranking(),
                'last_jackpot': get_last_jackpot(),
                'selected_football_pool': str(selected_competition_group_key)
            }
            
            render_template(self, 'edit_competition_group.html', template_values)
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
                search_result = []
                selected_competition_group_key = Key(self.request.get('selected-football-pool'))
                competition_group = CACompetitonGroup.get(selected_competition_group_key)
                members = competition_group.members.fetch(10000)
                members_keys = []
                
                for member in members:
                    members_keys.append(member.key())
                
                if search_term:
                    users = CAUser.all().fetch(10000)
                    
                    for user in users:
                        if active_user.key() != user.key():
                            if user.key() not in members_keys:
                                username = []
                                
                                if user.type == 0:
                                    nickname = user.google_user.nickname()
                                    email = user.google_user.email()
                                    
                                    if (search_term.lower() in str(nickname).lower()) or (search_term.lower() in str(email).lower()):
                                        username = nickname +" "+email
                                elif user.type == 1:
                                    name = user.facebook_user.name
                                    
                                    if search_term.lower() in str(name).lower():
                                        username = name
                                else:
                                    name = user.native_user.name
                                    email = user.native_user.email
                                    
                                    if (search_term.lower() in str(name).lower()) or (search_term.lower() in str(email).lower()):
                                        username = name+" "+email
                            
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
                    'last_jackpot': get_last_jackpot(),
                    'selected_football_pool': self.request.get('selected-football-pool')
                }
                
                render_template(self, 'edit_competition_group.html', template_values)
            elif save:
                active_user = session['active_user']                
                name = self.request.get('name')
                
                selected_competition_group_key = Key(self.request.get('selected-football-pool'))
                competition_group = CACompetitonGroup.get(selected_competition_group_key)
                
                if competition_group.name != name:
                    competition_group.name = name
                    competition_group.put()
               
#                new_group = CACompetitonGroup(name=name, privacy=False)
#                new_group.put()
#                
#                active_user.groups.append(new_group.key())
#                active_user.put()
                
#                active_user_football_pools = CAFootballPool.all().filter("user =", active_user).filter("privacy =", False).fetch(1000)
#                
#                for football_pool in active_user_football_pools:
#                    if football_pool.payment:
#                        members = new_group.members.fetch(10000)
#                        
#                        group_ranking = CAGroupRanking(football_pool=football_pool, group=new_group, rank=len(members))
#                        group_ranking.put()
                
                members = eval(self.request.get('last-members'))
                
                for member in members:
                    if member[2]:
                        member_key = Key(member[1])
                        user = CAUser.get(member_key)
                        
                        users = []
                        users.append(active_user.key())
                        users.append(user.key())
                        
                        request_membership = CARequestGroupMembership(users=users, status=False, group=competition_group)
                        request_membership.put()
                    
                self.redirect('/list/groups/ranking')
        else:
            self.redirect('/')
            
class EditAddMemberToCompetitionGroup(webapp.RequestHandler):
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
                username = new_member.google_user.nickname() + " " + new_member.google_user.email()
            elif new_member.type == 1:
                username = new_member.facebook_user.name
            else:
                username = new_member.native_user.name + " " + new_member.native_user.email
                        
            if username:
                searched_users.remove((str(username), str(new_member.key())))
                members.append((str(username), str(new_member.key()), True))
                
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
                'last_jackpot': get_last_jackpot(),
                'selected_football_pool': self.request.get('selected-football-pool')
            }
                    
            render_template(self, 'edit_competition_group.html', template_values)
        else:
            self.redirect('/')
            
class EditDeleteMemberFromCompetitionGroup(webapp.RequestHandler):
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
                username = new_member.google_user.nickname() + " " + new_member.google_user.email()
            elif new_member.type == 1:
                username = new_member.facebook_user.name
            else:
                username = new_member.native_user.name + " " + new_member.native_user.email
                        
            if username:
                members.remove((str(username), str(new_member.key()), True))
                
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
                'last_jackpot': get_last_jackpot(),
                'selected_football_pool': self.request.get('selected-football-pool')
            }
                    
            render_template(self, 'edit_competition_group.html', template_values)
        else:
            self.redirect('/')