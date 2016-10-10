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
engine = create_engine('sqlite:///model/musicstore.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Show item

def show_item(category_name, item_name):
    if request.method == 'POST':
        search = request.form['search']
        return redirect(url_for('searchresult',
            search = search, sort_type = 'all'))
    else:
        categories = session.query(Category).order_by(Category.name).all()
        item = session.query(Item).filter_by(name = item_name).one()
        if 'username' not in login_session:
            return render_template('publicitem.html', item = item,
                categories = categories, status="Login",
            loginlink="/login")
        return render_template('item.html', item = item,
            categories = categories, status="Logout",
            loginlink="/gdisconnect")