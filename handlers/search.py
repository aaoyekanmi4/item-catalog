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



# Search

def searchresult(search, sort_type):
    if request.method == 'POST':
        search = request.form['search'].lower()
        return redirect(url_for('searchresult', search = search,
            sort_type = 'all'))
    items = session.query(Item).filter(Item.name.like('%' + search + '%')).all()
    if not items:
        items = session.query(Item).filter(Item.name.like('%' + search[:4] + '%')).all()
    search_count = len(items)
    categories = session.query(Category).order_by(Category.name).all()
    pricelist = []
    for item in items:
        price = float(item.price)
        pricelist.append([price, item])
    if sort_type == 'price_asc':
        items = []
        for pair in sorted(pricelist):
            items.append(pair[1])
        if 'username' not in login_session:
            return render_template('publicsearchresults.html', items = items,
             search_count = search_count, search = search,
             categories = categories, status="Login",
            loginlink="/login")
        return render_template('searchresults.html', items = items,
         categories = categories, search_count = search_count,
         search = search, status="Logout",
            loginlink="/gdisconnect")
    elif sort_type == 'price_desc':
        items = []
        for pair in sorted(pricelist, reverse = True):
            items.append(pair[1])
        if 'username' not in login_session:
            return render_template('publicsearchresults.html',
            items = items, search_count = search_count, search = search,
            categories = categories, status="Login",
            loginlink="/login")
        return render_template('searchresults.html', items = items,
            categories = categories, search_count = search_count,
            search = search, status="Logout",
            loginlink="/gdisconnect")
    else:
        if 'username' not in login_session:
            return render_template('publicsearchresults.html', items = items,
            search_count = search_count, search = search,
            categories = categories,
             status="Login", loginlink="/login")
        return render_template('searchresults.html', items = items,
            categories = categories, search_count = search_count,
            search = search, status="Logout",
            loginlink="/gdisconnect")