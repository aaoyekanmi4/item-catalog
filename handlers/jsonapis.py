#JSON for main, category, and item pages
from flask import jsonify
from sqlalchemy import create_engine, asc, func, desc
from sqlalchemy.orm import sessionmaker
from catalog_setup import Base, Category, Item, User
engine = create_engine('sqlite:///musicstore.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def show_mainJSON():
    categories = session.query(Category).order_by(Category.name).all()
    return jsonify(categories=[c.serialize for c in categories])


def show_categoryJSON(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id = category.id).all()
    return jsonify(items = [i.serialize for i in items])


def show_itemJSON(category_name, item_name):
    item = session.query(Item).filter_by(name= item_name).one()
    return jsonify(item = item.serialize)
