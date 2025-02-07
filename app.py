from flask import Flask, request, jsonify
import os
from spleeter.separator import Separator

app = Flask(__name__)
separator = Separator('spleeter:2stems')  # Use the 2-stem model

@app.route('/process', methods=['POST'])
def process_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    filename = file.filename
    input_path = os.path.join('/tmp', filename)
    output_path = '/tmp/output'

    file.save(input_path)
    separator.separate_to_file(input_path, output_path)

    return jsonify({'message': 'Processing complete', 'output_path': output_path}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
