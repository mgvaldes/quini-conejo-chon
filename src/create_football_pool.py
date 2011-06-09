import os.path
import datetime

from sets import Set

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from models.ca_models import CAFootballPool, CATeam

from gaesessions import get_current_session

class CreateFootballPoolStepOne(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        
        if session.has_key('session_timestamp'):
            session_timestamp = session['session_timestamp']
            delta = datetime.timedelta(minutes=-10)
            
            if (datetime.datetime.today() > (session_timestamp - delta)):
                session.terminate()
        
        if session.is_active():
            original_pool = CAFootballPool.all().filter("privacy =", True).fetch(1)[0]
            first_round_matches = original_pool.first_round_matches
            
            group_a_teams = []
            group_b_teams = []
            group_c_teams = []
            
            ga_teams = Set()
            gb_teams = Set()
            gc_teams = Set()
            
            for match in first_round_matches:
                team_list = db.get(match.teams)
                
                if team_list[0].group.name == 'A':
                    group_a_teams.append((team_list[0].name, team_list[1].name))
                    ga_teams.add(team_list[0].name)
                    ga_teams.add(team_list[1].name)
                elif team_list[0].group.name == 'B':
                    group_b_teams.append((team_list[0].name, team_list[1].name))
                    gb_teams.add(team_list[0].name)
                    gb_teams.add(team_list[1].name)
                else:
                    group_c_teams.append((team_list[0].name, team_list[1].name))
                    gc_teams.add(team_list[0].name)
                    gc_teams.add(team_list[1].name)
                    
            a_teams = list(ga_teams)
            b_teams = list(gb_teams)
            c_teams = list(gc_teams)
            
            ga_teams = []
            gb_teams = []
            gc_teams = []
            
            for counter in range(0, 4):
                if counter % 2 == 1:
                    ga_teams.append((a_teams[counter], "odd"))
                    gb_teams.append((b_teams[counter], "odd"))
                    gc_teams.append((c_teams[counter], "odd"))
                else:
                    ga_teams.append((a_teams[counter], "pair"))
                    gb_teams.append((b_teams[counter], "pair"))
                    gc_teams.append((c_teams[counter], "pair"))
                
            template_values = {
                'groups': [(group_a_teams, ga_teams, 'A'), (group_b_teams, gb_teams, 'B'), (group_c_teams, gc_teams, 'C')],
                'test': str([['qf1', 'Arg-Col'], ['qf2', 'Uru-Chi'], ['qf3', 'Bol-Cos'], ['qf4', 'Ven-Ecu']])
            }
                
            path = os.path.join(os.path.dirname(__file__), 'create_step1.html')
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect('/')
        
def get_team_whole_name(team1_initials, team2_initials):
    teams = CATeam.all().fetch(12)
    
    team_names = []
    
    for team in teams:
        if team.name[:3] == team1_initials or team.name[:3] == team2_initials:
            team_names.append(team.name)
            
            if len(team_names) == 2:
                break 
    
    return team_names
        
class CreateFootballPoolStepTwo(webapp.RequestHandler):
    def post(self):
        session = get_current_session()
        
        if session.has_key('session_timestamp'):
            session_timestamp = session['session_timestamp']
            delta = datetime.timedelta(minutes=-10)
            
            if (datetime.datetime.today() > (session_timestamp - delta)):
                session.terminate()
        
        if session.is_active():
            original_pool = CAFootballPool.all().filter("privacy =", True).fetch(1)[0]
            first_round_matches = original_pool.first_round_matches
            final_matches = []
            
            for match in first_round_matches:
                team_list = db.get(match.teams)
                match_list = []
                
                key0 = team_list[0].name[:3]
                key1 = team_list[1].name[:3]
                
                final_key1 = key0 + '-' + key1 + '-g1'
                final_key2 = key0 + '-' + key1 + '-g2'
                
                match_list.append(final_key1)
                match_list.append(self.request.get(final_key1))
                match_list.append(final_key2)
                match_list.append(self.request.get(final_key2))
                
                final_matches.append(match_list)
            
            first_round_winners = eval(self.request.get('first-round-winners'))
            quarter_finals_teams = []
            
            for winners in first_round_winners:
                initials = winners[1].partition('-')
                team_names = get_team_whole_name(initials[0], initials[2])
                quarter_finals_teams.append(team_names)
                
            template_values = {
                'football_pool_name': self.request.get('football-pool-name'),
                'first_round_matches': str(final_matches),
                'quarter_finals_teams': quarter_finals_teams,
                'test': ([['qf1', 'Arg-Col'], ['qf2', 'Uru-Chi'], ['qf3', 'Bol-Cos'], ['qf4', 'Ven-Ecu']], ['sf1', 'Ven-Bol'], ['sf2', 'Col-Bol'], ['tf', 'Ecu-Chi'], ['f', 'Ven-Bra'])
            }     
            
            path = os.path.join(os.path.dirname(__file__), 'create_step2.html')    
            self.response.out.write(template.render(path, template_values))
        else:
            self.redirect('/')
        
class SaveFootbalPool(webapp.RequestHandler):
    def post(self):
        football_pool_name = self.request.get('football-pool-name')
        first_round_matches = eval(self.request.get('first-round-matches'))
        second_roud_matches = eval(self.request.get('second-round-matches'))
        
        original_pool = CAFootballPool.all().filter("privacy =", True).fetch(1)[0]
        
        first_round_matches = original_pool.first_round_matches
        second_round_matches = original_pool.second_round_matches
                    
        
                
        
        
        