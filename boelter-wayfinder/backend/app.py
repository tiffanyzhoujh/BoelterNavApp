from flask_cors import CORS
from pathfinder import get_shortest_path, get_floorplans
import os
import io
import zipfile
from flask import Flask, request, send_file, jsonify

app = Flask(__name__)
CORS(app)  # Allow frontend access

@app.route('/api/path', methods=['POST'])
# def compute_path():
#     data = request.get_json()
#     start = data.get('start')
#     dest = data.get('dest')

#     if not start or not des2:
#         return jsonify({'error': 'Missing start or destination'}), 400
    
#     try:
#         path = get_shortest_path(start, dest)
#         return jsonify({'path': path})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
def compute_and_send_zip():
    print("REQUEST RECEIVED")
    data = request.get_json()
    start = data.get('start')
    dest = data.get('dest')

    if not start or not dest:
        return jsonify({'error': 'Missing start or destination'}), 400

    try:
        path = get_shortest_path(start, dest)
        floorplan_files = get_floorplans(path)

        # Create an in-memory ZIP file
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for file_path in floorplan_files:
                filename = os.path.basename(file_path)  # Only use filename inside the ZIP
                zip_file.write(file_path, arcname=filename)

        zip_buffer.seek(0)

        # Send the zip file as HTTP response
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='floorplans.zip'  # What the user sees
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500