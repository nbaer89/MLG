from peewee import *
from wtfpeewee.fields import ModelHiddenField
from wtfpeewee.orm import model_form, ModelConverter
import wtforms
from flask_wtf import FlaskForm
from wtforms import Form, FieldList, FormField, SelectField, HiddenField, validators


db = SqliteDatabase('mlg.s', check_same_thread=False, pragmas={'foreign_keys': 1})


class HiddenForeignKeyConverter(ModelConverter):
    def handle_foreign_key(self, model, field, **kwargs):
        return field.name, ModelHiddenField(model=field.rel_model, **kwargs)

class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel):
    id = AutoField(primary_key=True)
    Reddit_Name = CharField(unique=True)
    Discord_Name = CharField()
    Discord_ID = CharField()
    Roles = CharField(default='Player')

class Teams(BaseModel):
    id = AutoField(primary_key=True)
    Team_Name = CharField(unique=True)
    Team_Abbr = CharField(unique=True)
    Logo = CharField()

class Players(BaseModel):
    id = AutoField(primary_key=True)
    User_ID = ForeignKeyField(Users,backref='uid')
    Player_ID = IntegerField(unique=True)
    Player_Name = CharField()
    PPos = CharField()
    SPos = CharField(null=True)
    Hand = CharField()
    Team = ForeignKeyField(Teams,field='Team_Abbr',null=True)
    Contact = IntegerField(default=0)
    Eye  = IntegerField(default=0)
    Power = IntegerField(default=0)
    Speed = IntegerField(default=0)
    Movement = IntegerField(default=0)
    Command = IntegerField(default=0)
    Velocity = IntegerField(default=0)
    Awareness = IntegerField(default=0)

class Games(BaseModel):
    id = AutoField(primary_key=True)
    Game_Number = IntegerField(unique=True)
    Game_ID = CharField()
    Season = IntegerField(null=True)
    Session = IntegerField(null=True)
    Away = ForeignKeyField(Teams,field='Team_Abbr',null=True)
    Home = ForeignKeyField(Teams,field='Team_Abbr',null=True)
    A_Score = CharField(default=0)
    H_Score = CharField(default=0)
    A_Bat_Pos = IntegerField(default=1)
    H_Bat_Pos = IntegerField(default=1)
    Inning = CharField(null=True)
    Outs = IntegerField(default=0)
    Situation = CharField(null=True)
    First_Base = ForeignKeyField(Players,field='Player_ID',null=True)
    Second_Base = ForeignKeyField(Players,field='Player_ID',null=True)
    Third_Base = ForeignKeyField(Players,field='Player_ID',null=True)
    Pitch = IntegerField(null=True)
    Swing = IntegerField(null=True)
    C_Throw = IntegerField(null=True)
    R_Steal = IntegerField(null=True)
    Win = ForeignKeyField(Teams,field='Team_Abbr',null=True)
    Loss = ForeignKeyField(Teams,field='Team_Abbr',null=True)
    WP = ForeignKeyField(Players,field='Player_ID',null=True)
    LP = ForeignKeyField(Players,field='Player_ID',null=True)
    SV = ForeignKeyField(Players,field='Player_ID',null=True)
    POTG = ForeignKeyField(Players,field='Player_ID',null=True)
    HM1 = ForeignKeyField(Players,field='Player_ID',null=True)
    HM2 = ForeignKeyField(Players,field='Player_ID',null=True)
    HM3 = ForeignKeyField(Players,field='Player_ID',null=True)
    Umpires = CharField(null=True)
    Reddit_Thread = CharField(null=True)
    Notes = CharField(null=True)

GameCreationForm = model_form(Games)


class Lineups(BaseModel):
    id = AutoField(primary_key=True)
    Game_Number = ForeignKeyField(Games,field='Game_Number',null=True)
    Team = ForeignKeyField(Teams,field='Team_Abbr',null=True)
    Player = ForeignKeyField(Players,field='Player_ID',null=True)
    Box = IntegerField(null=True)
    Order = IntegerField(null=True)
    Position = CharField(null=True)

class BoxOrderPosForm(Form):
    box_choices = []
    for i in range(0,10): box_choices.append((i,i))
    order_choices = []
    for i in range(0,10): order_choices.append((i,i))
    pos_choices = [('-','-')]
    for i in ['P','C','1B','2B','3B','SS','LF','CF','RF','DH']: pos_choices.append((i,i))
    player_id = HiddenField()
    box = SelectField(coerce=int,choices = box_choices)
    order = SelectField(coerce=int,choices = order_choices)
    pos = SelectField(choices = pos_choices)

class LineupBoxForm(FlaskForm):
    a_bop = FieldList(FormField(BoxOrderPosForm))
    h_bop = FieldList(FormField(BoxOrderPosForm))

class All_PAs(BaseModel):
    id = AutoField(primary_key=True)
    Play_No = IntegerField()
    Inning = CharField()
    Outs = IntegerField()
    BRC = IntegerField()
    Play_Type = CharField()
    Pitcher = CharField(null=True)
    Pitch_No = IntegerField(null=True)
    Batter = CharField(null=True)
    Swing_No = IntegerField(null=True)
    Catcher = CharField(null=True)
    Throw_No = IntegerField(null=True)
    Runner = CharField(null=True)
    Steal_No = IntegerField(null=True)
    Result = CharField()
    Run_Scored = IntegerField(null=True)
    Ghost_Scored = IntegerField(null=True)
    RBIs = IntegerField(null=True)
    Stolen_Base = IntegerField(null=True)
    Diff = IntegerField()
    Runs_Scored_On_Play = IntegerField(null=True)
    Off_Team = CharField()
    Def_Team = CharField()
    Game_No = IntegerField()
    Session_No = IntegerField()
    Inning_No = IntegerField()
    Pitcher_ID = ForeignKeyField(Players,field='Player_ID',null=True)
    Batter_ID = ForeignKeyField(Players,field='Player_ID',null=True)
    Catcher_ID = ForeignKeyField(Players,field='Player_ID',null=True)
    Runner_ID = ForeignKeyField(Players,field='Player_ID',null=True)

def db_init():
    db.connect(reuse_if_open=True)
    db.drop_tables([Users,Teams,Players,All_PAs,Games,Lineups])
    db.create_tables([Users,Teams,Players,All_PAs,Games,Lineups])
    db.close()

def populate_test_data():
    test_teams = [{'Team_Name':'Lonestar Pumpjacks','Team_Abbr':'LPJ','Logo':'/home/RLB_app/RLB_app/teams/static/LPJ_Logo'},
             {'Team_Name':'Sleepy Hollow Horsemen','Team_Abbr':'SHH','Logo':'/home/RLB_app/RLB_app/teams/static/SHH_Logo'}]
    test_users = [
    {'Reddit_Name':'Jzkitty21', 'Discord_Name': 'JZKITTY#3143', 'Discord_ID': 254774534274547713, 'Roles': 'player'},
    {'Reddit_Name':'ghosthardware515', 'Discord_Name': 'sarah_#4781', 'Discord_ID': 167796704739983360, 'Roles': 'player'},
    {'Reddit_Name':'dyslexda', 'Discord_Name': 'dyslexda#0531', 'Discord_ID': 202278109708419072, 'Roles': 'player, umpire, commissioner'},
    {'Reddit_Name':'therealduke96', 'Discord_Name': 'Bigbosstone#5754', 'Discord_ID': 235564193112260608, 'Roles': 'player'},
    {'Reddit_Name':'Kyounggun', 'Discord_Name': 'Kyounggun#0717', 'Discord_ID': 273639536804757514, 'Roles': 'player'},
    {'Reddit_Name':'Am3yankees3', 'Discord_Name': 'Andrew3#2319', 'Discord_ID': 402249979651031052, 'Roles': 'player'},
    {'Reddit_Name':'steelermade28', 'Discord_Name': 'steelermade28#8041', 'Discord_ID': 198821468317024256, 'Roles': 'player'},
    {'Reddit_Name':'xbijin', 'Discord_Name': 'xbijin#3776', 'Discord_ID': 398235187634503702, 'Roles': 'player'},
    {'Reddit_Name':'Ashbymtg','Discord_Name': 'Keyo', 'Discord_ID': 114529305219956739, 'Roles': 'player'},
    {'Reddit_Name':'Druidicdwarf','Discord_Name': 'LefLop#4771', 'Discord_ID': 246762932703068162, 'Roles': 'player'}]
    test_players = [
    { 'User_ID':1, 'Player_ID':7001, 'Player_Name': 'JZ', 'PPos': 'C', 'SPos': 'CIF', 'Hand': 'R', 'Team': 'LPJ', 'Contact':2, 'Eye':4, 'Power':1, 'Speed':5, 'Movement':0, 'Command':0, 'Velocity':0, 'Awareness':0},
    { 'User_ID':2, 'Player_ID':7002, 'Player_Name': 'Sarah Buntingsworth', 'PPos': '2B', 'SPos': 'UTIL', 'Hand': 'L', 'Team': 'LPJ', 'Contact':5, 'Eye':1, 'Power':2, 'Speed':4, 'Movement':0, 'Command':0, 'Velocity':0, 'Awareness':0},
    { 'User_ID':3, 'Player_ID':7003, 'Player_Name': 'Tygen Shinybeard', 'PPos': 'CF', 'SPos': '', 'Hand': 'R', 'Team': 'LPJ', 'Contact':3, 'Eye':3, 'Power':3, 'Speed':3, 'Movement':0, 'Command':0, 'Velocity':0, 'Awareness':0},
    { 'User_ID':4, 'Player_ID':7004, 'Player_Name': 'Nate Duke', 'PPos': 'P', 'SPos': '', 'Hand': 'R', 'Team': 'LPJ', 'Contact':0, 'Eye':0, 'Power':0, 'Speed':0, 'Movement':4, 'Command':2, 'Velocity':1, 'Awareness':5},
    { 'User_ID':5, 'Player_ID':7005, 'Player_Name': 'Kalin Young', 'PPos': 'C', 'SPos': 'CIF', 'Hand': 'R', 'Team': 'SHH', 'Contact':1, 'Eye':5, 'Power':5, 'Speed':1, 'Movement':0, 'Command':0, 'Velocity':0, 'Awareness':0},
    { 'User_ID':6, 'Player_ID':7006, 'Player_Name': 'Poop McGee', 'PPos': '2B', 'SPos': 'UTIL', 'Hand': 'R', 'Team': 'SHH', 'Contact':3, 'Eye':3, 'Power':3, 'Speed':3, 'Movement':0, 'Command':0, 'Velocity':0, 'Awareness':0},
    { 'User_ID':7, 'Player_ID':7007, 'Player_Name': 'Dominus Nominus', 'PPos': 'CF', 'SPos': '', 'Hand': 'L', 'Team': 'SHH', 'Contact':2, 'Eye':4, 'Power':5, 'Speed':1, 'Movement':0, 'Command':0, 'Velocity':0, 'Awareness':0},
    { 'User_ID':8, 'Player_ID':7008, 'Player_Name': 'Spike Swordfish II', 'PPos': 'P', 'SPos': '', 'Hand': 'R', 'Team': 'SHH', 'Contact':0, 'Eye':0, 'Power':0, 'Speed':0, 'Movement':4, 'Command':2, 'Velocity':1, 'Awareness':5},
    { 'User_ID': 9, 'Player_ID': 7009, 'Player_Name': 'Rekt Kiddo', 'PPos': 'SS', 'SPos': 'UTIL', 'Hand': 'R', 'Team': 'LPJ', 'Contact': 3, 'Eye': 3, 'Power': 3, 'Speed': 3, 'Movement': 0, 'Command': 0, 'Velocity': 0, 'Awareness': 0},
    { 'User_ID': 10, 'Player_ID': 7010, 'Player_Name': 'King Kruul', 'PPos': 'SS', 'SPos': 'UTIL', 'Hand': 'R', 'Team': 'SHH', 'Contact': 3, 'Eye': 3, 'Power': 3, 'Speed': 3, 'Movement': 0, 'Command': 0, 'Velocity': 0, 'Awareness': 0}]
    test_games = [{'Game_Number':50002,'Game_ID':'SHHLPJ2','Season':5,'Session':2,'Away':'SHH','Home':'LPJ'},
                  {'Game_Number':50003,'Game_ID':'LPJSHH3','Season':5,'Session':3,'Away':'LPJ','Home':'SHH'}]


    with db.atomic():
        Teams.insert_many(test_teams).execute()
        Users.insert_many(test_users).execute()
        Players.insert_many(test_players).execute()
        Games.insert_many(test_games).execute()

