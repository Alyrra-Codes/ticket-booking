from flask import Flask 
from flask import jsonify

import sqlite3

app = Flask(__name__)

def create_database():
  conn = sqlite3.connect('todo.db')
  c = conn.cursor()
  c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)''')
  conn.commit()
  conn.close()
    
@app.route('/hello', methods=['GET'])
def hello():
  return jsonify({'message': 'Hello, World!'})


if __name__ == '__main__':
  create_database()
  app.run(host='0.0.0.0', port=5000, use_reloader=True)