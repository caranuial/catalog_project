from flask import Flask, render_template
from flask import request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item, User
import random
import string
from flask import session
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
from flask import make_response

app = Flask(__name__)

# Prepare for database query
engine = create_engine('sqlite:///mycatalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
dbsession = DBSession()


# Index page
@app.route('/')
@app.route('/index')
def homePage():
    categories = dbsession.query(Category).all()
    latestItems = dbsession.query(Item).order_by(Item.id.desc()).limit(10)
    return render_template(
                           "index.html",
                           categories=categories,
                           latestItems=latestItems
                           )

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 'super_secret_key'
    # Open "http://localhost:8000" in browser to avoid origin error in OAuth
    # Google API console should use "http://localhost:8000"
    # The console doesn't support 0.0.0.0
    app.run(host='0.0.0.0', port=8000)
