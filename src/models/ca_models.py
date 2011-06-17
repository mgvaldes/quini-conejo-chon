from google.appengine.ext import db
import datetime

class CANativeUser(db.Model):
    name = db.StringProperty()
    email = db.EmailProperty()
    password = db.StringProperty()

class CAFacebookUser(db.Model):
    id = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    access_token = db.StringProperty()

class CAUser(db.Model):
    google_user = db.UserProperty()
    facebook_user = db.ReferenceProperty(CAFacebookUser)
    native_user = db.ReferenceProperty(CANativeUser)
    type = db.IntegerProperty() #Google: type = 0, Facebook: type = 1, Native: type = 2
    groups = db.ListProperty(db.Key)
    
    @property
    def pending_membership_requests(self):
        membership_requests = CARequestGroupMembership.gql('WHERE users = :1 AND status = :2', self.key(), False).fetch(10000)
        
        pending_membership_requests = []
        
        for membership_request in membership_requests:
            if membership_request.users[1] == self.key():
                pending_membership_requests.append(membership_request)
                
        return pending_membership_requests

class CAPayment(db.Model):
    bank = db.StringProperty()
    type = db.BooleanProperty() #Transferencia = True, Deposito = False
    date = db.DateTimeProperty() 
    status = db.BooleanProperty() #Confirmada = True, Pendiente = False
    payment_number = db.StringProperty()

class CAFootballPool(db.Model):
    user = db.ReferenceProperty(CAUser, collection_name='football_pools')
    name = db.StringProperty(required=True)
    privacy = db.BooleanProperty(required=True)
    payment = db.ReferenceProperty(CAPayment)
    
    @property
    def first_round_matches(self):
        return CAMatch.gql("WHERE football_pool = :1 AND date < :2 ORDER BY date", self.key(), datetime.datetime(2011, 7, 16, 14, 30, 0))
    
    @property
    def second_round_matches(self):
        return CAMatch.gql("WHERE football_pool = :1 AND date > :2 ORDER BY date", self.key(), datetime.datetime(2011, 7, 13, 17, 45, 0))

class CAMatch(db.Model):
    date = db.DateTimeProperty()
    goals_team1 = db.IntegerProperty()
    goals_team2 = db.IntegerProperty()
    teams = db.ListProperty(db.Key)
    football_pool = db.ReferenceProperty(CAFootballPool)
    
    def __str__(self):
        real_teams = db.get(self.teams)
        
        return real_teams[0].name + '-' + real_teams[1].name + '-' + str(self.date) 
    
    def __eq__(self, other):
        if str(self) == str(other):
            return True
        else:
            return False
            
class CAClassificationInfo(db.Model):
    points = db.IntegerProperty(default=0)
    matches = db.IntegerProperty(default=0)
    wins = db.IntegerProperty(default=0)
    draws = db.IntegerProperty(default=0)
    loses = db.IntegerProperty(default=0)
    goals_scored = db.IntegerProperty(default=0)
    goals_against = db.IntegerProperty(default=0)

class CAGroup(db.Model):
    name = db.StringProperty()
    
    @property
    def matches(self):
        group_teams = self.teams
        final_matches = []
        
        for team in group_teams:
            team_matches = team.first_round_matches
            for match in team_matches:
                if match not in final_matches: 
                    final_matches.append(match)
                
        return final_matches

class CATeam(db.Model):
    name = db.StringProperty()
    flag = db.LinkProperty()
    info = db.LinkProperty()
    classification_info = db.ReferenceProperty(CAClassificationInfo)
    group = db.ReferenceProperty(CAGroup, collection_name='teams')
    
class CACompetitonGroup(db.Model):
    name = db.StringProperty()
    privacy = db.BooleanProperty()
    
    @property
    def members(self):
        return CAUser.gql("WHERE groups = :1", self.key())
    
class CAGroupRanking(db.Model):
    football_pool = db.ReferenceProperty(CAFootballPool)
    group = db.ReferenceProperty(CACompetitonGroup)
    rank = db.IntegerProperty()
    
class CARequestGroupMembership(db.Model):
    users = db.ListProperty(db.Key)
    status = db.BooleanProperty()
    group = db.ReferenceProperty(CACompetitonGroup)
    
class CAScorer(db.Model):
    name = db.StringProperty()
    team = db.ReferenceProperty(CATeam)
    goals = db.IntegerProperty
    
class CAJackPot(db.Model):
    amount = db.IntegerProperty()
    last_update = db.DateTimeProperty()
