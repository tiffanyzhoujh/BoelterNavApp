from flask import Flask, request, jsonify
from flask_cors import CORS
from pathfinder import get_shortest_path  # your function to compute path

app = Flask(__name__)
CORS(app)  # Allow frontend access

@app.route('/api/path', methods=['POST'])
def compute_path():
    data = request.get_json()
    start = data.get('start')
    dest = data.get('dest')

    if not start or not dest:
        return jsonify({'error': 'Missing start or destination'}), 400
    
    try:
        path = get_shortest_path(start, dest)
        return jsonify({'path': path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
