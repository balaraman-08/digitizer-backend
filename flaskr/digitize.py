import os
import json
from datetime import datetime

from flask import Blueprint, request, session, Response, abort, jsonify
from werkzeug.utils import secure_filename
from pymongo import MongoClient
import pandas as pd

from . import extract
from . import JSONEncoder

digitize = Blueprint('digitize', __name__, url_prefix='/digitize')

# MongoDB --------------------------------------------------------------------------------------------------
client = MongoClient(os.getenv('DATABASE_URL'))
db = client.digitizer
documentsCollection = db.documents
# ----------------------------------------------------------------------------------------------------------

# Utilty funtions ------------------------------------------------------------------------------------------
def format_data(raw_data: pd.DataFrame, filename: str):
    formatted_data = {
        "filename": filename,
        "fields": [],
        "status": "extracted"
    }
    for idx, row in raw_data.iterrows():
        if row["text"].strip() != "":
            formatted_data["fields"].append({
                "extractedText": row["text"].strip(),
                "correctedText": row["text"].strip(),
                "conf": row["conf"],
                "bounding_box": {
                    "top": row["top"],
                    "left": row["left"],
                    "width": row["width"],
                    "width": row["width"]
                }
            })
    formatted_data["timestamp"] = int(datetime.now().timestamp() * 1000)
    return formatted_data

# ----------------------------------------------------------------------------------------------------------

# Routers funtions ------------------------------------------------------------------------------------------
@digitize.route('/', methods=['GET'])
def upload():
    return  '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@digitize.route('/', methods=['POST'])
def upload_and_extract():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(os.getenv('UPLOAD_FOLDER'), filename))
        data = extract.extract_data(os.path.join(os.getenv('UPLOAD_FOLDER'), filename))
        formatted_data = format_data(data, filename)
        documentsCollection.insert_one(formatted_data)
        return JSONEncoder.JSONEncoder().encode(formatted_data)

# ----------------------------------------------------------------------------------------------------------