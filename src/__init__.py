from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from logging import Logger
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt 

from datetime import timedelta


# Constants 
app = Flask(__name__)
CORS(app,
       resources={r"/*": {"origins": "*"}},
        supports_credentials=True,
     )
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config.update(
    TEMPLATES_AUTO_RELOAD=True
)

bycrypt = Bcrypt(app)
db= SQLAlchemy(app)
migrate = Migrate(app, db)


# app.register_blueprint(auth_route, url_prefix='/api')

@app.route("/")
def hello_world():
    return "<p>Hello, Expedier!</p>"

@app.route("/api/create-applicant", methods=["POST"])
def applicant():
    pass
 
@app.route("/api/create-token", methods=['POST'])
def create_token():
    pass

@app.route("/api/add_document", methods=['POST'])
def create_token():
    pass

@app.route("/api/add_document", methods=['POST'])
def verification_status():
    pass
     

