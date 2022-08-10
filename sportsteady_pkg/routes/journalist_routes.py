import random, os, re
from flask import Flask, render_template, make_response, request, redirect, flash, session
from sqlalchemy import asc, values, desc
from sportsteady_pkg import  app, db, csrf
from sportsteady_pkg.forms import *
from sportsteady_pkg.models import *
from werkzeug.security import generate_password_hash, check_password_hash



@app.route("/journalist/signup/",methods=["POST","GET"])
def journalist_signup():
    journalst_form = JournalistForm()
    return render_template("journalist/signup.html", journalst_form=journalst_form)

@app.route("/journalist_signup/",methods=["POST","GET"])
def journalist_signing():
    journalist_form = JournalistForm()
    if request.method == "GET":
        return redirect("/journalist/signup/")
    else:
        if journalist_form.validate_on_submit():
            firstname = request.form["firstname"]
            lastname = request.form["lastname"]
            email = request.form["email"]
            address = request.form["address"]
            phone = request.form["phone"]
            password = request.form["password"]
            #Insert into db using the model class
            hashed = generate_password_hash(password)
            journalist = Journalist(first_name=firstname, last_name=lastname, residential_address=address,contact_number=phone, email_address=email,password=hashed)
            db.session.add(journalist)
            db.session.commit()
        
            journalist_id = journalist.id
            journalist_name = journalist.first_name, journalist.last_name
            session["journalistid"] = journalist_id
            session["journalist_name"] = journalist_name
            return redirect("/journalist/dashboard/")
        else:
            return render_template("journalist/signup.html",journalist_form=journalist_form)

@app.route("/journalist/login/")
def journalist_login():
    return render_template("journalist/login.html")

@app.route("/journalist/logging/",methods=["POST","GET"])
def journalist_logging():
    if request.method == "GET":
        return redirect("/journalist/login/")
    else:
        email = request.form["email"]
        password = request.form["pwd"]

        admin = Journalist.query.filter(Journalist.email_address==email).first()

        if admin and check_password_hash(admin.password,password):
            journalist_id = admin.id
            journalist_name = admin.first_name, admin.last_name
            session["journalistid"] = journalist_id
            session["journalist_name"] = journalist_name
            return redirect("/journalist/dashboard/")
        else:
            flash("Invalid Credentials")
            return redirect("/journalist/login/")

@app.route("/journalist/dashboard/",methods=["POST","GET"])
def journalist_dashboard():
    loggedin = session.get("journalistid")
    if loggedin != None:
        admin = Journalist.query.filter(Journalist.id==loggedin).first()
        category = db.session.query(Categories).all()
        all_posts = db.session.query(News).all()
        posts = db.session.query(News).filter(News.journalist_id==loggedin).count()
        first_post = db.session.query(News).filter(News.journalist_id==loggedin).first()
        latest = db.session.query(News).filter(News.journalist_id==loggedin).order_by(News.news_id.desc()).first()
        return render_template("journalist/dashboard.html",admin=admin, category=category, all_posts=all_posts, posts=posts,first_post=first_post,latest=latest)
    else:
        flash("You must be logged in  to view this page")
        return redirect("/journalist/login/")

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

@app.route("/add/post/",methods=["POST","GET"])
def add_post():
    loggedin = session.get("journalistid")
    if loggedin != None:
        admin = Journalist.query.filter(Journalist.id==loggedin).first()
        category = db.session.query(Categories).all()
        return render_template("journalist/add_post.html",admin=admin, category=category)
    else:
        flash("You must be logged in  to view this page")
        return redirect("/journalist/login/")

@app.route("/post/",methods=["POST"])
def post():
    loggedin = session.get("journalistid")
    if loggedin != None:
        if request.files != "":
            post = request.form["content"]
            title = request.form["title"]
            category = request.form.getlist("category")

            allowed = [".jpeg",".jpg",".webp",".png"]
            picture = request.files["image"]
            file_name = picture.filename

            newname = random.random() * 1000
            image, ext = os.path.splitext(file_name)

            if ext in allowed and post != "":
                file_path = "sportsteady_pkg/static/uploads/"+str(newname)+ext
                picture.save(f"{file_path}")

                for i in category:
                    cat = News()
                    cat.cat_id = i
                    db.session.add(cat)
                    cat.news_title = title
                    cat.news_content = cleanhtml(post)
                    cat.news_image = str(newname)+ext
                    cat.journalist_id = loggedin
                    db.session.commit()
                    flash("News Successfully Posted!")
                    return redirect("/journalist/dashboard/")
            else:
                flash("Invalid File format")
                return redirect("/journalist/dashboard/")
        else:
            flash("Please Select a valid image")
            return redirect("/journalist/dashboard/")
    else:
        return redirect("/journalist/login")

@app.route("/manage/post/")
def manage_post():
    loggedin = session.get("journalistid")
    if  loggedin != None:
        admin = Journalist.query.filter(Journalist.id==loggedin).first()
        all_posts = db.session.query(News).filter(News.journalist_id==loggedin).all()
        return render_template("journalist/manage_post.html",admin=admin, all_posts=all_posts)
    else:
        return redirect("/journalist/login/")
        

@app.route("/edit/post/<id>/")
def edit_post(id):
    post_id = db.session.query(News).get(id)
    category = db.session.query(Categories).all()
    return render_template("journalist/update_post.html",post_id=post_id,category=category)

@app.route("/update/post/", methods=["POST"])
def update_post():
    loggedin = session.get("journalistid")
    if  loggedin != None:
        edited_title = request.form["title"]
        edited_post = request.form["content"]
        edited_image = request.files["image"]
        news_id = request.form["newsid"]

        allowed = [".jpeg",".jpg",".webp",".png"]
        file_name = edited_image.filename
        newname = random.random() * 1000
        image, ext = os.path.splitext(file_name)
        
        if request.files != "" or edit_post != "" or edited_title != "" and ext in allowed:
            
            
            file_path = "sportsteady_pkg/static/uploads/"+str(newname)+ext
            edited_image.save(f"{file_path}")

            news = db.session.query(News).get(news_id)
            news.news_title = edited_title
            news.news_content = cleanhtml(edited_post) 
            news.news_image = str(newname)+ext
            db.session.commit()
            flash ("Post Updated!")
            return redirect("/manage/post/")
        else:
            flash ("You cannot pass an empty field")
            return redirect("/update/post/")
    else:
        return redirect("/journalist/login/")

@app.route("/delete/post/<id>/")
def delete_post(id):
    post_id = db.session.query(News).get(id)
    db.session.delete(post_id)
    db.session.commit()
    flash("Post Deleted!")
    return redirect("/manage/post/")


@app.route("/journalist/logout/")
def journalist_logout():
    session.pop("journalistid")
    session.pop("journalist_name")
    return redirect("/journalist/login/")