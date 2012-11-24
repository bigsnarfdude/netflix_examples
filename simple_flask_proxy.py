from flask import Flask
import sys
import urllib2
import transaction
from ZODB.FileStorage import FileStorage
from ZODB.DB import DB

app = Flask(__name__)

@app.route('/url/<data>')
def url(data):
    data = "http://" + data
    return urllib2.urlopen(data).read()

app.run()
