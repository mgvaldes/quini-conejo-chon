from sets import Set

from google.appengine.ext import webapp
from google.appengine.ext import db

from gaesessions import get_current_session

from ca_utils import check_session_status, render_template, get_top_scorers, get_top_users_global_ranking, get_last_jackpot, get_total_points,\
    get_upcomming_matches
from models.ca_models import CAFootballPool

class ViewCopaAmerica(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        
        check_session_status()
            
        if session.is_active():
            upcomming_matches = get_upcomming_matches()
            upcomming_matches_info = []
            
            for match in upcomming_matches:
                team_list = db.get(match.teams)
                
                upcomming_matches_info.append((team_list[0].name, team_list[1].name, str(match.date)))
            
            copa_america = CAFootballPool.all().filter("privacy =", True).fetch(1)[0]
            
            copa_america_first_round_matches = copa_america.first_round_matches
            
            ga_team_set = Set()
            gb_team_set = Set()
            gc_team_set = Set()
            
            for match in copa_america_first_round_matches:
                team_list = db.get(match.teams)
                
                if team_list[0].group.name == 'A':
                    ga_team_set.add(team_list[0].name)
                    ga_team_set.add(team_list[1].name)
                elif team_list[0].group.name == 'B':
                    gb_team_set.add(team_list[0].name)
                    gb_team_set.add(team_list[1].name)
                else:
                    gc_team_set.add(team_list[0].name)
                    gc_team_set.add(team_list[1].name)
                    
            a_teams = list(ga_team_set)
            b_teams = list(gb_team_set)
            c_teams = list(gc_team_set)
            
            ga_teams_info = []
            gb_teams_info = []
            gc_teams_info = []
            
            for counter in range(0, 4):
                if counter % 2 == 1:
                    ga_teams_info.append((a_teams[counter], "odd"))
                    gb_teams_info.append((b_teams[counter], "odd"))
                    gc_teams_info.append((c_teams[counter], "odd"))
                else:
                    ga_teams_info.append((a_teams[counter], "pair"))
                    gb_teams_info.append((b_teams[counter], "pair"))
                    gc_teams_info.append((c_teams[counter], "pair"))
                    
            ga_results = []
            gb_results = []
            gc_results = []
            
            for match in copa_america_first_round_matches:
                match_info = []
                team_list = db.get(match.teams)
                
                match_info.append(team_list[0].name)
                match_info.append(str(match.goals_team1))
                match_info.append(str(match.goals_team2))
                match_info.append(team_list[1].name)
                
                if team_list[0].group.name == 'A':
                    ga_results.append(match_info)
                elif team_list[0].group.name == 'B':
                    gb_results.append(match_info)
                else:
                    gc_results.append(match_info)
                    
            second_round_matches = copa_america.second_round_matches.fetch(8)
                    
            quarter_finals_matches = []
            
            for i in range(0, 4):
                match = second_round_matches[i]
                match_info = []
                team_list = db.get(match.teams)
                
                if team_list:
                    match_info.append(team_list[0].name)
                    match_info.append(str(match.goals_team1))
                    match_info.append(str(match.goals_team2))
                    match_info.append(team_list[1].name)
                    match_info.append(str(i + 1))
                else:
                    match_info.append('?')
                    match_info.append('')
                    match_info.append('')
                    match_info.append('?')
                    match_info.append(str(i + 1))
                
                quarter_finals_matches.append(match_info)
                
            semi_final_matches = []
                
            for i in range(4, 6):
                match = second_round_matches[i]
                match_info = []
                team_list = db.get(match.teams)
                
                if team_list:
                    match_info.append(team_list[0].name)
                    match_info.append(str(match.goals_team1))
                    match_info.append(str(match.goals_team2))
                    match_info.append(team_list[1].name)
                    match_info.append(str(i - 3))
                else:
                    match_info.append('?')
                    match_info.append('')
                    match_info.append('')
                    match_info.append('?')
                    match_info.append(str(i - 3))
                
                semi_final_matches.append(match_info)
                
            match = second_round_matches[6]
            third_fourth_match = []
            team_list = db.get(match.teams)
               
            if team_list:
                third_fourth_match.append(team_list[0].name)
                third_fourth_match.append(str(match.goals_team1))
                third_fourth_match.append(str(match.goals_team2))
                third_fourth_match.append(team_list[1].name)
            else:
                third_fourth_match.append('?')
                third_fourth_match.append('')
                third_fourth_match.append('')
                third_fourth_match.append('?')
            
            match = second_round_matches[7]
            final_match = []
            team_list = db.get(match.teams)
            
            if team_list:
                final_match.append(team_list[0].name)
                final_match.append(str(match.goals_team1))
                final_match.append(str(match.goals_team2))
                final_match.append(team_list[1].name)
            else:
                final_match.append('?')
                final_match.append('')
                final_match.append('')
                final_match.append('?')
            
            template_values = {
                'session_status': True,
                'user': session['active_user'],
                'upcomming_matches_info': upcomming_matches_info,
                'name': copa_america.name,
                'groups': [(ga_results, ga_teams_info, 'A'), (gb_results, gb_teams_info, 'B'), (gc_results, gc_teams_info, 'C')],
                'quarter_finals_matches': quarter_finals_matches,
                'semi_final_matches': semi_final_matches,
                'third_fourth_match': third_fourth_match,
                'final_match': final_match,
                'top_scorers': get_top_scorers(),
                'top_users': get_top_users_global_ranking(),
                'last_jackpot': get_last_jackpot()
            }
        else:
            template_values = {
                'session_status': False,
                'upcomming_matches_info': upcomming_matches_info,
                'name': copa_america.name,
                'groups': [(ga_results, ga_teams_info, 'A'), (gb_results, gb_teams_info, 'B'), (gc_results, gc_teams_info, 'C')],
                'quarter_finals_matches': quarter_finals_matches,
                'semi_final_matches': semi_final_matches,
                'third_fourth_match': third_fourth_match,
                'final_match': final_match,
                'top_scorers': get_top_scorers(),
                'top_users': get_top_users_global_ranking(),
                'last_jackpot': get_last_jackpot()
            }
            
        render_template(self, 'copa_america.html', template_values)