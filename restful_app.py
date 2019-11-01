import os
import use_model
import json
from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

app = Flask(__name__)
api = Api(app)
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['jpg','jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def helloIndex():
    return 'Hello World from Python Flask!'

class CATSDOGS(Resource):
    def post(self):
        print(request.files['data'])
        file = request.files['data']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            final_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print(filename)
            ans = use_model.overall(final_path)
            return {"ANSWER": ans}
        else:
            return {'False'}

api.add_resource(CATSDOGS, '/cats-dogs/')

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)
