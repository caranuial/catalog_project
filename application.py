from flask import Flask, render_template
from flask import request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
import random
import string
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
from flask import make_response

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "WinterCatalog"

# Prepare for database query
engine = create_engine('sqlite:///mycatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
dbsession = DBSession()

# Login page
@app.route('/login')
def login():
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits)
        for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# Google Connect
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
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    print(access_token)
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

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
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
    login_session['logged_in'] = True
    
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    dbsession.add(newUser)
    dbsession.commit()
    user = dbsession.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = dbsession.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = dbsession.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    print(access_token)
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print(result)
    if result['status'] == '200':
        #response = make_response(json.dumps('Successfully disconnected.'), 200)
        #response.headers['Content-Type'] = 'application/json'
        #return response
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        login_session.pop('logged_in', None)
        flash('You are now logged out.')
        return redirect('/index')
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# Index page
@app.route('/')
@app.route('/index')
def homePage():
    categories = dbsession.query(Category).distinct()
    latestItems = dbsession.query(Item).order_by(Item.id.desc()).limit(10)
    #latestItems = dbsession.query(User).distinct().limit(10)
    return render_template(
                           "index.html",
                           categories=categories,
                           latestItems=latestItems,
                           login_session=login_session
                           )

# Show items in a category
@app.route('/catalog/<category_id>')
def categoryFullInfo(category_id):
    categories = dbsession.query(Category).distinct()
    currentCategory = dbsession.query(Category).filter(Category.id == category_id).one()
    items = dbsession.query(Item).filter(Item.category_id == category_id).distinct()
    count = items.count()
    return render_template(
                           "categoryDetails.html",
                           categories=categories,
                           category_name=currentCategory.name,
                           items=items,
                           count=count,
                           login_session=login_session
                           )

# Delete item in a category
@app.route('/catalog/<category_id>/<item_id>/delete', methods=['POST', 'GET'])
def deleteItem(category_id, item_id):

    itemToDelete = dbsession.query(Item).filter(Item.id == item_id).one()
    
    if request.method == 'POST':
        dbsession.delete(itemToDelete)
        flash('%s Successfully Deleted' % itemToDelete.title)
        dbsession.commit()
        return redirect(url_for('categoryFullInfo',
                                category_id=itemToDelete.category_id,
                                login_session=login_session
                                ))
    else:
        return render_template(
                               'deleteItem.html',
                               item=itemToDelete,
                               category_id=itemToDelete.category_id,
                               login_session=login_session
                               )

# Create a new item
@app.route('/catalog/item/new/', methods=['GET', 'POST'])
def newItem():
    categories = dbsession.query(Category).distinct()
    if request.method == 'POST':
        newItem = Item(
                       user_id=1,
                       title=request.form['title'],
                       description=request.form['description'],
                       category_id=request.form['category']
                      )
        dbsession.add(newItem)
        dbsession.commit()
        flash('New Menu %s Item Successfully Created' % (newItem.title))
        return redirect(url_for('homePage'))
    else:
        return render_template(
                               'addItem.html',
                               categories=categories,
                               login_session=login_session
                               )

# Item Edit
@app.route('/catalog/<category_id>/<item_id>/edit/', methods=['GET', 'POST'])
def editItem(category_id, item_id):
    categories = dbsession.query(Category).distinct()
    currentCategory = dbsession.query(Category).filter(Category.id == category_id).one()
    currentItem = dbsession.query(Item).filter(Item.id == item_id).one()
    if request.method == 'POST':
        if request.form['title']:
            currentItem.name = request.form['title']
        if request.form['description']:
            currentItem.description = request.form['description']
        if request.form['category']:
            currentItem.category_id = request.form['category']
        dbsession.add(currentItem)
        dbsession.commit()
        flash('Item Successfully Edited')
        return redirect(url_for('homePage'))
    else:
        return render_template(
                               'editItem.html',
                               categories=categories,
                               currentCategory=currentCategory,
                               item=currentItem,
                               login_session=login_session
                               )

# Item Description
@app.route('/description/<category_id>/<item_id>')
def itemDescription(category_id, item_id):
    categories = dbsession.query(Category).distinct()
    item = dbsession.query(Item).filter(Item.id == item_id).one()
    currentCategory = dbsession.query(Category).filter(Category.id == item.category_id).one()
    return render_template(
                           "itemDescription.html",
                           categories=categories,
                           category_name=currentCategory.name,
                           item=item,
                           login_session=login_session
                           )

# JSON APIs to view Restaurant Information
@app.route('/catalog/JSON')
def catalogJSON():
    categories = dbsession.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])

						   
if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    # Open "http://localhost:8000" in browser to avoid origin error in OAuth
    # Google API console should use "http://localhost:8000"
    # The console doesn't support 0.0.0.0
    app.run(host='0.0.0.0', port=8000)
