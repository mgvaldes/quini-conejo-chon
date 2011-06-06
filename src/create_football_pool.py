import datetime
import os.path

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from models.ca_models import CAFootballPool

#from gaesessions import get_current_session

class CreateFootballPoll(webapp.RequestHandler):
    def get(self):
        #session = get_current_session()
        
        #if session.is_active():
        original_pool = CAFootballPool.all().filter("privacy =", True).fetch(1)[0]
            
        matches = original_pool.matches.filter("date >=", datetime.datetime(2011, 6, 30, 20, 15, 0)).filter("date <=", datetime.datetime(2011, 7, 13, 17, 45, 0)).order('date').fetch(18)
        
        teams = []
        
        for match in matches:
            team_pair_list = db.GqlQuery("SELECT * FROM CATeam WHERE teams = :1", match.teams)
            team_pair = {
                'team1': team_pair_list[0],
                'team2': team_pair_list[1]
            }
            
            teams.append(team_pair)
            
        template_values = {
            'teams': teams
        }
            
        path = os.path.join(os.path.dirname(__file__), 'create.html')
        self.response.out.write(template.render(path, template_values))
         
        
        