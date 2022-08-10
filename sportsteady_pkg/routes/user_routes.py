import random, os
from flask import Flask, render_template, make_response, abort, redirect, flash, session, request
from sqlalchemy import values
from sportsteady_pkg import  app, db, csrf
from sportsteady_pkg.forms import *
from sportsteady_pkg.models import *
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/home/")
def home():
    left_post = db.session.query(News).order_by(News.news_id.desc()).first()
    
        
    right_post =  db.session.query(News).order_by(News.cat_id.asc()).first()
    top_all_posts =  db.session.query(News).order_by(News.cat_id.desc()).limit(5)
    right_all_posts =  db.session.query(News).order_by(News.news_id.desc()).limit(5)
    left_all_posts =  db.session.query(News).order_by(News.news_id.desc()).limit(4)

    return render_template("/user/index.html",left_post=left_post, right_post=right_post, all_posts=top_all_posts, right_all_posts=right_all_posts, left_all_posts=left_all_posts)


@app.route("/user/signup/")
def signup():
    user_form = UserForm()
    return render_template("user/signup.html", user_form=user_form)

@app.route("/signing/",methods=["POST","GET"])
def signing_up():
    user_form = UserForm()
    if request.method == "GET":
        return redirect("/user/signup/")
    else:
        if user_form.validate_on_submit():
            firstname = request.form["firstname"]
            lastname = request.form["lastname"]
            email = request.form["email"]
            phone = request.form["phone"]
            password = request.form["password"]
            #Insert into db using the model class
            hashed = generate_password_hash(password)
            user = User(first_name=firstname, last_name=lastname, email_address=email, contact_number=phone, password=hashed)
            db.session.add(user)
            db.session.commit()
        
            user = user.id
            session["user"] = user
            return redirect("/user/home/")
        else:
            return render_template("user/signup.html",user_form=user_form)
    

@app.route("/user/login/")
def login():
    return render_template("user/login.html")

@app.route("/home/")
def home_page():
    all_posts = db.session.query(News).all()
    return render_template("user/index.html",all_posts=all_posts)
    
@app.route("/athletics/")
def athletics():
    right_all_posts =  db.session.query(News).order_by(News.news_id.asc()).limit(5)
    athletics = News.query.filter(News.cat_id==1).limit(4)
    latest = News.query.filter(News.cat_id==1).order_by(News.news_id.desc()).limit(4)
    left_all_posts =  db.session.query(News).order_by(News.news_id.desc()).limit(4)
    return render_template("user/athletics.html", right_all_posts=right_all_posts,athletics=athletics,latest=latest,left_all_posts=left_all_posts)

@app.route("/football/")
def football():
    right_all_posts =  db.session.query(News).order_by(News.news_id.asc()).offset(4).limit(5)

    football = News.query.filter(News.cat_id==2).order_by(News.cat_id.desc()).limit(4)

    latest = News.query.filter(News.cat_id==2).order_by(News.news_id.desc()).first()

    others =  News.query.filter(News.cat_id==2).order_by(News.news_id.desc()).limit(4)
    
    left_all_posts =  db.session.query(News).order_by(News.news_id.desc()).limit(4)

    epl = Fixtures.query.filter(Fixtures.subcat_id==1).order_by(Fixtures.fixtures_date.asc()).all()
    la_liga = Fixtures.query.filter(Fixtures.subcat_id==2).order_by(Fixtures.fixtures_date.asc()).all()
    serie_a = Fixtures.query.filter(Fixtures.subcat_id==3).order_by(Fixtures.fixtures_date.asc()).all()
    ligue_1 = Fixtures.query.filter(Fixtures.subcat_id==4).order_by(Fixtures.fixtures_date.asc()).all()

    return render_template("user/football.html", right_all_posts=right_all_posts,football=football,latest=latest,others=others,left_all_posts=left_all_posts, epl=epl, la_liga=la_liga, serie_a=serie_a, ligue_1=ligue_1)

@app.route("/tennis/")
def tennis():
    right_all_posts =  db.session.query(News).order_by(News.news_id.asc()).offset(9).limit(5)

    tennis = News.query.filter(News.cat_id==3).order_by(News.cat_id.desc()).limit(4)

    latest = News.query.filter(News.cat_id==3).order_by(News.news_id.desc()).first()
    others =  News.query.filter(News.cat_id==3).order_by(News.news_id.desc()).limit(4)

    left_all_posts =  db.session.query(News).order_by(News.news_id.desc()).limit(4)
    
    return render_template("user/tennis.html", right_all_posts=right_all_posts,tennis=tennis,latest=latest,others=others,left_all_posts=left_all_posts)

@app.route("/football/results/")
def f_results():
    left_all_posts =  db.session.query(News).order_by(News.news_id.desc()).limit(4)
    epl = Results.query.filter(Results.subcat_id==1).order_by(Results.results_date.asc()).all()
    la_liga = Results.query.filter(Results.subcat_id==2).order_by(Results.results_date.asc()).all()
    serie_a = Results.query.filter(Results.subcat_id==3).order_by(Results.results_date.asc()).all()
    ligue_1 = Results.query.filter(Results.subcat_id==4).order_by(Results.results_date.asc()).all()

    return render_template("/user/results.html",left_all_posts=left_all_posts, epl=epl, la_liga=la_liga, ligue_1=ligue_1, serie_a=serie_a)   

@app.route("/news/<id>/")
def news(id):
    news_id = db.session.query(News).get(id)
    right_all_posts =  db.session.query(News).order_by(News.news_id.asc()).limit(5)
    latest = News.query.filter(News.news_id).order_by(News.news_id.desc()).limit(4)
    return render_template("user/news.html",news_id=news_id, right_all_posts=right_all_posts,latest=latest)


@app.errorhandler(404)
def pagenotfound(error):
    left_all_posts =  db.session.query(News).order_by(News.news_id.desc()).limit(4)
    return render_template("/user/error404.html",error=error,left_all_posts=left_all_posts),404

@app.errorhandler(500)
def pagenotfound(error):
    left_all_posts =  db.session.query(News).order_by(News.news_id.desc()).limit(4)
    return render_template("/user/error500.html",error=error,left_all_posts=left_all_posts),500

@app.route("/user/logout/")
def logout():
    session.pop("user")
    return redirect("/home/")


#For logged in viewers:

@app.route("/logging/",methods=["GET","POST"])
def logging():
    if request.method == "GET":
        return redirect("/user/login/")
    else:
        email = request.form["email"]
        password = request.form["password"]
        #Retrieve the hashed password belonging to this user:
        user_details = User.query.filter(User.email_address==email).first()
        if user_details and check_password_hash(user_details.password,password):
            session["user"] = user_details.id
            return redirect("/user/home/")
        else:
            flash("Invalid Credentials")
            return redirect("/user/login/")


@app.route("/user/home/",methods=["POST","GET"])
def user_home():
    loggedin = session.get("user")
    if loggedin != None:
        left_post = db.session.query(News).order_by(News.news_id.desc()).first()
    
        
        right_post =  db.session.query(News).order_by(News.cat_id.asc()).first()
        top_all_posts =  db.session.query(News).order_by(News.cat_id.desc()).limit(5)
        right_all_posts =  db.session.query(News).order_by(News.news_id.desc()).offset(6).limit(5)
        left_all_posts =  db.session.query(News).order_by(News.news_id.desc()).limit(4)

        return render_template("/user2/index.html",left_post=left_post, right_post=right_post, all_posts=top_all_posts, right_all_posts=right_all_posts, left_all_posts=left_all_posts)
    else:
        flash("You must be logged in  to view this page")
        return redirect("/user/login/")

@app.route("/user/athletics/",methods=["POST","GET"])
def user_athletics():
    loggedin = session.get("user")
    if loggedin != None:
        user_deets = db.session.query(User).filter(User.id==loggedin).first()
        right_all_posts =  db.session.query(News).order_by(News.news_id.asc()).limit(5)
        athletics = News.query.filter(News.cat_id==1).order_by(News.news_id.desc()).first()
        latest = News.query.filter(News.cat_id==1).order_by(News.news_id.desc()).limit(6)
        left_all_posts =  db.session.query(News).order_by(News.news_id.desc()).limit(4)
        return render_template("user2/athletics.html",user_deets=user_deets, right_all_posts=right_all_posts,athletics=athletics,latest=latest,left_all_posts=left_all_posts)
    else:
        flash("You must be logged in  to view this page")
        return redirect("/user/login/")

@app.route("/user/football/",methods=["POST","GET"])
def user_football():
    loggedin = session.get("user")
    if loggedin != None:
        user_deets = db.session.query(User).filter(User.id==loggedin).first()
        right_all_posts =  db.session.query(News).order_by(News.news_id.asc()).offset(4).limit(5)

        football = News.query.filter(News.cat_id==2).order_by(News.news_id.desc()).offset(5).limit(4)

        latest = News.query.filter(News.cat_id==2).order_by(News.news_id.desc()).first()

        others =  News.query.filter(News.cat_id==2).order_by(News.news_id.desc()).limit(4)
        
        left_all_posts =  db.session.query(News).order_by(News.news_id.desc()).limit(4)

        epl = Fixtures.query.filter(Fixtures.subcat_id==1).order_by(Fixtures.fixtures_date.asc()).all()
        la_liga = Fixtures.query.filter(Fixtures.subcat_id==2).order_by(Fixtures.fixtures_date.asc()).all()
        serie_a = Fixtures.query.filter(Fixtures.subcat_id==3).order_by(Fixtures.fixtures_date.asc()).all()
        ligue_1 = Fixtures.query.filter(Fixtures.subcat_id==4).order_by(Fixtures.fixtures_date.asc()).all()

        return render_template("user2/football.html",user_deets=user_deets, right_all_posts=right_all_posts,football=football,latest=latest,others=others,left_all_posts=left_all_posts, epl=epl, la_liga=la_liga, serie_a=serie_a, ligue_1=ligue_1)

    else:
        flash("You must be logged in  to view this page")
        return redirect("/user/login/")

@app.route("/user/tennis/",methods=["POST","GET"])
def user_tennis():
    loggedin = session.get("user")
    if loggedin != None:
        user_deets = db.session.query(User).filter(User.id==loggedin).first()
        right_all_posts =  db.session.query(News).order_by(News.news_id.asc()).offset(9).limit(5)

        tennis = News.query.filter(News.cat_id==3).order_by(News.news_id.desc()).limit(5)

        latest = News.query.filter(News.cat_id==3).order_by(News.news_id.desc()).first()

        left_all_posts =  db.session.query(News).order_by(News.news_id.desc()).limit(4)
        
        return render_template("user2/tennis.html",user_deets=user_deets,right_all_posts=right_all_posts,tennis=tennis,latest=latest,left_all_posts=left_all_posts)
    else:
        flash("You must be logged in  to view this page")
        return redirect("/user/login/")

@app.route("/user/football/results/",methods=["POST","GET"])
def user_f_results():
    loggedin = session.get("user")
    if loggedin != None:
        user_deets = db.session.query(User).filter(User.id==loggedin).first()
        left_all_posts =  db.session.query(News).order_by(News.news_id.desc()).limit(4)
        epl = Results.query.filter(Results.subcat_id==1).order_by(Results.results_date.asc()).all()
        la_liga = Results.query.filter(Results.subcat_id==2).order_by(Results.results_date.asc()).all()
        serie_a = Results.query.filter(Results.subcat_id==3).order_by(Results.results_date.asc()).all()
        ligue_1 = Results.query.filter(Results.subcat_id==4).order_by(Results.results_date.asc()).all()

        return render_template("/user2/results.html",user_deets=user_deets, left_all_posts=left_all_posts, epl=epl, la_liga=la_liga, ligue_1=ligue_1, serie_a=serie_a)
    else:
        flash("You must be logged in  to view this page")
        return redirect("/user/login/")

@app.route("/user/redirect/")
def user_redirect():
    loggedin = session.get("user")
    if loggedin != None:
        user_deets = db.session.query(User).filter(User.id==loggedin).first()

        return render_template("/user2/redirect.html",user_deets=user_deets)
    else:
        flash("You must be logged in  to view this page")
        return redirect("/user/login/")

@app.route("/livestream/")
def user_livestream():
    loggedin = session.get("user")
    if loggedin != None:
        user_deets = db.session.query(User).filter(User.id==loggedin).first()

        epl = Fixtures.query.filter(Fixtures.subcat_id==1).order_by(Fixtures.fixtures_date.asc()).all()
        la_liga = Fixtures.query.filter(Fixtures.subcat_id==2).order_by(Fixtures.fixtures_date.asc()).all()
        serie_a = Fixtures.query.filter(Fixtures.subcat_id==3).order_by(Fixtures.fixtures_date.asc()).all()
        ligue_1 = Fixtures.query.filter(Fixtures.subcat_id==4).order_by(Fixtures.fixtures_date.asc()).all()

        return render_template("/user2/livestream.html",user_deets=user_deets, epl=epl, la_liga=la_liga, ligue_1=ligue_1, serie_a=serie_a)
    else:
        flash("You must be logged in  to view this page")
        return redirect("/user/login/")