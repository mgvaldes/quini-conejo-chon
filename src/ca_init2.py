#sys.path.append(os.path.join(os.path.dirname(__file__), "models"))
from models.ca_models import *
import datetime
from google.appengine.api.mail import EmailMessage
from google.appengine.api import mail

def add_match(key1, key2, month, day, hours, minutes, copa_america):
    match_teams = []
    match_teams.append(key1)
    match_teams.append(key2)

    match_date = datetime.datetime(2011, month, day, hours, minutes, 0)

    match = CAMatch(teams=match_teams, football_pool=copa_america, date=match_date, goals_team1=-1, goals_team2=-1)
    match.put()

def add_empty_team_match(month, day, hours, minutes, copa_america):
    match_teams = []
    match_date = datetime.datetime(2011, month, day, hours, minutes, 0)

    match = CAMatch(teams=match_teams, football_pool=copa_america, date=match_date, goals_team1=-1, goals_team2=-1)
    match.put()

def create_initial_info():
    group_a = CAGroup(name='A')
    group_a.put()
    
    group_b = CAGroup(name='B')
    group_b.put()
    
    group_c = CAGroup(name='C')
    group_c.put()
        
    classification_info_argentina = CAClassificationInfo()
    classification_info_argentina.put()
    argentina = CATeam(name='Argentina', info='http://www.ca2011.com/selecoes_resumo.php?idS=eccbc87e4b5ce2fe28308fd9f2a7baf3', group=group_a, classification_info=classification_info_argentina)
    argentina.put()
    
    classification_info_bolivia = CAClassificationInfo()
    classification_info_bolivia.put()
    bolivia = CATeam(name='Bolivia', info='http://www.ca2011.com/selecoes_resumo.php?idS=a87ff679a2f3e71d9181a67b7542122c', group=group_a, classification_info=classification_info_bolivia)
    bolivia.put()
    
    classification_info_colombia = CAClassificationInfo()
    classification_info_colombia.put()
    colombia = CATeam(name='Colombia', info='http://www.ca2011.com/selecoes_resumo.php?idS=1679091c5a880faf6fb5e6087eb1b2dc', group=group_a, classification_info=classification_info_colombia)
    colombia.put()
    
    classification_info_costa_rica = CAClassificationInfo()
    classification_info_costa_rica.put()
    costa_rica = CATeam(name='Costa Rica', info='http://www.ca2011.com/selecoes_resumo.php?idS=9bf31c7ff062936a96d3c8bd1f8f2ff3', group=group_a, classification_info=classification_info_costa_rica)
    costa_rica.put()

    classification_info_brazil = CAClassificationInfo()
    classification_info_brazil.put()
    brazil = CATeam(name='Brasil', info='http://www.ca2011.com/selecoes_resumo.php?idS=c4ca4238a0b923820dcc509a6f75849b', group=group_b, classification_info=classification_info_brazil)
    brazil.put()
    
    classification_info_paraguay = CAClassificationInfo()
    classification_info_paraguay.put()
    paraguay = CATeam(name='Paraguay', info='http://www.ca2011.com/selecoes_resumo.php?idS=d3d9446802a44259755d38e6d163e820', group=group_b, classification_info=classification_info_paraguay)
    paraguay.put()
    
    classification_info_venezuela = CAClassificationInfo()
    classification_info_venezuela.put()
    venezuela = CATeam(name='Venezuela', info='http://www.ca2011.com/selecoes_resumo.php?idS=c51ce410c124a10e0db5e4b97fc2af39', group=group_b, classification_info=classification_info_venezuela)
    venezuela.put()
    
    classification_info_ecuador = CAClassificationInfo()
    classification_info_ecuador.put()
    ecuador = CATeam(name='Ecuador', info='http://www.ca2011.com/selecoes_resumo.php?idS=8f14e45fceea167a5a36dedd4bea2543', group=group_b, classification_info=classification_info_ecuador)
    ecuador.put()
    
    classification_info_chile = CAClassificationInfo()
    classification_info_chile.put()
    chile = CATeam(name='Chile', info='http://www.ca2011.com/selecoes_resumo.php?idS=e4da3b7fbbce2345d7772b0674a318d5', group=group_c, classification_info=classification_info_chile)
    chile.put()
    
    classification_info_mexico = CAClassificationInfo()
    classification_info_mexico.put()
    mexico = CATeam(name='Mexico', info='http://www.ca2011.com/selecoes_resumo.php?idS=45c48cce2e2d7fbdea1afc51c7c6ad26', group=group_c, classification_info=classification_info_mexico)
    mexico.put()
    
    classification_info_peru = CAClassificationInfo()
    classification_info_peru.put()
    peru = CATeam(name='Peru', info='http://www.ca2011.com/selecoes_resumo.php?idS=6512bd43d9caa6e02c990b0a82652dca', group=group_c, classification_info=classification_info_peru)
    peru.put()
    
    classification_info_uruguay = CAClassificationInfo()
    classification_info_uruguay.put()
    uruguay = CATeam(name='Uruguay', info='http://www.ca2011.com/selecoes_resumo.php?idS=c20ad4d76fe97759aa27a0c99bff6710', group=group_c, classification_info=classification_info_uruguay)
    uruguay.put()
    
    admin = CANativeUser(name='Admin', email='mgvaldesgraterol@gmail.com', password='admin')
    admin.put()
    
    copa_america_competition_group = CACompetitonGroup(name='Ranking Global', privacy=True)
    copa_america_competition_group.put()
    
    ca_admin = CAUser(native_user=admin, type=2)
    ca_admin.put()
    
    copa_america = CAFootballPool(user=ca_admin, name='Copa America 2011', privacy=True)
    copa_america.put()
    
    add_match(argentina.key(), bolivia.key(), 6, 30, 20, 15, copa_america)
    add_match(colombia.key(), costa_rica.key(), 7, 2, 14, 0, copa_america)
    add_match(argentina.key(), colombia.key(), 7, 5, 20, 15, copa_america)
    add_match(bolivia.key(), costa_rica.key(), 7, 7, 17, 45, copa_america)
    add_match(colombia.key(), bolivia.key(), 7, 10, 14, 30, copa_america)
    add_match(argentina.key(), costa_rica.key(), 7, 10, 20, 15, copa_america)
    
    add_match(brazil.key(), venezuela.key(), 7, 3, 14, 30, copa_america)
    add_match(paraguay.key(), ecuador.key(), 7, 3, 17, 0, copa_america)
    add_match(brazil.key(), paraguay.key(), 7, 9, 14, 30, copa_america)
    add_match(venezuela.key(), ecuador.key(), 7, 9, 17, 0, copa_america)
    add_match(paraguay.key(), venezuela.key(), 7, 13, 17, 45, copa_america)
    add_match(brazil.key(), ecuador.key(), 7, 12, 20, 45, copa_america)
    
    add_match(uruguay.key(), peru.key(), 7, 4, 17, 45, copa_america)
    add_match(chile.key(), mexico.key(), 7, 3, 20, 15, copa_america)
    add_match(peru.key(), mexico.key(), 7, 8, 17, 45, copa_america)
    add_match(uruguay.key(), chile.key(), 7, 7, 20, 15, copa_america)
    add_match(chile.key(), peru.key(), 7, 12, 17, 45, copa_america)
    add_match(uruguay.key(), mexico.key(), 7, 11, 20, 15, copa_america)

    add_empty_team_match(7, 16, 14, 30, copa_america)
    add_empty_team_match(7, 16, 17, 45, copa_america)
    add_empty_team_match(7, 17, 14, 30, copa_america)
    add_empty_team_match(7, 17, 17, 45, copa_america)
    add_empty_team_match(7, 18, 20, 15, copa_america)
    add_empty_team_match(7, 19, 20, 15, copa_america)
    add_empty_team_match(7, 23, 14, 30, copa_america)
    add_empty_team_match(7, 24, 14, 30, copa_america)
    
    jackpot = CAJackPot(amount=4000, last_update=datetime.datetime.now())
    jackpot.put()

    scorer1 = CAScorer(name="Miku Fedor", team=venezuela, goals=0)
    scorer1.put()
    
    scorer2 = CAScorer(name="Nilmar", team=brazil, goals=0)
    scorer2.put()
    
    scorer3 = CAScorer(name="Lionel Messi", team=argentina, goals=0)
    scorer3.put()
    
    scorer4 = CAScorer(name="Diego Forl&aacute;n", team=uruguay, goals=0)
    scorer4.put()
    
    scorer5 = CAScorer(name="Carlos T&eacute;vez", team=argentina, goals=0)
    scorer5.put()
    
def send_reminder_email():
    users = CAUser.all().fetch(10000)
    
    for user in users:
        if user.type == 0:
            email = user.google_user.email()
        elif user.type == 2:
            email = user.native_user.email
            
    
        mail = EmailMessage(sender="info@quinielaca.com", to=email, subject="Recordatorio de Quinielaca.com", html="<html><body><img src=\"http://img84.imageshack.us/img84/210/emailxy.png\"/></body></html>")
        mail.send()

def update_dates():
#    #Argentiina-Bolivia
#    matches1 = CAMatch.all().filter("date =", datetime.datetime(2011, 6, 30, 20, 15, 0)).fetch(10000)
#    
#    for match1 in matches1:
#        match1.date = datetime.datetime(2011, 7, 1, 20, 15, 0)
#        match1.put()
#    
#    #Argentiina-Colombia
#    matches2 = CAMatch.all().filter("date =", datetime.datetime(2011, 7, 5, 20, 15, 0)).fetch(10000)
#    
#    for match2 in matches2:
#        match2.date = datetime.datetime(2011, 7, 6, 20, 15, 0)
#        match2.put()
#    
#    #Uruguay-Mexico
#    matches8 = CAMatch.all().filter("date =", datetime.datetime(2011, 7, 11, 20, 15, 0)).fetch(10000)
#    
#    for match8 in matches8:
#        match8.date = datetime.datetime(2011, 7, 12, 20, 15, 0)
#        match8.put()
#    
#    #Argentiina-CostaRica    
#    matches3 = CAMatch.all().filter("date =", datetime.datetime(2011, 7, 10, 20, 15, 0)).fetch(10000)
#    
#    for match3 in matches3:
#        match3.date = datetime.datetime(2011, 7, 11, 20, 15, 0)
#        match3.put()
#        
#    #Brasil-Ecuador
#    matches4 = CAMatch.all().filter("date =", datetime.datetime(2011, 7, 12, 20, 45, 0)).fetch(10000)
#    
#    for match4 in matches4:
#        match4.date = datetime.datetime(2011, 7, 13, 20, 15, 0)
#        match4.put()
        
    #Chile-Mexico
    matches5 = CAMatch.all().filter("date =", datetime.datetime(2011, 7, 8, 17, 45, 0)).fetch(10000)
    
    for match5 in matches5:
        teams = CATeam.get(match5.teams)
        
        if teams[0].name == "Chile" and teams[1].name == "Mexico":
            match5.date = datetime.datetime(2011, 7, 4, 20, 15, 0)
            match5.put()
        
#    #Peru-Mexico
#    matches7 = CAMatch.all().filter("date =", datetime.datetime(2011, 7, 8, 17, 45, 0)).fetch(10000)
#    
#    for match7 in matches7:
#        match7.date = datetime.datetime(2011, 7, 8, 20, 15, 0)
#        match7.put()
    
    #Uruguay-Chile
    matches6 = CAMatch.all().filter("date =", datetime.datetime(2011, 7, 7, 20, 15, 0)).fetch(10000)
    
    for match6 in matches6:
        teams = CATeam.get(match6.teams)
        
        if teams[0].name == "Uruguay" and teams[1].name == "Chile":
            match6.date = datetime.datetime(2011, 7, 8, 17, 45, 0)
            match6.put()
    
    #Semi-Final2
    matches10 = CAMatch.all().filter("date =", datetime.datetime(2011, 7, 19, 20, 15, 0)).fetch(10000)
    
    for match10 in matches10:
        match10.date = datetime.datetime(2011, 7, 20, 20, 15, 0)
        match10.put()
    
    #Semi-Final1
    matches9 = CAMatch.all().filter("date =", datetime.datetime(2011, 7, 18, 20, 15, 0)).fetch(10000)
    
    for match9 in matches9:
        match9.date = datetime.datetime(2011, 7, 19, 20, 15, 0)
        match9.put()    
        
#create_initial_info()
