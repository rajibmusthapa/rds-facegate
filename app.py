from flask import Flask, render_template, request, jsonify
import json
import datetime
import os

app = Flask(__name__)

# File database
DATA_FILE = 'visitors.json'

# Inisialisasi file
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/checkin', methods=['POST'])
def checkin():
    data = request.json
    visitor = {
        'id': datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        'nama': data.get('nama'),
        'checkin': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'checkout': None,
        'status': 'active'
    }
    
    with open(DATA_FILE, 'r') as f:
        visitors = json.load(f)
    
    visitors.append(visitor)
    
    with open(DATA_FILE, 'w') as f:
        json.dump(visitors, f, indent=2)
    
    return jsonify({'status': 'success', 'visitor': visitor})

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    visitor_id = data.get('id')
    
    with open(DATA_FILE, 'r') as f:
        visitors = json.load(f)
    
    for v in visitors:
        if v['id'] == visitor_id and v['status'] == 'active':
            v['checkout'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            v['status'] = 'completed'
            
            with open(DATA_FILE, 'w') as f:
                json.dump(visitors, f, indent=2)
            
            return jsonify({'status': 'success'})
    
    return jsonify({'status': 'error', 'message': 'Visitor not found'})

@app.route('/visitors')
def get_visitors():
    with open(DATA_FILE, 'r') as f:
        visitors = json.load(f)
    return jsonify(visitors)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)