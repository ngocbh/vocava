import os
# import magic
import urllib.request
from server import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from server.services.ocr_image.ocr_v1 import ScanText
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ocr_text = ScanText()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/ocr-image', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        if 'file' not in request.files:
            return {"Null"}
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return {"Null"}
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return ocr_text.get_text(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            return {"Null"}

