import os
import requests
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy

from forms import EditForm, AddForm

TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
# initialize the app with the extension
db.init_app(app)
bootstrap = Bootstrap5(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    movies = Movie.query.all()
    return render_template("index.html", movies=movies)


@app.route("/add", methods=["GET", "POST"])
def add():
    add_form = AddForm()
    if add_form.validate_on_submit():
        movie_title = add_form.title.data
        url = f"https://api.themoviedb.org/3/search/movie?query={movie_title}&include_adult=false&language=en-US&page=1"
        headers = {
            "accept": "application/json",
            "Authorization": TMDB_API_KEY,
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        movies = response.json()["results"]
        return render_template("select.html", movies=movies)
    return render_template("add.html", form=add_form)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    movie_to_edit = Movie.query.get(id)
    edit_form = EditForm()
    if edit_form.validate_on_submit():
        movie_to_edit.rating = float(edit_form.rating.data)
        movie_to_edit.review = edit_form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie_to_edit, form=edit_form)


@app.route("/delete/<int:id>")
def delete(id):
    movie_to_delete = Movie.query.get(id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
