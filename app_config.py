from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


DATABASE_CONNECTION = "mysql+mysqlconnector://root:root@localhost/flaskBlog"


# engine = create_engine("mysql+mysqlconnector://root:root@localhost/flaskBlog")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_PRE_PING'] = True
db = SQLAlchemy(app=app)






