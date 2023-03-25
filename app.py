from datetime import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient

import json

DB_CONFIG = "db_config.json"

def create_app():
    with open(DB_CONFIG, "r") as db_conf:
        db_creds = json.load(db_conf)
    app = Flask(__name__)
    client = MongoClient(f"mongodb+srv://{db_creds.get('username')}:{db_creds.get('password')}@techie-blog-app.fvkbioh.mongodb.net/test")
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
        return render_template("index.html", entries=entries_with_date)
    
    return app
