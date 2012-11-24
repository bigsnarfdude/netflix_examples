from flask import Flask
import urllib2
import transaction
from ZODB.FileStorage import FileStorage
from ZODB.DB import DB

app = Flask(__name__)
db_filename = "Data.fs"
root = []

def open_db(data, client_data):
    storage = FileStorage(db_filename)
    db = DB(storage)
    connection = db.open()
    root = connection.root()
    print "database started"
    root[data] = client_data
    transaction.commit()
    print "transaction committed"
    db.close()
    print "closed db"
    return client_data

def get_web(data):
    return urllib2.urlopen(data).read()


@app.route('/url/<data>')
def url(data):
    data = "http://" + data
    client_data = get_web(data)
    return open_db(data, client_data)


app.run()
