from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics

import psycopg2
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        database=os.environ.get("DB_NAME", "users_db"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", "postgres")
    )
    return conn

@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        );
    ''')
    conn.commit()
    cur.execute('SELECT id, name FROM users;')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)


@app.route('/users', methods=['POST'])
def add_user():
    name = request.json['name']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (name) VALUES (%s) RETURNING id;', (name,))
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'id': user_id, 'name': name}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
