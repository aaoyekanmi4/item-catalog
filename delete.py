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

# Delete item

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