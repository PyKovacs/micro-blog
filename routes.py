import json
from datetime import datetime

from flask import (Blueprint, flash, redirect, render_template, request,
                   session, url_for)
from passlib.hash import pbkdf2_sha256
from pymongo import MongoClient

from db import MongoDBCrud

blog_app = Blueprint(__name__, 'blog_app')
CONFIG = "config.json"

with open(CONFIG, "r") as config:
    conf_dict = json.load(config)
    db_uri = conf_dict.get('mongodb_uri')
    secret_key = conf_dict.get('secret_key')

db_client = MongoClient(db_uri)
db_crud_entries = MongoDBCrud(db_client.techieblog.entries)
db_crud_users = MongoDBCrud(db_client.techieblog.users)


@blog_app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        entry_content = request.form.get('content')
        date = datetime.today().strftime('%Y-%m-%d')
        db_crud_entries.create(document={
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
        for entry in db_crud_entries.read(document={})
        ]

    return render_template(
        "posts.html",
        main='posts',
        entries=entries_with_date,
        user=session.get('user')
    )


@blog_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        input_password = request.form.get('password')
        user_entry = db_crud_users.read(document={'username': username})

        try:
            db_password = user_entry.next().get('password')
        except StopIteration:
            db_password = None

        if input_password and db_password:
            if (pbkdf2_sha256.identify(db_password)
                    and pbkdf2_sha256.verify(input_password, db_password)):
                session["user"] = username
                flash(f'User "{session["user"]}" logged in.')
                return redirect(url_for('routes.home'))
        flash('Incorrect credentials!')

    return render_template('login.html', main='login', user=session.get('user'))


@blog_app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        flash(f'User "{session["user"]}" logged out.')
        session['user'] = None

        return redirect(url_for('routes.home'))

    return render_template('logout.html', main='login', user=session.get('user'))


@blog_app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        hashed_pwd = pbkdf2_sha256.hash(request.form.get('password'))

        db_crud_users.create(document={
                                    'username': username,
                                    'password': hashed_pwd
                                    }
                             )
        session['user'] = username

        flash(f'User "{username}" successfully signed up!')
        return redirect(url_for('routes.home'))

    return render_template('signup.html', main='signup', user=session.get('user'))
