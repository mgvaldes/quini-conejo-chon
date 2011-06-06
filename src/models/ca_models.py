from google.appengine.ext import db

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
    type = db.IntegerProperty()

class CAFootballPool(db.Model):
    user = db.ReferenceProperty(CAUser, collection_name='football_pools')
    name = db.StringProperty(required=True)
    privacy = db.BooleanProperty(required=True)

class CAMatch(db.Model):
    date = db.DateTimeProperty()
    goals_team1 = db.IntegerProperty()
    goals_team2 = db.IntegerProperty()
    teams = db.ListProperty(db.Key)
    football_pool = db.ReferenceProperty(CAFootballPool, collection_name='matches')

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

class CATeam(db.Model):
    name = db.StringProperty()
    flag = db.LinkProperty()
    info = db.LinkProperty()
    classification_info = db.ReferenceProperty(CAClassificationInfo)
    group = db.ReferenceProperty(CAGroup, collection_name='teams')

    @property
    def matches(self):
        return CAMatch.gql('WHERE teams = :1', self.key())
