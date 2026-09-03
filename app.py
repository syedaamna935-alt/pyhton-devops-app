from flask import Flask
import redis
import psycopg2
import os

app = Flask(__name__)

# Redis Connection
cache = redis.Redis(host='redis', port=6379)

# PostgreSQL Connection
def get_db_connection():
    conn = psycopg2.connect(
        host='db',
        database=os.environ.get('POSTGRES_DB', 'mydb'),
        user=os.environ.get('POSTGRES_USER', 'myuser'),
        password=os.environ.get('POSTGRES_PASSWORD', 'mypassword')
    )
    return conn

@app.route('/')
def hello():
    # 1. Redis Cache Update
    count = cache.incr('hits')

    # 2. PostgreSQL Permanent Store
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, count INT);')
        cur.execute('INSERT INTO visits (count) VALUES (%s);', (count,))
        conn.commit()
        cur.close()
        conn.close()
        db_status = "Successfully logged to PostgreSQL!"
    except Exception as e:
        db_status = f"DB Error: {str(e)}"

    return f"Hello World! I have been seen {count} times.\nPostgreSQL Status: {db_status}\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)