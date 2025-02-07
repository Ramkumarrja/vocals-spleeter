from flask import Flask, request, jsonify
import os
from spleeter.separator import Separator

app = Flask(__name__)
separator = Separator('spleeter:2stems')  # Use the 2-stem model


@app.route('/', methods=['GET'])
def server_checking():
    print("Server is running...")
    return jsonify({"message":"server running"})


@app.route('/process', methods=['POST'])
def process_audio():
    print("Processing audio...")
    
    if 'file' not in request.files:
        print("Error: No file provided")
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    filename = file.filename
    input_path = os.path.join('/tmp', filename)
    output_path = '/tmp/output'

    print(f"Received file: {filename}")
    print(f"Saving file to: {input_path}")
    file.save(input_path)
    
    print(f"Starting separation on file: {input_path}")
    separator.separate_to_file(input_path, output_path)

    print(f"Processing complete. Output saved at: {output_path}")
    return jsonify({'message': 'Processing complete', 'output_path': output_path}), 200

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=5000)
