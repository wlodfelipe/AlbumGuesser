import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify, url_for
from flask_session import Session
#from werkzeug.security import check_password_hash, generate_password_hash
from helpers import *
from datetime import timedelta, datetime

# Configure application
app = Flask(__name__)

app.secret_key = os.getenv('secret_key')

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.permanent_session_lifetime = timedelta(seconds=60)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///albums.db")

POINTS = 0
ALBUM_ID = 1

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/AlbumGuesser", methods=["GET", "POST"])
def albumGuesser():
    global POINTS
    global ALBUM_ID

    if request.method == "GET":
        difficulty_mode = {"easy": 100, "hard": 5000}
        inputMode = request.args.get("mode")
        if inputMode not in difficulty_mode:
            return redirect("/")
        print("The input mode was: ", inputMode)
        difficulty_mode = difficulty_mode.get(inputMode)
        print("The difficulty mode is: ", difficulty_mode)


        POINTS = 0
        REPEATED_ALBUMS.clear()
        print(REPEATED_ALBUMS)

        randomAlbum = getRandomAlbum(difficulty_mode)
        ALBUM_ID = randomAlbum
        album = album_info(randomAlbum)

        session.permanent = True # starts a 60 sec session
        session['permanent_session_lifetime'] = datetime.now()
        session['difficulty'] = difficulty_mode
        return render_template("AlbumGuesser.html", album=album["image"], points=POINTS)

    if request.method == "POST":
        try:
            album = album_info(ALBUM_ID)
            if album is not None and album.get("image") is not None:
                image_url = album["image"]
            else:
                album = {'name': 'error', 'artist': 'error', 'release_date': 'error', 'image': 'error'}
        except TypeError as e:
            album = {'name': 'error', 'artist': 'error', 'release_date': 'error', 'image': 'error'}

        inputAlbumName = request.form.get("albumName")
        inputDate = request.form.get("albumReleaseDate")
        inputArtistName = request.form.get("artistName")

        if inputAlbumName:
            fairness_distance = levenshtein_distance(album['name'].lower(), inputAlbumName.lower())
            if fairness_distance <= 4:
                POINTS += 1
                flash("😎 You got the last album name right! +1 point")

        if inputArtistName:
            fairness_distance = levenshtein_distance(album["artist"].lower(), inputArtistName.lower())
            if fairness_distance <= 3:
                POINTS += 1
                flash("😎 You got the last artist name right! +1 point")

        if inputDate:
            date = album["release_date"]
            date = date[:4]
            print(album["release_date"])
            print(date)

            if inputDate == date:
                POINTS += 3
                flash("😎 You got the last album release year right! +3 point")


        randomAlbum = getRandomAlbum(session['difficulty'])
        ALBUM_ID = randomAlbum
        album = album_info(randomAlbum)
        results_url = url_for('results', score=POINTS) # url_for() generates a url for the future results route with parameters such as score
        return render_template("AlbumGuesser.html", album=album["image"], points=POINTS, results_url=results_url)
        # might crash

@app.route('/check_session', methods=["GET"])
def check_session():
    if 'permanent_session_lifetime' in session:
        print("the permanent session lifetime in sessin is: ", session['permanent_session_lifetime'])
        # Removing timezone info
        current_time = datetime.now().replace(tzinfo=None)
        session_time = session['permanent_session_lifetime'].replace(tzinfo=None)

        elapsed_time = current_time - session_time
        print("elapsed time is: ", elapsed_time)

        if elapsed_time.total_seconds() <= 60:
            return jsonify({'status': 'active', 'time': (elapsed_time.total_seconds() - 62)*-1})

    return jsonify({'status': 'inactive'})


@app.route('/results/<score>', methods=["GET"])
def results(score):
    return render_template("results.html", score=score)

@app.route('/unlimited', methods=["GET", "POST"])
def unlimited():
    global POINTS
    global ALBUM_ID

    if request.method == "GET":
        inputMode = request.args.get("mode")
        if inputMode != "unlimited":
            return redirect("/")
        print("The input mode was: ", inputMode)

        POINTS = 0
        REPEATED_ALBUMS.clear()
        print(REPEATED_ALBUMS)

        randomAlbum = getRandomAlbum(5000)
        ALBUM_ID = randomAlbum
        album = album_info(randomAlbum)

        return render_template("unlimited.html", album=album["image"], points=POINTS)

    if request.method == "POST":
        try:
            album = album_info(ALBUM_ID)
            if album is not None and album.get("image") is not None:
                image_url = album["image"]
            else:
                album = {'name': 'error', 'artist': 'error', 'release_date': 'error', 'image': 'error'}
        except TypeError as e:
            album = {'name': 'error', 'artist': 'error', 'release_date': 'error', 'image': 'error'}

        inputAlbumName = request.form.get("albumName")
        inputDate = request.form.get("albumReleaseDate")
        inputArtistName = request.form.get("artistName")


        if inputAlbumName:
            fairness_distance = levenshtein_distance(album['name'].lower(), inputAlbumName.lower())
            if fairness_distance <= 4:
                POINTS += 1
                flash("😎 You got the last album name right! +1 point")
            else:
                flash("📝 The last album's name was " + album["name"])
        else:
            flash("📝 The last album's name was " + album["name"])

        if inputArtistName:
            fairness_distance = levenshtein_distance(album["artist"].lower(), inputArtistName.lower())
            if fairness_distance <= 3:
                POINTS += 1
                flash("😎 You got the last artist name right! +1 point")
            else:
                flash("📝The last artist's name was " + album["artist"])
        else:
                flash("📝The last artist's name was " + album["artist"])

        if inputDate:
            date = album["release_date"]
            date = date[:4]
            print(album["release_date"])
            print(date)

            if inputDate == date:
                POINTS += 3
                flash("😎 You got the last album release year right! +3 point")
            else:
                flash("📝 The last album's release year was " + date)
        else:
                flash("📝 The last album's release year was " + album["release_date"][:4])


        randomAlbum = getRandomAlbum(5000)
        ALBUM_ID = randomAlbum
        image_url = ""

        try:
            album = album_info(randomAlbum)
            if album is not None and album.get("image") is not None:
                image_url = album["image"]
            else:
                album = {'name': 'error', 'artist': 'error', 'release_date': 'error', 'image': 'error'}
        except TypeError as e:
            album = {'name': 'error', 'artist': 'error', 'release_date': 'error', 'image': 'error'}

        results_url = url_for('results', score=POINTS) # url_for() generates a url for the future results route with parameters such as score
        return render_template("unlimited.html", album=image_url, points=POINTS, results_url=results_url)


if __name__ == "__main__":
    configure()
    app.run(debug=True)