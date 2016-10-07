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

# Show a category's items
def show_category(category_name, sort_type):
    if request.method == 'POST':
        search = request.form['search']
        return redirect(url_for('searchresult', search = search, sort_type = 'all'))
    else:
        categories = session.query(Category).order_by(Category.name).all()
        thiscategory = session.query(Category).filter_by(name=category_name).one()
        items = session.query(Item).filter_by(category_id = thiscategory.id).all()
        pricelist = []
        for item in items:
            price = float(item.price)
            pricelist.append([price, item])
        if sort_type == 'price_asc':
            items = []
            for pair in sorted(pricelist):
                items.append(pair[1])
            if 'username' not in login_session:
                return render_template('publiccategory.html', items = items,
            thiscategory = thiscategory, categories = categories)
            return render_template('category.html', items = items,
            thiscategory = thiscategory, categories = categories)
        elif sort_type == 'price_desc':
            items = []
            for pair in sorted(pricelist, reverse = True):
                items.append(pair[1])
            if 'username' not in login_session:
                return render_template('publiccategory.html', items = items,
            thiscategory = thiscategory, categories = categories)
            return render_template('category.html', items = items,
            thiscategory = thiscategory, categories = categories)
        else:
            if 'username' not in login_session:
                return render_template('publiccategory.html', items = items,
                thiscategory = thiscategory, categories = categories)
            return render_template('category.html', items = items,
            thiscategory = thiscategory, categories = categories)

