from .db import db

class UploadRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    file_path = db.Column(db.String(120), nullable=False)
    upload_time = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Numeric(20, 2), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ocr_result = db.Column(db.Text, nullable=False)