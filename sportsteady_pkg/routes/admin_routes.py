from flask import Flask, render_template, make_response, request, redirect, flash, session
from sqlalchemy import values
from sportsteady_pkg import  app, db, csrf
from sportsteady_pkg.forms import *
from sportsteady_pkg.models import *
from werkzeug.security import generate_password_hash, check_password_hash



@app.route("/admin/")
def admin():
    return render_template("admin/login.html")

@app.route("/admin/login/",methods=["POST","GET"])
def admin_login():
    if request.method == "GET":
        return redirect("/admin/")
    else:
        email = request.form["email"]
        password = request.form["pwd"]

        admin = Admin.query.filter(Admin.email_address==email,Admin.admin_pwd==password).first()

        if admin:
            admin_id = admin.id
            admin_username = admin.username
            session["admin_id"] = admin_id
            session["admin_username"] = admin_username
            return redirect("/admin/dashboard/")
        else:
            flash("Invalid Credentials")
            return redirect("/admin/")

@app.route("/admin/dashboard/")
def admin_profile():
    loggedin = session.get("admin_id")
    if loggedin != None:
        admin = Admin.query.filter(Admin.id==loggedin).first()
        users = db.session.query(User).count()
        journalists = db.session.query(Journalist).count()
        user = db.session.query(User).order_by(User.id.desc()).first()
        journalist = db.session.query(Journalist).order_by(Journalist.id.desc()).first()
        news = db.session.query(News).count()
        new = db.session.query(News).order_by(News.news_id.desc()).first()
        news_flash = db.session.query(News).order_by(News.news_id.desc()).offset(1).limit(5)
        return render_template("admin/dashboard.html",admin=admin, users=users, journalists=journalists,user=user,journalist=journalist,news=news,new=new,news_flash=news_flash)
    else:
        flash("You must be logged in  to view this page")
        return redirect("/admin/login/")

@app.route("/manage/journalists/")
def manage_journalists():
    loggedin = session.get("admin_id")
    if  loggedin != None:
        admin = Admin.query.filter(Admin.id==loggedin).first()
        journalists = db.session.query(Journalist).all()
        return render_template("admin/manage_journalists.html",admin=admin, journalists=journalists)
    else:
        return redirect("/admin/")

@app.route("/manage/users/")
def manage_users():
    loggedin = session.get("admin_id")
    if  loggedin != None:
        admin = Admin.query.filter(Admin.id==loggedin).first()
        users = db.session.query(User).all()
        return render_template("admin/manage_users.html",admin=admin, users=users)
    else:
        return redirect("/admin/")

@app.route("/manage/news/")
def manage_news():
    loggedin = session.get("admin_id")
    if  loggedin != None:
        admin = Admin.query.filter(Admin.id==loggedin).first()
        news = db.session.query(News).all()
        return render_template("admin/manage_news.html",admin=admin, news=news)
    else:
        return redirect("/admin/")

@app.route("/manage/teams/")
def manage_teams():
    loggedin = session.get("admin_id")
    if  loggedin != None:
        admin = Admin.query.filter(Admin.id==loggedin).first()
        epl = Teams.query.filter(Teams.subcat_id==1).all()
        la_liga = Teams.query.filter(Teams.subcat_id==2).all()
        serie_a = Teams.query.filter(Teams.subcat_id==3).all()
        ligue_1 = Teams.query.filter(Teams.subcat_id==4).all()
        return render_template("admin/manage_teams.html",admin=admin, epl=epl, la_liga=la_liga, serie_a=serie_a, ligue_1=ligue_1)
    else:
        return redirect("/admin/")

@app.route("/admin/fixtures/")
def manage_fixtures():
    loggedin = session.get("admin_id")
    if  loggedin != None:
        admin = Admin.query.filter(Admin.id==loggedin).first()
        league = db.session.query(Sub_categories).all()
    
        epl = Fixtures.query.filter(Fixtures.subcat_id==1).all()
        la_liga = Fixtures.query.filter(Fixtures.subcat_id==2).all()
        serie_a = Fixtures.query.filter(Fixtures.subcat_id==3).all()
        ligue_1 = Fixtures.query.filter(Fixtures.subcat_id==4).all()
       
        return render_template("/admin/manage_fixtures.html", admin=admin, league=league, epl=epl, la_liga=la_liga, ligue_1=ligue_1, serie_a=serie_a)
    else:
        return redirect("/admin/")
    
@app.route("/admin/manage/fixtures/", methods=["POST"])
def submit_fixtures():
    loggedin = session.get("admin_id")
    if  loggedin != None:
        admin = Admin.query.filter(Admin.id==loggedin).first()
        week = request.form["week"]
        home_team = request.form["home_team"]
        away_team = request.form["away_team"]
        league = request.form.getlist("league")
        date = request.form["date"]
        time = request.form["time"]
        livestream = request.form["livestream"]

        for i in league:
            subcat = Fixtures()
            subcat.subcat_id = i
            db.session.add(subcat)
            subcat.fixtures_week = week
            subcat.home_team = home_team
            subcat.away_team = away_team
            subcat.fixtures_date = date
            subcat.fixture_time = time
            subcat.livestream = livestream
            db.session.commit()

        flash("Fixtures Added Successfully!")
        return redirect("/admin/fixtures/")
    else:
        return redirect("/admin/")


@app.route("/edit/fixture/<id>/")
def edit_fixture(id):
    loggedin = session.get("admin_id")
    if  loggedin != None:
        admin = Admin.query.filter(Admin.id==loggedin).first()
        fixture_id = db.session.query(Fixtures).get(id)
        league = db.session.query(Sub_categories).all()
        return render_template("admin/edit_fixture.html",admin=admin,fixture_id=fixture_id,league=league)
    else:
        return redirect("/admin/")


@app.route("/update/fixture/", methods=["POST"])
def update_fixture():
    loggedin = session.get("admin_id")
    if  loggedin != None:
        admin = Admin.query.filter(Admin.id==loggedin).first()
        fixture_id = request.form["fixture_id"]
        week = request.form["week"]
        home_team = request.form["home_team"]
        away_team = request.form["away_team"]
        league = request.form.getlist("league")
        date = request.form["date"]
        time = request.form["time"]
        livestream = request.form["livestream"]

        for i in league:
            fixtures = db.session.query(Fixtures).get(fixture_id)
            fixtures.subcat_id = i
            db.session.add(fixtures)
            fixtures.fixtures_id = fixture_id
            fixtures.fixtures_week = week
            fixtures.home_team = home_team
            fixtures.away_team = away_team
            fixtures.fixtures_date = date
            fixtures.fixture_time = time
            fixtures.livestream = livestream
            db.session.commit()

        flash("Fixtures Changed Successfully!")
        return redirect("/admin/fixtures/")
    else:
        return redirect("/admin/")

@app.route("/delete/fixture/<id>/")
def delete_fixture(id):
    loggedin = session.get("admin_id")
    if  loggedin != None:
        admin = Admin.query.filter(Admin.id==loggedin).first()
        fixture_id = db.session.query(Fixtures).get(id)
        db.session.delete(fixture_id)
        db.session.commit()
        flash("Fixture Deleted!")
        return redirect("/admin/fixtures/")
    else:
        return redirect("/admin/")


# Results Starts
@app.route("/admin/results/")
def manage_results():
    loggedin = session.get("admin_id")
    if  loggedin != None:
        admin = Admin.query.filter(Admin.id==loggedin).first()
        league = db.session.query(Sub_categories).all()
    
        epl = Results.query.filter(Results.subcat_id==1).all()
        la_liga = Results.query.filter(Results.subcat_id==2).all()
        serie_a = Results.query.filter(Results.subcat_id==3).all()
        ligue_1 = Results.query.filter(Results.subcat_id==4).all()
       
        return render_template("/admin/manage_results.html", admin=admin, league=league, epl=epl, la_liga=la_liga, ligue_1=ligue_1, serie_a=serie_a)
    else:
        return redirect("/admin/")
    
@app.route("/admin/manage/results/", methods=["POST"])
def submit_results():
    loggedin = session.get("admin_id")
    if  loggedin != None:
        admin = Admin.query.filter(Admin.id==loggedin).first()
        game_week = request.form["week"]
        home_team = request.form["home_team"]
        scoreboard = request.form["scoreboard"]
        away_team = request.form["away_team"]
        league = request.form.getlist("league")
        date = request.form["date"]

        for i in league:
            subcat = Results()
            subcat.subcat_id = i
            db.session.add(subcat)
            subcat.results_week = game_week
            subcat.home_team = home_team
            subcat.scoreboard = scoreboard
            subcat.away_team = away_team
            subcat.results_date = date
            db.session.commit()

        flash("Fixtures Added Successfully!")
        return redirect("/admin/results/")
    else:
        return redirect("/admin/")


@app.route("/edit/results/<id>/")
def edit_results(id):
    loggedin = session.get("admin_id")
    if  loggedin != None:
        admin = Admin.query.filter(Admin.id==loggedin).first()
        results_id = db.session.query(Results).get(id)
        league = db.session.query(Sub_categories).all()
        return render_template("admin/edit_result.html",admin=admin,results_id=results_id,league=league)
    else:
        return redirect("/admin/")


@app.route("/update/results/", methods=["POST"])
def update_results():
    loggedin = session.get("admin_id")
    if  loggedin != None:
        admin = Admin.query.filter(Admin.id==loggedin).first()
        results_id = request.form["results_id"]
        week = request.form["week"]
        home_team = request.form["home_team"]
        scoreboard = request.form["scoreboard"]
        away_team = request.form["away_team"]
        league = request.form.getlist("league")
        date = request.form["date"]

        for i in league:
            results = db.session.query(Results).get(results_id)
            results.subcat_id = i
            db.session.add(results)
            results.results_id = results_id
            results.results_week = week
            results.results_team = home_team
            results.scoreboard = scoreboard
            results.away_team = away_team
            results.results_date = date
            db.session.commit()

        flash("Results Updated!")
        return redirect("/admin/results/")
    else:
        return redirect("/admin/")

@app.route("/delete/results/<id>/")
def delete_result(id):
    loggedin = session.get("admin_id")
    if  loggedin != None:
        admin = Admin.query.filter(Admin.id==loggedin).first()
        fixture_id = db.session.query(Results).get(id)
        db.session.delete(fixture_id)
        db.session.commit()
        flash("Results Deleted!")
        return redirect("/admin/results/")
    else:
        return redirect("/admin/")
# Results Ends

@app.route("/admin/remove/user/<id>/")
def delete_user(id):
    loggedin = session.get("admin_id")
    if  loggedin != None:
        admin = Admin.query.filter(Admin.id==loggedin).first()
        user_id = db.session.query(User).get(id)
        db.session.delete(user_id)
        db.session.commit()
        flash("User Removed!")
        return redirect("/manage/users/")
    else:
        return redirect("/admin/")

@app.route("/admin/remove/journalist/<id>/")
def delete_journalist(id):
    loggedin = session.get("admin_id")
    if  loggedin != None:
        admin = Admin.query.filter(Admin.id==loggedin).first()
        journalist_id = db.session.query(Journalist).get(id)
        db.session.delete(journalist_id)
        db.session.commit()
        flash("Journalist Removed!")
        return redirect("/manage/journalists/")
    else:
        return redirect("/admin/")

@app.route("/admin/delete/news/<id>/")
def delete_news(id):
    loggedin = session.get("admin_id")
    if  loggedin != None:
        admin = Admin.query.filter(Admin.id==loggedin).first()
        news_id = db.session.query(News).get(id)
        db.session.delete(news_id)
        db.session.commit()
        flash("News Deleted!")
        return redirect("/manage/news/")
    else:
        return redirect("/admin/")

@app.route("/admin/delete/team/<id>/")
def delete_team(id):
    loggedin = session.get("admin_id")
    if  loggedin != None:
        admin = Admin.query.filter(Admin.id==loggedin).first()
        team_id = db.session.query(Teams).get(id)
        db.session.delete(team_id)
        db.session.commit()
        flash("Team Deleted!")
        return redirect("/manage/teams/")
    else:
        return redirect("/admin/")

@app.route("/admin/edit/team/<id>/")
def edit_team(id):
    loggedin = session.get("admin_id")
    if  loggedin != None:
        admin = Admin.query.filter(Admin.id==loggedin).first()
        team_id = db.session.query(Teams).get(id)
        return render_template("admin/edit_teams.html",team_id=team_id)
    else:
        return redirect("/admin/")

@app.route("/admin/update/team/",methods=["POST"])
def update_team():
    loggedin = session.get("admin_id")
    if  loggedin != None:
        admin = Admin.query.filter(Admin.id==loggedin).first()
        new_team = request.form["team"]
        team_id = request.form["team_id"]
        team = db.session.query(Teams).get(team_id)
        team.team_name = new_team
        db.session.commit()
        return redirect("/manage/teams/")
    else:
        return redirect("/admin/")

@app.route("/admin/logout/")
def admin_logout():
    session.pop("admin_id")
    session.pop("admin_username")
    return redirect("/home/")