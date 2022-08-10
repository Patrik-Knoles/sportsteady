from  datetime import datetime
from sportsteady_pkg import db


class Admin(db.Model):
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    first_name =db.Column(db.String(50), nullable=False)
    last_name =db.Column(db.String(50), nullable=False)
    username =db.Column(db.String(50), nullable=False)
    email_address = db.Column(db.String(255),nullable=False)
    admin_pwd =db.Column(db.String(30), nullable=False)

class Journalist(db.Model):
    id =  db.Column(db.Integer(), primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255),nullable=False)
    last_name = db.Column(db.String(255),nullable=False)
    email_address = db.Column(db.String(255),nullable=False)
    password = db.Column(db.String(10),nullable=False)
    residential_address = db.Column(db.String(255),nullable=False)
    contact_number = db.Column(db.Float(),nullable=False)
    date_registered = db.Column(db.DateTime(),nullable=False, default=datetime.utcnow())

class User(db.Model):
    id =  db.Column(db.Integer(), primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255),nullable=False)
    last_name = db.Column(db.String(255),nullable=False)
    email_address = db.Column(db.String(255),nullable=False)
    password = db.Column(db.String(10),nullable=False)
    contact_number = db.Column(db.Float(),nullable=False)
    date_registered = db.Column(db.DateTime(),nullable=False, default=datetime.utcnow())

class Categories(db.Model):
    cat_id =  db.Column(db.Integer(), primary_key=True, autoincrement=True)
    cat_name = db.Column(db.String(255),nullable=False)

class Fixtures(db.Model):
    fixtures_id =  db.Column(db.Integer(), primary_key=True, autoincrement=True)
    fixtures_date = db.Column(db.DateTime(),nullable=False, default=datetime.utcnow())
    fixtures_week = db.Column(db.Float(), nullable=False)
    home_team = db.Column(db.Integer(), db.ForeignKey('teams.team_id'))
    away_team =db.Column(db.Integer(), db.ForeignKey('teams.team_id'))
    subcat_id =db.Column(db.Integer(), db.ForeignKey('sub_categories.sub_id'))
    fixture_time = db.Column(db.DateTime(),nullable=False, default=datetime.utcnow())
    livestream = db.Column(db.String(255),nullable=False)


    #Relationship Starts
    teamhome_details = db.relationship("Teams", backref="dhometeam",foreign_keys=[home_team])
    teamhaway_details = db.relationship("Teams", backref="dawayteam",foreign_keys=[away_team])
    subcat_details = db.relationship("Sub_categories", backref="dsub_category")
    #Relationship Ends

class News(db.Model):
    news_id =  db.Column(db.Integer(), primary_key=True, autoincrement=True)
    news_title =  db.Column(db.String(255),nullable=False)
    news_content =  db.Column(db.String(255),nullable=False)
    news_image = db.Column(db.String(),nullable=True)
    journalist_id =db.Column(db.Integer(), db.ForeignKey('journalist.id'))
    cat_id =db.Column(db.Integer(), db.ForeignKey('categories.cat_id'))
    subcat_id =db.Column(db.Integer(), db.ForeignKey('sub_categories.sub_id'))
    date_published = db.Column(db.DateTime(),nullable=False, default=datetime.utcnow())


    #Relationship Starts
    journalist_details = db.relationship("Journalist", backref="djournalist")
    cat_details = db.relationship("Categories", backref="news_category")
    subcat_details = db.relationship("Sub_categories", backref="news_sub_category")
    #Relationship Ends

class Results(db.Model):
    results_id =  db.Column(db.Integer(), primary_key=True, autoincrement=True)
    results_date = db.Column(db.DateTime(),nullable=False, default=datetime.utcnow())
    results_week = db.Column(db.Float(),nullable=False)
    home_team = db.Column(db.Integer(), db.ForeignKey('teams.team_id'))
    scoreboard =  db.Column(db.String(255),nullable=False)
    away_team =db.Column(db.Integer(), db.ForeignKey('teams.team_id'))
    subcat_id =db.Column(db.Integer(), db.ForeignKey('sub_categories.sub_id'))



    #Relationship Starts
    teamhome_details = db.relationship("Teams", backref="hometeam",foreign_keys=[home_team])
    teamhaway_details = db.relationship("Teams", backref="awayteam",foreign_keys=[away_team])
    subcat_details = db.relationship("Sub_categories", backref="result_sub_category")
    #Relationship Ends
    

class Season(db.Model):
    season_id =  db.Column(db.Integer(), primary_key=True, autoincrement=True)
    season_tag = db.Column(db.Float(),nullable=False)

class Sub_categories(db.Model):
    sub_id =  db.Column(db.Integer(), primary_key=True, autoincrement=True)
    cat_id =db.Column(db.Integer(), db.ForeignKey('categories.cat_id'))
    sub_name = db.Column(db.String(255),nullable=False)
    season_id = db.Column(db.Integer(), db.ForeignKey('season.season_id'))


    #Relationship Starts
    cat_details = db.relationship("Categories", backref="subcat_category")
    season_details = db.relationship("Season", backref="subcat_season")
    #Relationship Ends

class Teams(db.Model):
    team_id =  db.Column(db.Integer(), primary_key=True, autoincrement=True)
    team_name = db.Column(db.String(255),nullable=False)
    cat_id =db.Column(db.Integer(), db.ForeignKey('categories.cat_id'))
    subcat_id =db.Column(db.Integer(), db.ForeignKey('sub_categories.sub_id'))

    #Relationship Starts
    cat_details = db.relationship("Categories", backref="teams_category")
    subcat_details = db.relationship("Sub_categories", backref="teams_sub_category")
    #Relationship Ends

#Setting Foreign Key  Constraints


    #Set up the relationship
    