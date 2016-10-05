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
from catalog_setup import Base, Category, Item, User
from jsonapis import show_mainJSON, show_categoryJSON
from jsonapis import show_itemJSON
from login import show_login, gconnect, create_user
from login import get_user_info, get_user_id
from logout import gdisconnect
from mainpage import show_main
from categorypage import show_category
from itempage import show_item
from search import searchresult

app = Flask(__name__)

# Connect to Database and create database session
engine = create_engine('sqlite:///musicstore.db')
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

# Login(show login page)

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

# New item
@app.route('/<string:category_name>/new', methods=['GET', 'POST'])

def new_item(category_name):
    if 'username' not in login_session:
        flash("Please login to make a new item")
        return redirect('/')
    categories = session.query(Category).order_by(Category.name).all()
    category = session.query(Category).filter_by(name = category_name).one()
    if request.method == 'POST':
        filename = upload_file()
        price = valid_price(request.form['price'])
        if not price:
            flash("That's not a valid price")
            return render_template('new.html', categories= categories)
        if price and request.form['name'] and request.form['description']:
            item = Item(name=request.form['name'], price = request.form['price'],
            description = request.form['description'], picture = filename,
            category = category, user_id = login_session['user_id'])
        else:
            flash("Please fill out the required fields.")
            return render_template('new.html', categories= categories)
        flash('%s has been added' % item.name)
        session.add(item)
        category.items_val += 1

        session.add(category)
        session.commit()
        return redirect(url_for('show_category', item_name = request.form['name'],
        category_name = category_name, sort_type = all))
    else:
        return render_template('new.html', categories = categories)


# Edit item
@app.route('/<string:category_name>/<string:item_name>/edit', methods=['GET', 'POST'])
def edit_item(category_name, item_name):
    item = session.query(Item).filter_by(name = item_name).one()
    categories = session.query(Category).order_by(Category.name).all()
    if item.user_id != login_session['user_id']:
        flash("You may only edit items you have created")
        return redirect(url_for('show_category', item_name = item_name, category_name = category_name, sort_type = 'all'))
    if request.method == 'POST':

        if request.form['name']:
            item.name = request.form['name']
        if request.form['description']:
            item.description = request.form['description']
        price = valid_price(request.form['price'])
        if not price:
            flash("That's not a valid price")
            return render_template('edit.html', item=item, categories= categories)
        if price and request.form['name'] and request.form['description']:
            filename = upload_file()
            item.picture = filename
            flash('%s has been edited' % item.name)
            session.add(item)
            session.commit()
            return redirect(url_for('show_category', item_name = item_name, category_name = category_name, sort_type = 'all'))
        else:
            flash("Please fill out the required fields.")
            return render_template('edit.html', item = item, categories = categories)
    else:
        return render_template('edit.html', item = item, categories = categories)


# Delete item
@app.route('/<string:category_name>/<string:item_name>/delete', methods=['GET', 'POST'])
def delete_item(category_name, item_name):
    item = session.query(Item).filter_by(name = item_name).first()
    categories = session.query(Category).order_by(Category.name).all()
    category = session.query(Category).filter_by(name = category_name).one()
    if item.user_id != login_session['user_id']:
        flash("You may only delete items you have created")
        return redirect(url_for('show_category', item_name = item_name, category_name = category_name, sort_type = 'all'))
    if request.method == 'POST':
        flash('%s has been deleted' % item.name)
        category.items_val -= 1
        session.add(category)
        if item.picture:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], item.picture))
        session.delete(item)
        session.commit()
        return redirect(url_for('show_category', item_name = item_name, category_name = category_name, sort_type = 'all'))
    else:
        return render_template('delete.html', item = item, categories = categories)







if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

