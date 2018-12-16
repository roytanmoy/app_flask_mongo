import os
from flask import Flask, request, jsonify, make_response, render_template
from werkzeug.utils import secure_filename
from flask_httpauth import HTTPBasicAuth
from processInput import processUserInput

app = Flask(__name__)

UPLOAD_FOLDER = './upload/'
ALLOWED_EXTENSIONS = set(['csv','json'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

auth = HTTPBasicAuth()
@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'nopass'
    return None
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def upload_file():
   return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_csv():
    submitted_file = request.files['file']
    if submitted_file and allowed_file(submitted_file.filename):
        file = secure_filename(submitted_file.filename)
        if not os.path.exists(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file)
        submitted_file.save(filename)
        op_file_names = process_input(filename)
        out = {
            'status': 'OK',
            'filename': op_file_names,
            'message': "{} saved successful.".format(filename)
            }
        return jsonify(out)
    return render_template('upload.html')

def process_input(file):
    ph_obj = processUserInput(file, process_data=True, storage_type='file')
    return ph_obj.read_from_CSV_File()



if __name__ == "__main__":
    app.run(debug=True)
