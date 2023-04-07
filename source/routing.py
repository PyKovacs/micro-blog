from datetime import datetime

from flask import flash, redirect, render_template, request, session, url_for
from passlib.hash import pbkdf2_sha256
from werkzeug.wrappers.response import Response

from source.db import DBCrudInterface


class Router:
    def __init__(self, db_users: DBCrudInterface, db_entries: DBCrudInterface) -> None:
        self.db_users = db_users
        self.db_entries = db_entries

    def home(self) -> str:
        """ Home page with all posts and new post window. """
        
        if request.method == 'POST':
            entry_content = request.form.get('content')
            date = datetime.today().strftime('%Y-%m-%d')
            self.db_entries.create(document={
                                    'content': entry_content,
                                    'date': date,
                                    'user': session.get('user')
                                        })
        entries_with_date = [(
                entry['content'],
                entry['user'],
                entry['date'],
                datetime.strptime(entry['date'], '%Y-%m-%d').strftime('%b %d')
            ) for entry in self.db_entries.read(document={})]

        return render_template(
            "posts.html",
            main='posts',
            entries=entries_with_date,
            user=session.get('user')
        )

    def login(self) -> (Response | str):
        """ Login page with credentials form. """
        
        if request.method == 'POST':
            username = request.form.get('username')
            input_password = request.form.get('password')
            user_entry = self.db_users.read(document={'username': username})

            try:
                db_password = user_entry.next().get('password')
            except StopIteration:
                db_password = None

            if input_password and db_password:
                if (pbkdf2_sha256.identify(db_password)
                        and pbkdf2_sha256.verify(input_password, db_password)):
                    session["user"] = username
                    flash(f'User "{session["user"]}" logged in.')
                    return redirect(url_for('blog_app.home'))
            flash('Incorrect credentials!')

        return render_template('login.html', main='login', user=session.get('user'))

    def logout(self) -> (Response | str):
        """ Logout page with logout button. """
        
        if request.method == 'POST':
            flash(f'User "{session["user"]}" logged out.')
            session['user'] = None
            return redirect(url_for('blog_app.home'))

        return render_template('logout.html', main='login', user=session.get('user'))

    def signup(self) -> (Response | str):
        """ Signup page with credentials form. """
        
        if request.method == 'POST':
            username = request.form.get('username')
            hashed_pwd = pbkdf2_sha256.hash(request.form.get('password'))

            self.db_users.create(document={
                                        'username': username,
                                        'password': hashed_pwd
                                        }
                                 )
            session['user'] = username

            flash(f'User "{username}" successfully signed up!')
            return redirect(url_for('blog_app.home'))

        return render_template('signup.html', main='signup', user=session.get('user'))
