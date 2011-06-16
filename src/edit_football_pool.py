from sets import Set

from google.appengine.ext import db
from google.appengine.ext.db import Key
from google.appengine.ext import webapp

from models.ca_models import CAFootballPool, CAMatch, CATeam
from ca_utils import check_session_status, render_template, get_team_whole_name, update_session_time

from gaesessions import get_current_session

#class EditFootballPoolStepOne(webapp.RequestHandler):
#    def get(self):
#        update_session_time()
#        session = get_current_session()
#        check_session_status()
#        
#        if session.is_active():
#            selected = self.request.get('selected_football_pool')
#            
#            if selected != "default":
#                selected_football_pool_key = Key(selected)
#                
#                selected_football_pool = CAFootballPool.get(selected_football_pool_key)
#                first_round_matches = selected_football_pool.first_round_matches
#                
#                ga_team_set = Set()
#                gb_team_set = Set()
#                gc_team_set = Set()
#                    
#                for match in first_round_matches:
#                    team_list = db.get(match.teams)
#                        
#                    if team_list[0].group.name == 'A':
#                        ga_team_set.add(team_list[0].name)
#                        ga_team_set.add(team_list[1].name)
#                    elif team_list[0].group.name == 'B':
#                        gb_team_set.add(team_list[0].name)
#                        gb_team_set.add(team_list[1].name)
#                    else:
#                        gc_team_set.add(team_list[0].name)
#                        gc_team_set.add(team_list[1].name)
#                            
#                a_teams = list(ga_team_set)
#                b_teams = list(gb_team_set)
#                c_teams = list(gc_team_set)
#                    
#                ga_teams_info = []
#                gb_teams_info = []
#                gc_teams_info = []
#                    
#                for counter in range(0, 4):
#                    if counter % 2 == 1:
#                        ga_teams_info.append((a_teams[counter], "odd"))
#                        gb_teams_info.append((b_teams[counter], "odd"))
#                        gc_teams_info.append((c_teams[counter], "odd"))
#                    else:
#                        ga_teams_info.append((a_teams[counter], "pair"))
#                        gb_teams_info.append((b_teams[counter], "pair"))
#                        gc_teams_info.append((c_teams[counter], "pair"))
#                            
#                ga_results = []
#                gb_results = []
#                gc_results = []
#                    
#                for match in first_round_matches:
#                    match_info = []
#                    team_list = db.get(match.teams)
#                        
#                    match_info.append(team_list[0].name)
#                    match_info.append(str(match.goals_team1))
#                    match_info.append(str(match.goals_team2))
#                    match_info.append(team_list[1].name)
#                        
#                    if team_list[0].group.name == 'A':
#                        ga_results.append(match_info)
#                    elif team_list[0].group.name == 'B':
#                        gb_results.append(match_info)
#                    else:
#                        gc_results.append(match_info)
#                        
#                template_values = {
#                    'name': selected_football_pool.name,
#                    'groups': [(ga_results, ga_teams_info, 'A'), (gb_results, gb_teams_info, 'B'), (gc_results, gc_teams_info, 'C')],
#                    'test': str([['qf1', 'Arg-Col'], ['qf2', 'Uru-Chi'], ['qf3', 'Bol-Cos'], ['qf4', 'Ven-Ecu']]),
#                    'football_pool_key': selected_football_pool.key()
#                } 
#                        
#                render_template(self, 'edit_step1.html', template_values)
#            else:
#                self.redirect('/list')
#        else:
#            self.redirect('/')
        
class EditFootballPoolStepTwo(webapp.RequestHandler):
    def post(self):
        update_session_time()
        session = get_current_session()
        check_session_status()
        
        if session.is_active():
            selected_football_pool_key = Key(self.request.get('football-pool-key'))
                
            selected_football_pool = CAFootballPool.get(selected_football_pool_key)
            first_round_matches = selected_football_pool.first_round_matches
            final_matches = []
            change_first_round = False
            
            for match in first_round_matches:
                team_list = db.get(match.teams)
                match_list = []
                
                key0 = team_list[0].name[:3]
                key1 = team_list[1].name[:3]
                
                final_key1 = key0 + '-' + key1 + '-g1'
                final_key2 = key0 + '-' + key1 + '-g2'

                if (match.goals_team1 != int(self.request.get(final_key1))) or (match.goals_team2 != int(self.request.get(final_key2))):
                    change_first_round = True
                                
                match_list.append(final_key1)
                match_list.append(self.request.get(final_key1))
                match_list.append(final_key2)
                match_list.append(self.request.get(final_key2))
                
                final_matches.append(match_list)
            
            if change_first_round:
                first_round_winners = eval(self.request.get('first-round-winners'))
                quarter_finals_teams = []
                
                counter = 1
                for winners in first_round_winners:
                    initials = winners[1].partition('-')
                    team_names = []
                    team_names.append(get_team_whole_name(initials[0]))
                    team_names.append(get_team_whole_name(initials[2]))
                    team_names.append(counter)
                    quarter_finals_teams.append(team_names)
                    counter += 1
                
                template_values = {
                    'football_pool_key': selected_football_pool.key(),
                    'first_round_matches': str(final_matches),
                    'quarter_finals_teams': quarter_finals_teams,
                    'test': str([['qf1-Arg-Col-g1', '2', 'qf1-Arg-Col-g2', '2'], 
                                 ['qf2-Uru-Chi-g1', '3', 'qf2-Uru-Chi-g2', '0'], 
                                 ['qf3-Bol-Cos-g1', '0', 'qf3-Bol-Cos-g2', '4'], 
                                 ['qf4-Ven-Ecu-g1', '6', 'qf4-Ven-Ecu-g2', '2'], 
                                 ['sf1-Ven-Bol-g1', '2', 'sf1-Ven-Bol-g2', '1'], 
                                 ['sf2-Col-Bol-g1', '0', 'sf2-Col-Bol-g2', '1'], 
                                 ['tf-Ecu-Chi-g1', '1', 'tf-Ecu-Chi-g2', '4'], 
                                 ['f-Ven-Bra-g1', '3', 'f-Ven-Bra-g2', '2']])
                }
                
                render_template(self, 'edit_step2_1.html', template_values)
            else:
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
                    'football_pool_key': selected_football_pool.key(),
                    'first_round_matches': str([]),
                    'quarter_finals_matches': quarter_finals_matches,
                    'semi_final_matches': semi_final_matches,
                    'third_fourth_match': third_fourth_match,
                    'final_match': final_match,
                    'test': str([['qf1-Arg-Col-g1', '2', 'qf1-Arg-Col-g2', '2'], 
                                 ['qf2-Uru-Chi-g1', '3', 'qf2-Uru-Chi-g2', '0'], 
                                 ['qf3-Bol-Cos-g1', '0', 'qf3-Bol-Cos-g2', '4'], 
                                 ['qf4-Ven-Ecu-g1', '6', 'qf4-Ven-Ecu-g2', '2'], 
                                 ['sf1-Ven-Bol-g1', '2', 'sf1-Ven-Bol-g2', '1'], 
                                 ['sf2-Col-Bra-g1', '3', 'sf2-Col-Bra-g2', '1'], 
                                 ['tf-Bol-Col-g1', '1', 'tf-Bol-Col-g2', '4'], 
                                 ['f-Ven-Bra-g1', '2', 'f-Ven-Bra-g2', '0']])
                }
            
            render_template(self, 'edit_step2_2.html', template_values)
        else:
            self.redirect('/')
        
class SaveEditFootbalPool(webapp.RequestHandler):
    def post(self):
        update_session_time()
        session = get_current_session()
        check_session_status()
        
        if session.is_active():
            if session.has_key('active_user'):
                selected_football_pool_key = Key(self.request.get('football-pool-key'))
                selected_football_pool = CAFootballPool.get(selected_football_pool_key)
                
                selected_first_round_matches = selected_football_pool.first_round_matches.fetch(18)
                first_round_matches = eval(self.request.get('first-round-matches'))
                
                if first_round_matches: #Hay cambios en la primera fase
                    counter = 0
                
                    for match_results in first_round_matches:
                        selected_match = selected_first_round_matches[counter]
                        
                        selected_match.goals_team1 = int(match_results[1])
                        selected_match.goals_team2 = int(match_results[3])
                        selected_match.put()
                
                second_round_matches = eval(self.request.get('second-round-matches'))
                selected_second_round_matches = selected_football_pool.second_round_matches.fetch(8)
                
                for i in range(0, len(selected_second_round_matches)):
                    initials = second_round_matches[i][0].partition('-')
                    initials = initials[2].partition('-')
                    team0_initials = initials[0]
                    initials = initials[2].partition('-')
                    team1_initials = initials[0]
                    
                    team0 = CATeam.all().filter("name =", get_team_whole_name(team0_initials)).fetch(1)[0]
                    team1 = CATeam.all().filter("name =", get_team_whole_name(team1_initials)).fetch(1)[0]
                    
                    teams_list = [team0.key(), team1.key()]
                    
                    selected_match = selected_second_round_matches[i]
                    selected_match.goals_team1 = int(second_round_matches[i][1])
                    selected_match.goals_team2 = int(second_round_matches[i][3])
                    selected_match.teams = teams_list
                    selected_match.put()
                
                template_values = {
                    'user': session['active_user']
                }
                        
                render_template(self, 'home.html', template_values)
        else:
            self.redirect('/')