import os
from flask import Flask, redirect, request, render_template, send_file
from storage import upload_file, get_list_of_files, download_file

app = Flask(__name__)

# Replace with your Google Cloud Storage bucket name
BUCKET_NAME = 'my-bucket-for-project'

@app.route('/')
def index():
    # Get files from the bucket and pass them to the template
    files = get_list_of_files(BUCKET_NAME)
    return render_template("index.html", files=files)

@app.route('/upload', methods=["POST"])
def upload():
    # Handle file upload
    if 'form_file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['form_file']
    if file.filename == '':
        return 'No selected file', 400

    # Save file locally first (optional, but required for GCS upload)
    temp_path = os.path.join('/tmp', file.filename)
    file.save(temp_path)

    # Upload file to GCS
    upload_file(BUCKET_NAME, temp_path)

    # Remove local temporary file
    os.remove(temp_path)

    return redirect("/")

@app.route('/files/<filename>')
def get_file(filename):
    # Allow user to download/view file
    temp_path = os.path.join('/tmp', filename)
    download_file(BUCKET_NAME, filename)

    return send_file(temp_path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
