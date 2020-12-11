from flask import Flask, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)


app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://usersql:usersql@localhost/aurora'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
Migrate(app, db)

from periscope.ballasting.views import ballasting_blueprint
from periscope.batteries.views import batteries_blueprint
from periscope.tension.views import tension_blueprint
from periscope.instest.views import instest_blueprint
from periscope.digest.views import digest_blueprint

app.register_blueprint(ballasting_blueprint, url_prefix='/ballasting')
app.register_blueprint(batteries_blueprint, url_prefix='/batteries')
app.register_blueprint(instest_blueprint, url_prefix='/instest')
app.register_blueprint(tension_blueprint, url_prefix='/tension')
app.register_blueprint(digest_blueprint, url_prefix='/digest')
