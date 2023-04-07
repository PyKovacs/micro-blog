from flask import Blueprint
from pymongo import MongoClient

from source.configuration import db_uri
from source.db import MongoDBCrud, get_db_crud_entries, get_db_crud_users
from source.routing import Router

db_client = MongoClient(db_uri)
router = Router(
    get_db_crud_users(MongoDBCrud, db_client),
    get_db_crud_entries(MongoDBCrud, db_client))

blog_app = Blueprint('blog_app', __name__)


@blog_app.route("/", methods=['GET', 'POST'])
def home():
    return router.home()


@blog_app.route('/login', methods=['GET', 'POST'])
def login():
    return router.login()


@blog_app.route('/logout', methods=['GET', 'POST'])
def logout():
    return router.logout()


@blog_app.route('/signup', methods=['GET', 'POST'])
def signup():
    return router.signup()
