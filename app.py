from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for, flash
from pymongo import MongoClient
from passlib.hash import pbkdf2_sha256

import json

CONFIG = "config.json"


def create_app():
    """ Flask app factory. """

    app = Flask(__name__)

    with open(CONFIG, "r") as config:
        conf_dict = json.load(config)
        db_uri = conf_dict.get('mongodb_uri')
        app.secret_key = conf_dict.get('secret_key')

    client = MongoClient(db_uri)
    app.db = client.techieblog

    users = {}

    @app.route("/", methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            entry_content = request.form.get('content')
            date = datetime.today().strftime('%Y-%m-%d')
            app.db.entries.insert_one(
                {
                    'content': entry_content,
                    'date': date,
                    'user': session.get('user')
                }
            )

        entries_with_date = [
            (
                entry['content'],
                entry['user'],
                entry['date'],
                datetime.strptime(entry['date'], '%Y-%m-%d').strftime('%b %d')
            )
            for entry in app.db.entries.find({})
        ]
        return render_template(
            "posts.html",
            main='posts',
            entries=entries_with_date,
            user=session.get('user')
        )

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            if password and pbkdf2_sha256.identify(users.get(username, "")):
                if pbkdf2_sha256.verify(password, users.get(username)):
                    session["user"] = username
                    flash(f'User "{session["user"]}" logged in.')
                    return redirect(url_for('home'))
            flash('Incorrect credentials.')

        return render_template('login.html', main='login', user=session.get('user'))

    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        if request.method == 'POST':
            flash(f'User "{session["user"]}" logged out.')
            session['user'] = None

            return redirect(url_for('home'))

        return render_template('logout.html', main='login', user=session.get('user'))

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form.get('username')
            hashed_pwd = pbkdf2_sha256.hash(request.form.get('password'))

            users[username] = hashed_pwd
            session['user'] = username

            flash(f'User "{username}" successfully signed up!')
            return redirect(url_for('home'))

        return render_template('signup.html', main='signup', user=session.get('user'))

    return app
