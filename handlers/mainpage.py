from flask import Flask, render_template, request, url_for
from flask import make_response, redirect, jsonify, flash
from flask import session as login_session

from sqlalchemy import create_engine, asc, func, desc
from sqlalchemy.orm import sessionmaker

from catalog_setup import Base, Category, Item, User

# Connect to Database and create database session
engine = create_engine('sqlite:///musicstore.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



# Show main page

def show_main():

    if request.method == 'POST':
        search = request.form['search']
        return redirect(url_for('searchresult', search = search, sort_type = 'all'))
    else:
        rw1categories = session.query(Category).order_by(Category.name).limit(3)
        items = []
        for category in rw1categories:
            item = session.query(Item).filter_by(category_id = category.id).order_by(Item.when_added.desc()).first()
            items.append(item)
        items_row1 = items
        items = []
        rw2categories = session.query(Category).order_by(Category.name).limit(3).offset(3)
        for category in rw2categories:
            item = session.query(Item).filter_by(category_id = category.id).order_by(Item.when_added.desc()).first()
            items.append(item)
        items_row2 = items
        categories = session.query(Category).order_by(Category.name).all()
        if 'username' not in login_session:
            return render_template('publicmain.html',
            categories = categories, items_row1 = items_row1, items_row2 = items_row2)
        else:
            return render_template('main.html',
            categories = categories, items_row1 = items_row1, items_row2 = items_row2)
