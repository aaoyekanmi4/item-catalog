from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, func, desc
from sqlalchemy.orm import sessionmaker
from catalog_setup import Base, Category, Item, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from werkzeug.utils import secure_filename
from flask import send_from_directory
import os

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/images')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'svg'])



app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "catalog app"


# Connect to Database and create database session
engine = create_engine('sqlite:///musicstore.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
def upload_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename

def uploaded_file(filename):

    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

#JSON for main, category, and item pages
@app.route('/JSON')
@app.route('/main/JSON')
def show_mainJSON():
    categories = session.query(Category).order_by(Category.name).all()
    return jsonify(categories=[c.serialize for c in categories])

@app.route('/<string:category_name>/JSON')
def show_categoryJSON(category_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(Item).filter_by(category_id = category.id).all()
    return jsonify(items = [i.serialize for i in items])

@app.route('/<string:category_name>/<string:item_name>/JSON')
def show_itemJSON(category_name, item_name):
    item = session.query(Item).filter_by(name= item_name).one()
    return jsonify(item = item.serialize)



# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
        print "1", credentials
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    print "2", credentials
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_credentials = login_session.get('credentials')
    print "4", stored_credentials
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    flash("You are now logged in as %s" % login_session['username'])
    print "done!"
    output = "Welcome!"
    return output



# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    c = login_session['access_token']
    print 'In gdisconnect access token is %s', c
    if c is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % c
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("You have been logged out")
        return redirect(url_for('show_main'))
# Show main page
@app.route('/', methods=['GET', 'POST'])
@app.route('/main/', methods=['GET', 'POST'])
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




# Show a category's items
@app.route('/<string:category_name>/<string:sort_type>', methods=['GET', 'POST'])
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
            price = float(item.price[1:])
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

# Show item
@app.route('/<string:category_name>/<string:item_name>/', methods=['GET', 'POST'])
def show_item(category_name, item_name):
    if request.method == 'POST':
        search = request.form['search']
        return redirect(url_for('searchresult', search = search, sort_type = 'all'))
    else:
        categories = session.query(Category).order_by(Category.name).all()
        item = session.query(Item).filter_by(name = item_name).one()
        if 'username' not in login_session:
            return render_template('publicitem.html', item = item, categories = categories)
        return render_template('item.html', item = item, categories = categories)






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
        print filename
        print "hurray"
        item = Item(name=request.form['name'], price = request.form['price'],
        description = request.form['description'], picture = filename,
        category = category, user_id = login_session['user_id'])
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
        if request.form['price']:
            item.price = request.form['price']
        if request.form['picture']:
            item.picture = request.form['picture']
        flash('%s has been edited' % item.name)
        session.add(item)
        session.commit()
        return redirect(url_for('show_category', item_name = item_name, category_name = category_name, sort_type = 'all'))
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
        session.delete(item)
        session.commit()
        return redirect(url_for('show_category', item_name = item_name, category_name = category_name, sort_type = 'all'))
    else:
        return render_template('delete.html', item = item, categories = categories)

# Search
@app.route('/search/<string:search>/<string:sort_type>', methods=['GET', 'POST'])
def searchresult(search, sort_type):
    if request.method == 'POST':
        search = request.form['search']
        return redirect(url_for('searchresult', search = search, sort_type = 'all'))
    items = session.query(Item).filter(Item.name.like('%' + search + '%')).all()
    if not items:
        items = session.query(Item).filter(Item.name.like('%' + search[:4] + '%')).all()
    search_count = len(items)
    categories = session.query(Category).order_by(Category.name).all()
    pricelist = []
    for item in items:
        price = float(item.price[1:])
        pricelist.append([price, item])
    if sort_type == 'price_asc':
        items = []
        for pair in sorted(pricelist):
            items.append(pair[1])
        if 'username' not in login_session:
            return render_template('publicsearchresults.html', items = items,
             search_count = search_count, search = search, categories = categories)
        return render_template('searchresults.html', items = items, categories = categories, search_count = search_count, search = search)
    elif sort_type == 'price_desc':
        items = []
        for pair in sorted(pricelist, reverse = True):
            items.append(pair[1])
        if 'username' not in login_session:
            return render_template('publicsearchresults.html', items = items,
            search_count = search_count, search = search, categories = categories)
        return render_template('searchresults.html', items = items, categories = categories, search_count = search_count, search = search)
    else:
        if 'username' not in login_session:
            return render_template('publicsearchresults.html', items = items,
            search_count = search_count, search = search, categories = categories)
        return render_template('searchresults.html', items = items, categories = categories, search_count = search_count, search = search)





if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

