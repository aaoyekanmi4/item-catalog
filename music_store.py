import random
import string
import requests
import httplib2
import json
import os
import re

from flask import Flask, render_template, request, url_for
from flask import make_response, redirect, jsonify, flash
from flask import session as login_session

from sqlalchemy import create_engine, asc, func, desc
from sqlalchemy.orm import sessionmaker

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from werkzeug.utils import secure_filename

from model import Base, Category, Item, User


from handlers import show_mainJSON, show_categoryJSON, show_itemJSON
from handlers import show_login, gconnect, create_user, get_user_info

from handlers import get_user_id, gdisconnect, show_main, show_category
from handlers import show_item, searchresult, new_item, edit_item, delete_item



app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///model/musicstore.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Constants and functions for uploading pictures
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/images')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'svg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename


# Function for determining valid price with regular expressions
PRICE_RE = re.compile(r"^\d{0,8}(\.\d{1,4})?$")
def valid_price(price):
    return PRICE_RE.match(price)

# Application

# JSON endpoints for main, category, and item pages

show_mainJSON = app.route('/JSON')(show_mainJSON)
show_mainJSON = app.route('/main/JSON')(show_mainJSON)

show_categoryJSON = app.route('/<string:category_name>/JSON')(show_categoryJSON)

show_itemJSON = app.route('/<string:category_name>/<string:item_name>/JSON')(show_itemJSON)

# Show Login Page
show_login = app.route('/login')(show_login)

# Gconnect(login through google)
gconnect = app.route('/gconnect', methods=['POST'])(gconnect)

# Gdisconnect(Logout with google)
gdisconnect = app.route('/gdisconnect')(gdisconnect)

# Show main page with latest items from all categories
show_main = app.route('/', methods=['GET', 'POST'])(show_main)
show_main = app.route('/main/', methods=['GET', 'POST'])(show_main)

# Show a category's items
show_category = app.route('/<string:category_name>/<string:sort_type>', methods=['GET', 'POST'])(show_category)

#Show a particular item
show_item = app.route('/<string:category_name>/<string:item_name>/', methods=['GET', 'POST'])(show_item)

# Get search results
searchresult = app.route('/search/<string:search>/<string:sort_type>', methods=['GET', 'POST'])(searchresult)

# Make a new item
new_item = app.route('/<string:category_name>/new', methods=['GET', 'POST'])(new_item)

# Edit item
edit_item = app.route('/<string:category_name>/<string:item_name>/edit', methods=['GET', 'POST'])(edit_item)

# Delete item
delete_item = app.route('/<string:category_name>/<string:item_name>/delete', methods=['GET', 'POST'])(delete_item)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

