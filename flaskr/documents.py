import os

from flask import Blueprint, request, session, Response, abort, jsonify
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson.objectid import ObjectId
import pandas as pd

from . import JSONEncoder

documents = Blueprint('documents', __name__, url_prefix='/documents')

# MongoDB --------------------------------------------------------------------------------------------------
client = MongoClient(os.getenv('DATABASE_URL'))
db = client.digitizer
documentsCollection = db.documents
# ----------------------------------------------------------------------------------------------------------

# Routers funtions ------------------------------------------------------------------------------------------
@documents.route('/', methods=['GET'])
def getDocuments():
    data = [document for document in documentsCollection.find({}, {"fields": 0})]
    return JSONEncoder.JSONEncoder().encode(data)

# Routers funtions ------------------------------------------------------------------------------------------
@documents.route('/<id>', methods=['GET'])
def getDocument(id):
    data = documentsCollection.find_one({"_id": ObjectId(id)})
    return JSONEncoder.JSONEncoder().encode(data)