from sets import Set

from google.appengine.ext import db
from google.appengine.ext import webapp

from models.ca_models import CAFootballPool, CAMatch, CATeam
from ca_utils import check_session_status, render_template, get_team_whole_name, update_session_time, get_top_scorers, get_pending_membership_requests, get_top_users_global_ranking, get_last_jackpot

from gaesessions import get_current_session

class CreateFootballPoolStepOne(webapp.RequestHandler):
    def get(self):
        update_session_time()
        session = get_current_session()
        check_session_status()
        
        if session.is_active():
            original_pool = CAFootballPool.all().filter("privacy =", True).fetch(1)[0]
            first_round_matches = original_pool.first_round_matches.fetch(18)
            
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
                'top_scorers': get_top_scorers(),
                'top_users': get_top_users_global_ranking(),
                'last_jackpot': get_last_jackpot()
            }
                
            render_template(self, 'create_step1.html', template_values)
        else:
            self.redirect('/')
        
class CreateFootballPoolStepTwo(webapp.RequestHandler):
    def post(self):
        update_session_time()
        session = get_current_session()
        check_session_status()
        
        if session.is_active():
            original_pool = CAFootballPool.all().filter("privacy =", True).fetch(1)[0]
            first_round_matches = original_pool.first_round_matches.fetch(18)
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
                'football_pool_name': self.request.get('football-pool-name'),
                'first_round_matches': str(final_matches),
                'quarter_finals_teams': quarter_finals_teams,
                'top_scorers': get_top_scorers(),
                'top_users': get_top_users_global_ranking(),
                'last_jackpot': get_last_jackpot()
            }     
            
            render_template(self, 'create_step2.html', template_values)
        else:
            self.redirect('/')
        
class SaveCreateFootbalPool(webapp.RequestHandler):
    def post(self):
        update_session_time()
        session = get_current_session()
        check_session_status()
        
        if session.is_active():
            if session.has_key('active_user'):
                football_pool_name = self.request.get('football-pool-name')
                active_user = session['active_user']
                
                active_user_football_pool = CAFootballPool(user=active_user, name=football_pool_name, privacy=False)
                active_user_football_pool.put()
                
                original_pool = CAFootballPool.all().filter("privacy =", True).fetch(1)[0]
                first_round_matches = eval(self.request.get('first-round-matches'))
                original_first_round_matches = original_pool.first_round_matches.fetch(18)
                counter = 0
                
                for match_results in first_round_matches:
                    initials = match_results[0].partition('-')
                    team0_initials = initials[0]
                    initials = initials[2].partition('-')
                    team1_initials = initials[0]
                    
                    team0 = CATeam.all().filter("name =", get_team_whole_name(team0_initials)).fetch(1)[0]
                    team1 = CATeam.all().filter("name =", get_team_whole_name(team1_initials)).fetch(1)[0]
                    
                    teams_list = [team0.key(), team1.key()]
                    
                    original_match = original_first_round_matches[counter]
                    active_user_match = CAMatch(date=original_match.date, goals_team1=int(match_results[1]), goals_team2=int(match_results[3]), teams=teams_list, football_pool=active_user_football_pool)
                    active_user_match.put()
                    counter += 1
                
                second_round_matches = eval(self.request.get('second-round-matches'))
                original_second_round_matches = original_pool.second_round_matches.fetch(8)
                
                for i in range(0, len(original_second_round_matches)):
                    initials = second_round_matches[i][0].partition('-')
                    initials = initials[2].partition('-')
                    team0_initials = initials[0]
                    initials = initials[2].partition('-')
                    team1_initials = initials[0]
                    
                    team0 = CATeam.all().filter("name =", get_team_whole_name(team0_initials)).fetch(1)[0]
                    team1 = CATeam.all().filter("name =", get_team_whole_name(team1_initials)).fetch(1)[0]
                    #print team0.name + ' ' + second_round_matches[i][1] + ' ' + second_round_matches[i][3] + ' ' + team1.name
                    
                    teams_list = [team0.key(), team1.key()]
                    
                    original_match = original_second_round_matches[i]
                    active_user_match = CAMatch(date=original_match.date, goals_team1=int(second_round_matches[i][1]), goals_team2=int(second_round_matches[i][3]), teams=teams_list, football_pool=active_user_football_pool)
                    active_user_match.put()
                
                template_values = {
                    'user': session['active_user'],
                    'top_scorers': get_top_scorers(),
                    'top_users': get_top_users_global_ranking(),
                    'last_jackpot': get_last_jackpot()
                }
                        
                render_template(self, 'home.html', template_values)
        else:
            self.redirect('/')
                
        
        
        