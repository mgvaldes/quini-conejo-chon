from google.appengine.ext import webapp

from gaesessions import get_current_session

from ca_utils import check_session_status, render_template
from models.ca_models import CAGroupRanking, CACompetitonGroup

class ViewGlobalRanking(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        
        check_session_status()
            
        if session.is_active():
            if session.has_key('active_user'):
                active_user = session['active_user']
                
                global_competition_group = CACompetitonGroup.all().filter("privacy =", True).fetch(1)[0]
                global_rank = CAGroupRanking.gql("WHERE group = :1 ORDER BY rank", global_competition_group.key()).fetch(10000)
                
                global_rank_list = []
                
                for rank in global_rank:
                    if rank.user.key() == active_user.key():
                        current_user = True
                    else:
                        current_user = False
                    
                    if rank.user.type == 0:
                        user_name = rank.user.google_user
                    elif rank.user.type == 1:
                        user_name = rank.user.facebook_user.name
                    else:
                        user_name = rank.user.native_user.name
                    
                    global_rank_list.append((user_name, rank.rank, current_user))
                
                template_values = {
                    'ranking': global_rank_list,
                    'competition_group_name': global_competition_group.name
                }
                
                render_template(self, 'view_global_ranking.html', template_values)
        else:
            self.redirect('/')