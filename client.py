import os
import requests
from flask import Flask, request, redirect, url_for, render_template, flash,jsonify
from werkzeug.utils import secure_filename
import use_model
import json

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/catsdogs/')
def upload_form():
	return render_template('upload.html')

@app.route('/upload-image/',methods=['POST'])
def sendit():
	file = request.files['file']
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		final_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		print('./uploads/'+filename)
		files = {'data': open('./uploads/'+filename,'rb')}
		r = requests.post(url = "http://127.0.0.1:5000/cats-dogs/",files=files)
		answer = r.json()
		return render_template("answer.html", filepath=answer)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0',debug=True)
