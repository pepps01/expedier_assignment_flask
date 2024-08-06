from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from logging import Logger
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt 
import random
import string
import os

from datetime import timedelta

from .models import Applicant, Document
from .sumsub import Sumsub

LENGTH_OF_STRINGS = 10
DEFAULT_LEVEL_NAME="basic-kyc-level"
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

db= SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route("/")
def hello_world():
    return "<p>Hello, Expedier!</p>"

@app.route("/api/create-applicant", methods=["POST"])
def applicant():
    try:
        if request.method == "POST":
            data = request.get_json()

            first_name = validator(data.get("first_name"))
            last_name = validator(data.get("last_name"))
            email = validator(data.get("email"))
            
            # assumption based
            external_user_id = generate_random_number(LENGTH_OF_STRINGS)
            level_name = DEFAULT_LEVEL_NAME
            applicant_object_id = Sumsub.create_applicant(external_user_id, level_name)

            applicant = Applicant(
                        firstname=first_name,
                        lastname=last_name,
                        email=email,
                        sumsub_id=applicant_object_id,
                        status='pending'
                    )

            db.session.add(applicant)
            db.session.commit()

            applicant =  Applicant.query.filter_by(sumsub_id=applicant_object_id).first()
            return response_message(result=applicant, status=201, message="applicant created")
        
    except ConnectionError as e:
        return response_message(result=e)
    except Exception as b:
        return response_message(b)
 
@app.route("/api/create-token/<:applicant_object_id>", methods=['POST'])
def create_token(applicant_object_id):
    try:
        applicant =  Applicant.query.filter_by(sumsub_id=applicant_object_id).first()
        token = Sumsub.get_access_token(applicant.sumsub_id, level_name=DEFAULT_LEVEL_NAME)
        return response_message(result=token,message="token created")
    except ConnectionError as e:
        return response_message(result=e)   
    

@app.route("/api/add_document/<:applicant_id>", methods=['POST'])
def document_upload(applicant_id):
    # TODO: Technical Debt to upload document and update | add other data parameters
    try:
        request_data= request.data
        applicant =  Applicant.query.filter_by(sumsub_id=applicant_id).first()
        response = Sumsub.add_document(applicant.sumsub_id)

        if applicant:
        # include static files
            document = Document(
                image=request_data['img'], 
                applicant_id= applicant_id,
                verified=response['status']
            )

            db.session.add(document)
            db.session.commit()
            return response_message(result=response,message="Document uploaded created")
    except ConnectionError as e:
        return response_message(result=e)   
        

@app.route("/api/verify_status", methods=['GET'])
def verification_status(applicant_id):
    try:
        applicant =  Applicant.query.filter_by(sumsub_id=applicant_id).first()
        response = Sumsub.get_applicant_status(applicant.sumsub_id)

        document =  Applicant.query.filter_by(applicant_id=applicant.id).first()

        if response:
            return response_message(result=response,message="token created")
    except ConnectionError as e:
        return response_message(result=e)   
        
# helper functions
def generate_random_number(length):
    # Generate a random string of digits (0-9) of given length
    return ''.join(random.choices(string.digits, k=length))


def response_message(message="Ok", status=200, result ={}):
    message = {
        'status': status,
        'message': message,
        'result': result
    }
    return jsonify(message) 


def validator(get_data):
    errors={}
    if len(get_data) ==0:
        return "input is required"
    if '@' not in get_data:
        return "email input is invalid"
    
    return get_data
