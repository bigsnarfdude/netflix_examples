import ZODB
from ZODB.FileStorage import FileStorage
from ZODB.DB import DB

target_file = 'Data.fs'
storage = FileStorage (target_file)
db = DB(storage)
connection = db.open()
root = connection.root()

import transaction
print root.keys()

