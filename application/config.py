import os
basedir= os.path.abspath(os.path.dirname(__file__))
class config():
    DEBUG= True
    SQLITE_DB_DIR=os.path.join(basedir,"../info_base")
    SQLALCHEMY_DATABASE_URI ="sqlite:///" + os.path.join(SQLITE_DB_DIR,"library.db")
