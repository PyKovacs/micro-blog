from datetime import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient

import json

DB_CONFIG = "db_config.json"


def create_app():
    """ Flask app factory. """

    with open(DB_CONFIG, "r") as db_conf:
        db_uri = json.load(db_conf).get('mongodb_uri')
    app = Flask(__name__)
    client = MongoClient(db_uri)
    app.db = client.techieblog

    @app.route("/", methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            entry_content = request.form.get('content')
            date = datetime.today().strftime('%Y-%m-%d')
            app.db.entries.insert_one({'content': entry_content, 'date': date})

        entries_with_date = [
            (
                entry['content'],
                entry['date'],
                datetime.strptime(entry['date'], '%Y-%m-%d').strftime('%b %d')
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("posts.html", main='posts', entries=entries_with_date)

    @app.route('/calendar')
    def calendar():
        return render_template('calendar.html', main='calendar')

    return app
