from flask import Flask, Response, json
from werkzeug.exceptions import HTTPException
import traceback
import os
from flask_cors import CORS

def create_app():
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    app.secret_key = 'willbereplacedbyarandomstring'

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, world!'

    # Error Handler
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Return JSON instead of HTML for errors"""

        if(isinstance(e, HTTPException)):
            # start with the correct headers and status code from the error
            response = e.get_response()
            # replace the body with JSON
            response.data = json.dumps({
                "code": e.code,
                "name": e.name,
                "description": e.description,
            })
            response.content_type = "application/json"
        else:
            traceback.print_exc()
            # start with empty response object
            response = Response(status=500)
            # add a JSON body
            response.data = json.dumps({
                "code": 500,
                "name": 'Internal Server Error',
                "description": 'Something Went Wrong',
            })
            response.content_type = "application/json"

        return response

    from . import digitize
    from . import documents
    app.register_blueprint(digitize.digitize)
    app.register_blueprint(documents.documents)
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')

    app.run(host='0.0.0.0')
    
    return app