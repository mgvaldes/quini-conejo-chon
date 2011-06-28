import logging
import datetime

from google.appengine.ext import webapp
from google.appengine.ext.db import Key

from gaesessions import get_current_session

from ca_utils import check_session_status, render_template, get_total_points, update_session_time, get_pending_membership_requests, get_top_scorers, get_top_users_global_ranking, get_last_jackpot
from models.ca_models import CACompetitonGroup, CAGroupRanking, CAUser, CARequestGroupMembership, CAFootballPool, CAGroupComment

class CommentHandler(webapp.RequestHandler):
    def post(self):
        update_session_time()
        session = get_current_session()
        check_session_status()
            
        if session.is_active():
            comment_text = self.request.get('comment-text')
            selected_competition_group_key = Key(self.request.get('selected_group_key'))
            competition_group = CACompetitonGroup.get(selected_competition_group_key)
            
            google_time = datetime.datetime.today()
            delta = datetime.timedelta(minutes=270)
            comment_time = google_time - delta
            
            comment = CAGroupComment(group=competition_group, user=session['active_user'], comment=comment_text, date=comment_time)
            comment.put()
                        
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
                    
                group_ranking_list.append((name, rank.football_pool.name, get_total_points(rank.football_pool), selected, rank.football_pool.key()))
                
            comments = CAGroupComment.all().filter("group =", competition_group).fetch(10000)
            comments_info = []
            
            for comment in comments:
                if comment.user.type == 0:
                    name = comment.user.google_user.nickname()
                elif comment.user.type == 1:
                    name = comment.user.facebook_user.name
                else:
                    name = comment.user.native_user.name
                    
                comments_info.append((name, str(comment.date.day) + '/' + str(comment.date.month) + '/' + str(comment.date.year) + ' ' + str(comment.date.hour) + ':' + str(comment.date.minute), comment.comment))
                
            template_values = {
                'session_status': True,
                'user': active_user,
                'competition_group_name': competition_group.name,
                'group_ranking': group_ranking_list,
                'top_scorers': get_top_scorers(),
                'top_users': get_top_users_global_ranking(),
                'last_jackpot': get_last_jackpot(),
                'comments': comments_info,
                'selected_group_key': self.request.get('selected_group_key')
            }
            
            render_template(self, 'ranking.html', template_values)
        else:
            self.redirect('/')