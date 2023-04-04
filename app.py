from datetime import datetime
from flask import Flask, render_template, request, session, redirect
from pymongo import MongoClient

import json

DB_CONFIG = "db_config.json"


def create_app():
    """ Flask app factory. """

    app = Flask(__name__)

    with open(DB_CONFIG, "r") as db_conf:
        db_uri = json.load(db_conf).get('mongodb_uri')
        app.secret_key = json.load(db_conf).get('mongodb_uri')

    client = MongoClient(db_uri)
    app.db = client.techieblog

    users = {}

    @app.route("/", methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            entry_content = request.form.get('content')
            date = datetime.today().strftime('%Y-%m-%d')
            app.db.entries.insert_one({'content': entry_content, 'date': date, 'user': session.get('user')})

        entries_with_date = [
            (
                entry['content'],
                entry['user'],
                entry['date'],
                datetime.strptime(entry['date'], '%Y-%m-%d').strftime('%b %d')
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("posts.html", main='posts', entries=entries_with_date, user=session.get('user'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return render_template('login.html', main='login')
    
    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        if request.method == 'POST':
            session['user'] = None
            redirect('/', 200)  # not working
            
        return render_template('logout.html', main='login')
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            users[username] = password
            session['user'] = username
            
        return render_template('signup.html', main='signup')

    return app
