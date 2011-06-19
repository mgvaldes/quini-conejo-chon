import datetime
import os.path

from google.appengine.ext.webapp import template

from gaesessions import get_current_session

from models.ca_models import CATeam, CAUser, CAFootballPool, CAScorer, CAMatch, CAJackPot

def check_session_status():
    session = get_current_session()
        
    if session.has_key('session_timestamp'):
        session_timestamp = session['session_timestamp']
        delta = datetime.timedelta(minutes=-10)
            
        if (datetime.datetime.today() > (session_timestamp - delta)):
            session.terminate()
            
def render_template(handler, page, template_values):
    path = os.path.join(os.path.dirname(__file__), page)
    handler.response.out.write(template.render(path, template_values))
    
def save_session_info(ca_user):
    session = get_current_session()
    
    session['active_user'] = ca_user
    session['session_timestamp'] = datetime.datetime.today()
    
def update_session_time():
    session = get_current_session()
    session['session_timestamp'] = datetime.datetime.today()
    
def get_team_whole_name(team_initials):
    teams = CATeam.all().fetch(12)
    
    for team in teams:
        if team.name[:3] == team_initials:
            return team.name
        
def get_pending_membership_requests(ca_user):
    membership_requests = ca_user.pending_membership_requests
    pending_membership_requests = []
    
    for membership_request in membership_requests:
        user = CAUser.get(membership_request.users[0])
        username = []
        
        if user.type == 0:
            username = user.google_user.nickname()
        elif user.type == 1:
            username = user.facebook_user.name
        else:
            username = user.native_user.name
        
        if username:
            pending_membership_requests.append((str(username), str(membership_request.group.name), str(membership_request.key())))
            
    return pending_membership_requests

def get_total_points(football_pool):
    original_pool = CAFootballPool.all().filter("privacy =", True).fetch(1)[0]
    
    original_pool_first_round_matches = original_pool.first_round_matches.fetch(18)
    football_pool_first_round_matches = football_pool.first_round_matches.fetch(18)
    
    points = 0
    
    for x in range(0, 18):
        original_match_team1_goals = original_pool_first_round_matches[x].goals_team1
        original_match_team2_goals = original_pool_first_round_matches[x].goals_team2
        
        match_team1_goals = football_pool_first_round_matches[x].goals_team1
        match_team2_goals = football_pool_first_round_matches[x].goals_team2
        
        if (original_match_team1_goals == match_team1_goals) and (original_match_team2_goals == match_team2_goals):
            points += 5
        elif ((original_match_team1_goals > original_match_team2_goals) and (match_team1_goals > match_team2_goals)) or ((original_match_team1_goals < original_match_team2_goals) and (match_team1_goals < match_team2_goals)):
            points += 3
            
    original_pool_second_round_matches = original_pool.second_round_matches.fetch(8)
    football_pool_second_round_matches = football_pool.second_round_matches.fetch(8)
    
    #Quarter finals matches
    original_teams = []
    teams = []
    
    for x in range(0, 4):
        if original_pool_second_round_matches[x].teams:
            original_team1 = CATeam.get(original_pool_second_round_matches[x].teams[0]).name
            original_team2 = CATeam.get(original_pool_second_round_matches[x].teams[1]).name
            
            team1 = CATeam.get(football_pool_second_round_matches[x].teams[0]).name
            team2 = CATeam.get(football_pool_second_round_matches[x].teams[1]).name
            
            #Puntos por pegar orden en cuartos de final
            if (original_team1 == team1):
                points += 3
            
            if (original_team2 == team2):
                points += 3
            
            original_teams.append(original_team1)
            original_teams.append(original_team2)
            
            teams.append(team1)
            teams.append(team2)
            
            #Puntos por pegar partido completo
            points += add_points_for_match(original_team1, original_pool_second_round_matches[x].goals_team1, original_team2, original_pool_second_round_matches[x].goals_team2, team1, football_pool_second_round_matches[x].goals_team1, team2, football_pool_second_round_matches[x].goals_team2)
        
    #Puntos por adivinar equipo
    for team in teams:
        if team in original_teams:
            points += 3
    
    original_teams = []
    teams = []
            
    #Semi final matches
    for x in range(4, 6):
        if original_pool_second_round_matches[x].teams:
            original_team1 = CATeam.get(original_pool_second_round_matches[x].teams[0]).name
            original_team2 = CATeam.get(original_pool_second_round_matches[x].teams[1]).name
            
            team1 = CATeam.get(football_pool_second_round_matches[x].teams[0]).name
            team2 = CATeam.get(football_pool_second_round_matches[x].teams[1]).name
            
            #Puntos por pegar partido completo
            points += add_points_for_match(original_team1, original_pool_second_round_matches[x].goals_team1, original_team2, original_pool_second_round_matches[x].goals_team2, team1, football_pool_second_round_matches[x].goals_team1, team2, football_pool_second_round_matches[x].goals_team2)
            
            original_teams.append(original_team1)
            original_teams.append(original_team2)
            
            teams.append(team1)
            teams.append(team2)
        
    #Puntos por adivinar equipo
    for team in teams:
        if team in original_teams:
            points += 3
    
    original_teams = []
    teams = []
            
    #Third-fourth match
    if original_pool_second_round_matches[6].teams:
        original_team1 = CATeam.get(original_pool_second_round_matches[6].teams[0]).name
        original_team2 = CATeam.get(original_pool_second_round_matches[6].teams[1]).name
            
        team1 = CATeam.get(football_pool_second_round_matches[6].teams[0]).name
        team2 = CATeam.get(football_pool_second_round_matches[6].teams[1]).name
        
        original_teams.append(original_team1)
        original_teams.append(original_team2)
            
        teams.append(team1)
        teams.append(team2)
        
        #Puntos por pegar partido completo
        points += add_points_for_match(original_team1, original_pool_second_round_matches[6].goals_team1, original_team2, original_pool_second_round_matches[6].goals_team2, team1, football_pool_second_round_matches[6].goals_team1, team2, football_pool_second_round_matches[6].goals_team2)
    
    #Puntos por adivinar equipo
    for team in teams:
        if team in original_teams:
            points += 3    
    
    original_teams = []
    teams = []
    
    #Final
    if original_pool_second_round_matches[7].teams:
        original_team1 = CATeam.get(original_pool_second_round_matches[7].teams[0]).name
        original_team2 = CATeam.get(original_pool_second_round_matches[7].teams[1]).name
            
        team1 = CATeam.get(football_pool_second_round_matches[7].teams[0]).name
        team2 = CATeam.get(football_pool_second_round_matches[7].teams[1]).name
        
        original_teams.append(original_team1)
        original_teams.append(original_team2)
            
        teams.append(team1)
        teams.append(team2)
        
        #Puntos por pegar partido completo
        points += add_points_for_match(original_team1, original_pool_second_round_matches[7].goals_team1, original_team2, original_pool_second_round_matches[7].goals_team2, team1, football_pool_second_round_matches[7].goals_team1, team2, football_pool_second_round_matches[7].goals_team2)
    
    #Puntos por adivinar equipo
    for team in teams:
        if team in original_teams:
            points += 3
    
    return points
            
#Puntos por pegar partido completo    
def add_points_for_match(original_team1, original_team1_goals, original_team2, original_team2_goals, team1, team1_goals, team2, team2_goals):
    points = 0
        
    if (original_team1 == team1 and original_team2 == team2):
        original_match_team1_goals = original_team1_goals
        original_match_team2_goals = original_team2_goals
        
        match_team1_goals = team1_goals
        match_team2_goals = team2_goals
        
        if (original_match_team2_goals == match_team2_goals):
            points += 5
        elif ((original_match_team1_goals > original_match_team2_goals) and (match_team1_goals > match_team2_goals)) or ((original_match_team1_goals < original_match_team2_goals) and (match_team1_goals < match_team2_goals)):
            points += 3
    elif (original_team1 == team2 and original_team2 == team1):
        original_match_team1_goals = original_team1_goals
        original_match_team2_goals = original_team2_goals
        
        match_team1_goals = team2_goals
        match_team2_goals = team1_goals
        
        if (original_match_team1_goals == match_team1_goals) and (original_match_team2_goals == match_team2_goals):
            points += 5
        elif ((original_match_team1_goals > original_match_team2_goals) and (match_team1_goals > match_team2_goals)) or ((original_match_team1_goals < original_match_team2_goals) and (match_team1_goals < match_team2_goals)):
            points += 3

    return points

def get_top_scorers():
    return CAScorer.all().order('goals').fetch(5)

def get_top_users_global_ranking():
    counter = 0
    position_points = []
    
    football_pools = CAFootballPool.all().filter("privacy =", False).fetch(10000)
    
    for football_pool in football_pools:
        position_points.append((counter, get_total_points(football_pool)))
        counter += 1
    
    football_pools_sorted_by_total_points = sorted(position_points, key=lambda position_point: position_point[1])
    
    top_football_pools_sorted_by_total_points = football_pools_sorted_by_total_points[:5]
    
    top_users = []
    counter = 0
    
    for position_point in top_football_pools_sorted_by_total_points:
        football_pool = football_pools[position_point[0]] 
        user = football_pool.user
        
        if user.type == 0:
            username = user.google_user.nickname
        elif user.type == 1:
            username = user.facebook_user.name
        else:
            username = user.native_user.name
        
        if counter % 2 == 1:
            row = "odd"
        else:
            row = "pair"
        
        top_users.append((username, football_pool.name, position_point[1], row))
        
    return top_users

def get_upcomming_matches():
    football_pool = CAFootballPool.all().filter("privacy =", True).fetch(1)[0]
    
    return CAMatch.all().filter("football_pool =", football_pool).filter("date >=", datetime.datetime.now()).order("date").fetch(3)

def get_last_jackpot():
    jackpot = CAJackPot.all().fetch(1)[0]
    
    return jackpot