from flask import Flask
from application import config
from application.database import db
import os
from datetime import date
app=None
def create_app():
    app=Flask(__name__,template_folder="templates")
    app.app_context().push()
    app.config.from_object(config.config)
    db.init_app(app)
    return app
app=create_app()

from application.controllers import *

if __name__=="__main__":
    app.run(debug=True,threaded=True)