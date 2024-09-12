from flask import Flask, request, jsonify
import os
from filehash import FileHash
from flask_cors import CORS
hashes = ["ab978e278dd2acd0894f191d89a93ebd", "656c0ca99a46cfadaeafa6053779e8b4"]
app = Flask(__name__)
CORS(app)
# Set upload folder
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
md5hasher = FileHash("md5")

# Create the upload directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and file.filename.endswith('.pdf'):
        # Save the file temporarily to the upload folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        print(file_path)
        # Now hash the file using its path
        hashed = md5hasher.hash_file(file_path)

        # Check if the hash matches any in the list
        if hashed in hashes:
            return jsonify({'message': 'File successfully uploaded'}), 200
        else:
            # Optionally, remove the file if the hash doesn't match
            os.remove(file_path)
            return jsonify({'message': 'File hash does not match'}), 400
    else:
        return jsonify({'message': 'Only PDF files are allowed'}), 400

if __name__ == "__main__":
    app.run(debug=True)
