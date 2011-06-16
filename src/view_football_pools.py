from sets import Set

from google.appengine.ext import webapp
from google.appengine.ext.db import Key
from google.appengine.ext import db

from gaesessions import get_current_session

from ca_utils import check_session_status, render_template, update_session_time
from models.ca_models import CAFootballPool

class ListFootballPools(webapp.RequestHandler):
    def get(self):
        update_session_time()
        session = get_current_session()
        check_session_status()
            
        if session.is_active():
            if session.has_key('active_user'):
                active_user = session['active_user']
                
                active_user_football_pools = CAFootballPool.all().filter("user =", active_user).filter("privacy =", False).fetch(1000)
                
                template_values = {
                    'football_pools': active_user_football_pools,
                    'message':''
                } 
                
                render_template(self, 'list_football_pools.html', template_values)
        else:
            self.redirect('/')
            
class ViewFootballPool(webapp.RequestHandler):
    def post(self):
        update_session_time()
        session = get_current_session()
        check_session_status()
            
        if session.is_active():
            selected = self.request.get('selected_football_pool')
            
            if selected != "default":
                selected_football_pool_key = Key(selected)
                
                view = self.request.get('view')
                pay = self.request.get('pay')
                edit = self.request.get('edit')
                
                if view:
                    selected_football_pool = CAFootballPool.get(selected_football_pool_key)
                    first_round_matches = selected_football_pool.first_round_matches
                    
                    ga_team_set = Set()
                    gb_team_set = Set()
                    gc_team_set = Set()
                    
                    for match in first_round_matches:
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
                    
                    for match in first_round_matches:
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
                            
                    second_round_matches = selected_football_pool.second_round_matches.fetch(8)
                    
                    quarter_finals_matches = []
                    
                    for i in range(0, 4):
                        match = second_round_matches[i]
                        match_info = []
                        team_list = db.get(match.teams)
                        
                        match_info.append(team_list[0].name)
                        match_info.append(str(match.goals_team1))
                        match_info.append(str(match.goals_team2))
                        match_info.append(team_list[1].name)
                        match_info.append(str(i + 1))
                        
                        quarter_finals_matches.append(match_info)
                        
                    semi_final_matches = []
                        
                    for i in range(4, 6):
                        match = second_round_matches[i]
                        match_info = []
                        team_list = db.get(match.teams)
                        
                        match_info.append(team_list[0].name)
                        match_info.append(str(match.goals_team1))
                        match_info.append(str(match.goals_team2))
                        match_info.append(team_list[1].name)
                        match_info.append(str(i - 3))
                        
                        semi_final_matches.append(match_info)
                        
                    match = second_round_matches[6]
                    third_fourth_match = []
                    team_list = db.get(match.teams)
                       
                    third_fourth_match.append(team_list[0].name)
                    third_fourth_match.append(str(match.goals_team1))
                    third_fourth_match.append(str(match.goals_team2))
                    third_fourth_match.append(team_list[1].name)
                    
                    match = second_round_matches[7]
                    final_match = []
                    team_list = db.get(match.teams)
                       
                    final_match.append(team_list[0].name)
                    final_match.append(str(match.goals_team1))
                    final_match.append(str(match.goals_team2))
                    final_match.append(team_list[1].name)
                    
                    template_values = {
                        'name': selected_football_pool.name,
                        'groups': [(ga_results, ga_teams_info, 'A'), (gb_results, gb_teams_info, 'B'), (gc_results, gc_teams_info, 'C')],
                        'quarter_finals_matches': quarter_finals_matches,
                        'semi_final_matches': semi_final_matches,
                        'third_fourth_match': third_fourth_match,
                        'final_match': final_match
                    } 
                        
                    render_template(self, 'view_football_pool.html', template_values)
                elif pay:
                    selected_football_pool = CAFootballPool.get(Key(self.request.get('selected_football_pool')))
                    
                    if selected_football_pool.payment:
                        active_user = session['active_user']
                    
                        active_user_football_pools = CAFootballPool.all().filter("user =", active_user).filter("privacy =", False).fetch(1000)
                        
                        template_values = {
                            'football_pools': active_user_football_pools,
                            'message':'Esta quiniela ya fue pagada'
                        } 
                        
                        render_template(self, 'list_football_pools.html', template_values)
                    else:
                        template_values = {
                            'selected_football_pool_key': self.request.get('selected_football_pool')
                        }
                        
                        render_template(self, 'pay_football_pool.html', template_values)
                elif edit:
                    selected_football_pool = CAFootballPool.get(selected_football_pool_key)
                    first_round_matches = selected_football_pool.first_round_matches
                    
                    ga_team_set = Set()
                    gb_team_set = Set()
                    gc_team_set = Set()
                        
                    for match in first_round_matches:
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
                        
                    for match in first_round_matches:
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
                            
                    template_values = {
                        'name': selected_football_pool.name,
                        'groups': [(ga_results, ga_teams_info, 'A'), (gb_results, gb_teams_info, 'B'), (gc_results, gc_teams_info, 'C')],
                        'test': str([['qf1', 'Arg-Col'], ['qf2', 'Uru-Chi'], ['qf3', 'Bol-Cos'], ['qf4', 'Ven-Ecu']]),
                        'football_pool_key': selected_football_pool.key()
                    } 
                            
                    render_template(self, 'edit_step1.html', template_values)
            else:
                self.redirect('/list')
        else:
            self.redirect('/')