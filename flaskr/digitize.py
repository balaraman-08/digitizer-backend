from flask import Blueprint, request, session, Response, abort, jsonify
from werkzeug.utils import secure_filename
import os
from . import extract

digitize = Blueprint('digitize', __name__, url_prefix='/digitize')

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
        return jsonify(data=extract.extract_data(os.path.join(os.getenv('UPLOAD_FOLDER'), filename)))