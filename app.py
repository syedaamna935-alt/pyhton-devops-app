from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hello from Python Flask App!</h1><p>Main Docker aur Python seekh rahi hun</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)