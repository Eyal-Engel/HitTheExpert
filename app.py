from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS data
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL,
                           phone TEXT NOT NULL,
                           category TEXT NOT NULL,
                           responder TEXT NOT NULL,
                           proposal TEXT NOT NULL)''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM data")
        rows = cursor.fetchall()
        data = []
        for row in rows:
            data.append({
                'id': row[0],
                'name': row[1],
                'phone': row[2],
                'category': row[3],
                'responder': row[4],
                'proposal': row[5]
            })
    return jsonify(data)

@app.route('/submit_proposal', methods=['POST'])
def submit_proposal():
    data = request.get_json()
    name = data.get('name')
    phone = data.get('phone')
    category = data.get('category')
    responder = data.get('responder')
    proposal = data.get('proposal')
    
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO data (name, phone, category, responder, proposal) VALUES (?, ?, ?, ?, ?)",
                       (name, phone, category, responder, proposal))
        conn.commit()
    
    return jsonify({'message': 'Data saved successfully!'})

if __name__ == '__main__':
    init_db()
    app.run(port=69, debug=True)
