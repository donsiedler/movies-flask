import os
import requests
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////movies.db"
# initialize the app with the extension
db.init_app(app)
Bootstrap5(app)


class Movie(db.Model):
    pass


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
