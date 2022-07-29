from flask import Flask, render_template, request, flash, redirect, url_for
# from models import User, db
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menu.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
import os


class Base(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    menu_title = db.Column(db.String(30))
    menu_composition = db.Column(db.String(2000))
    price = db.Column(db.String(10))


IMAGES_FOLDER = os.path.join('static', 'icons')
app.config['UPLOAD_FOLDER'] = IMAGES_FOLDER


# set FLASK_APP=main.py
# set FLASK_ENV=development
# flask run


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/telli', methods=['GET', 'POST'])
def menu():
    x = Base.query.order_by(Base.id).all()
    return render_template("telli.html", x=x)


@app.route('/aruanne')
def aruanne():
    return render_template("aruanne.html")


@app.route('/register', methods=("POST", "GET"))
def register():
    delete_img = os.path.join(app.config['UPLOAD_FOLDER'], 'delete.png')
    edit_img = os.path.join(app.config['UPLOAD_FOLDER'], 'edit.png')
    if request.method == "POST":
        u = Base(menu_title=request.form['menu_title'], menu_composition=request.form['menu_composition'],
                 price=request.form['price'])
        db.session.add(u)
        # db.session.flush()
        db.session.commit()
    else:
        x = Base.query.order_by(Base.id).all()
        return render_template("register.html", x=x, delete_img=delete_img, edit_img=edit_img)
    x = Base.query.order_by(Base.id).all()
    return render_template("register.html", x=x, delete_img=delete_img, edit_img=edit_img)


@app.route('/delete/<int:id>')
def delete(id):
    me = Base.query.filter_by(id=id).first()
    db.session.delete(me)
    db.session.commit()
    # flash("Запись удалена!")
    return redirect('/register')


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    if request.method == "POST":
        admin = Base.query.filter_by(id=id).first()
        admin.menu_title = request.form['menu_title']
        admin.menu_composition = request.form['menu_composition']
        admin.price = request.form['price']
        db.session.commit()
        return redirect(url_for('register'))
    else:
        me = Base.query.filter_by(id=id).first()
        return render_template("update.html", x=me)
