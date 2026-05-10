from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)

# SIMPAN DI MEMORY (BUKAN FILE)
visitors = []

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
    visitors.append(visitor)
    return jsonify({'status': 'success', 'visitor': visitor})

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    visitor_id = data.get('id')
    
    for v in visitors:
        if v['id'] == visitor_id and v['status'] == 'active':
            v['checkout'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            v['status'] = 'completed'
            return jsonify({'status': 'success'})
    
    return jsonify({'status': 'error', 'message': 'Visitor not found'})

@app.route('/visitors')
def get_visitors():
    return jsonify(visitors)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
