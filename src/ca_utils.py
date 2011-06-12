import datetime
import os.path

from google.appengine.ext.webapp import template

from gaesessions import get_current_session

from models.ca_models import CATeam, CACompetitonGroup, CAGroupRanking

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
    
def get_team_whole_name(team_initials):
    teams = CATeam.all().fetch(12)
    
    for team in teams:
        if team.name[:3] == team_initials:
            return team.name