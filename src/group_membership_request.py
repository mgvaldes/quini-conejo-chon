from google.appengine.ext import webapp
from google.appengine.ext.db import Key

from gaesessions import get_current_session

from ca_utils import check_session_status, render_template, get_pending_membership_requests, update_session_time, get_top_scorers, get_top_users_global_ranking
from models.ca_models import CARequestGroupMembership, CAFootballPool, CAGroupRanking

class AcceptGroupMembershipRequest(webapp.RequestHandler):
    def get(self):
        update_session_time()
        session = get_current_session()
        check_session_status()
            
        if session.is_active():
            member_request = CARequestGroupMembership.get(Key(self.request.get('request')))
            active_user = session['active_user']
            
            active_user.groups.append(member_request.group.key())
            active_user.put()
            
            active_user_football_pools = CAFootballPool.all().filter("user =", active_user).filter("privacy =", False).fetch(1000)
            members = member_request.group.members.fetch(10000)
                
            for football_pool in active_user_football_pools:
                if football_pool.payment:
                    groups = active_user.groups
                        
                    group_ranking = CAGroupRanking(football_pool=football_pool, group=member_request.group, rank=len(members))
                    group_ranking.put()
                    
            CARequestGroupMembership.delete(member_request)
            
            template_values = {
                'user': session['active_user'],
                'pending_membership_requests': get_pending_membership_requests(session['active_user']),
                'top_scorers': get_top_scorers(),
                'top_users': get_top_users_global_ranking()
            }
                        
            render_template(self, 'home.html', template_values)
        else:
            self.redirect('/')

class RejectGroupMembershipRequest(webapp.RequestHandler):
    def get(self):
        update_session_time()
        session = get_current_session()
        check_session_status()
            
        if session.is_active():
            member_request = CARequestGroupMembership.get(Key(self.request.get('request')))
            CARequestGroupMembership.delete(member_request)
            
            template_values = {
                'user': session['active_user'],
                'pending_membership_requests': get_pending_membership_requests(session['active_user']),
                'top_scorers': get_top_scorers(),
                'top_users': get_top_users_global_ranking()
            }
                        
            render_template(self, 'home.html', template_values)
        else:
            self.redirect('/')
