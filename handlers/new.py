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


engine = create_engine('sqlite:///musicstore.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Constants and functions for uploading pictures
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/images')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'svg'])

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

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# New item function

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

