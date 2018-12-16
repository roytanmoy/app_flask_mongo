import os
from flask import Flask, request, jsonify, make_response, abort, render_template, url_for, send_file, send_from_directory
from werkzeug.utils import secure_filename
from flask_httpauth import HTTPBasicAuth
from processInput import processUserInput
from validation import validatePhoneNumber

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
@auth.login_required
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
        return jsonify({'output':for_public_data(out)})
    return render_template('upload.html')

def for_public_data(out):
    new_out = {}
    for field in out:
        if field == 'filename':
            new_out['uri'] = [url_for('upload_csv', filename=fname, _external=True) for fname in out[field]]
        else:
            new_out[field] = out[field]
    return new_out

@app.route('/phnumbers/status/<phonenumber>',  methods=['GET'])
@auth.login_required
def phnumber_status(phonenumber):
    return jsonify(get_phnumber_status(phonenumber))

@app.route('/phnumbers/file_status/<file_name>',  methods=['GET'])
@auth.login_required
def return_file(file_name):
    if get_files(file_name):
        return send_file(UPLOAD_FOLDER+file_name)
    else:
        abort(404)

def get_files(fname = None):
    fnames = [file for file in os.listdir(UPLOAD_FOLDER)]
    if fname:
        return fname in fnames
    else:
        return fnames

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def process_input(file):
    ph_obj = processUserInput(file, process_data=True, storage_type='file')
    return ph_obj.read_from_CSV_File()

def get_phnumber_status(phnumber):
    val_obj = validatePhoneNumber(countryCode="ZA")
    return val_obj.validate_number(phnumber)


if __name__ == "__main__":
    app.run(debug=True)