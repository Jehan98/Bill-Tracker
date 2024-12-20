from datetime import datetime
import os
from flask import Blueprint, jsonify,redirect, render_template, request, send_from_directory, url_for
from sqlalchemy import extract, func
import vertexai
from vertexai.generative_models import GenerativeModel

from inference import process_document
from utils import extract_json
from db_module.db import db
from db_module.models import UploadRecord

PROJECT_ID = "empirical-oven-442516-n0"
LOCATION = "us"
PROCESSOR_ID = "5f8679dd0aa41ff3"
HEADER_TEXT   = "This is a text extracted from a bill. I want to get the total amount of the bill and the category it belongs to among these food, travel, health, utility, other. I want the output in json format as example {'amount': 230, 'category': 'food'}. Follwoing is the text extracted from the bill: "
SUMMERIZE_HEADER_TEXT = "This is a text extracted from a bill. Give a small description on where and for that money is spent in the format as in example: 'Cloths from ABC clothing shop on 2024-05-22'. Follwoing is the text extracted from the bill: "

vertexai.init(project=PROJECT_ID, location="us-central1")
model = GenerativeModel("gemini-1.5-flash-002")

routes = Blueprint('routes', __name__)

@routes.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)
        if file:
            file_path = os.path.join("uploads", file.filename)
            file.save(file_path)
            
            document = process_document(
                project_id=PROJECT_ID,
                location=LOCATION,
                processor_id=PROCESSOR_ID,
                file_path=file_path,
                mime_type='image/jpeg',
            )
            bill_text = document.text

            response = model.generate_content(HEADER_TEXT + bill_text)
            print("response.text", response.text)

            json_response = extract_json(response.text)[0]
            bill_amount = json_response["amount"]
            bill_category = json_response["category"]
            print(json_response)

            detail_response = model.generate_content(SUMMERIZE_HEADER_TEXT + bill_text)
            new_record = UploadRecord(filename=file.filename, file_path=file_path, category=bill_category, amount=bill_amount, upload_time=datetime.now().replace(microsecond=0), ocr_result=bill_text, description=detail_response.text)
            db.session.add(new_record)
            db.session.commit()

            return redirect(request.url)
    
        return redirect(request.url)

    records = UploadRecord.query.all()
    current_month = datetime.now().month
    current_year = datetime.now().year

    records = UploadRecord.query.filter(
        extract('month', UploadRecord.upload_time) == current_month,
        extract('year', UploadRecord.upload_time) == current_year
    ).all()
    return render_template("index.html", records=records)

@routes.route('/uploads/<filename>')
def serve_image(filename):
    return send_from_directory('uploads', filename)

@routes.route("/clearall",  methods=["POST"])
def clear_all():
    db.session.query(UploadRecord).delete()
    db.session.commit()
    records = UploadRecord.query.all()
    return redirect(url_for('routes.index'))

@routes.route('/api/expenses-by-category', methods=['GET'])
def get_expenses_by_category():
    data = (
        db.session.query(
            UploadRecord.category, func.sum(UploadRecord.amount).label('total_amount')
        )
        .group_by(UploadRecord.category)
        .all()
    )
    result = {category: float(amount) for category, amount in data}
    return jsonify(result)

@routes.route("/api/update-record/<int:id>", methods=["POST"])
def update_record(id):
    data = request.json
    category = data.get('category')
    amount = data.get('amount')
    description = data.get('description')

    record = UploadRecord.query.get(id)
    if not record:
        return {"error": "Record not found"}, 404

    try:
        record.category = category
        record.amount = float(amount)
        record.description = description
        db.session.commit()
        return {"message": "Record updated successfully"}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500