from src import db
import datetime
from hmac import compare_digest


class Applicant(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=True)
    lastname = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    sumsub_id = db.Column(db.String(80), nullable=False)
    date_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow())

class Document(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    applicant_id = db.Column(db.Integer, db.ForeignKey("applicants.id"), nullable=False)
    document_type = db.Column(db.String(20), nullable=True)
    verified = db.Column(db.String(50), unique=True, nullable=True)
    sumsub_id = db.Column(db.String(80), nullable=False)
    date_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow())
