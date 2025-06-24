import os
from flask import Flask, request, jsonify, send_from_directory
import subprocess
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'exe'}

app = Flask(__name__, static_folder='public', template_folder='public')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/run', methods=['POST'])
def run_exe():
    if 'exe' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['exe']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400
    filename = secure_filename(file.filename)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # Windowsネイティブで実行
        result = subprocess.run(
            [filepath], capture_output=True, text=True, timeout=60, shell=True
        )
        return jsonify({
            'exitCode': result.returncode,
            'output': result.stdout + result.stderr
        })
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Execution timed out'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
