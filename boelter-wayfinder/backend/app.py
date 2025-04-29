from flask_cors import CORS
from pathfinder import get_shortest_path, get_floorplans
import os
import io
import zipfile
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)
CORS(app)  # Allow frontend access


import uuid
import shutil

@app.route('/api/path', methods=['POST'])
def compute_and_send_zip():
    data = request.get_json()
    start = data.get('start')
    dest = data.get('dest')

    if not start or not dest:
        return jsonify({'error': 'Missing start or destination'}), 400

    try:
        path = get_shortest_path(start, dest)

        # Create a unique temp folder for this request
        temp_folder = f"temp_output/{uuid.uuid4().hex}"
        os.makedirs(temp_folder, exist_ok=True)

        # Generate the floorplans into this temp folder
        floorplan_files = get_floorplans(path, temp_folder)

        # Create an in-memory ZIP file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for file_path in floorplan_files:
                filename = os.path.basename(file_path)
                zip_file.write(file_path, arcname=filename)

        zip_buffer.seek(0)

        # Clean up the temporary folder
        shutil.rmtree(temp_folder)

        # Send the zip file
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='floorplans.zip'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500
