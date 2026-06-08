from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return {"status": "ok"}

@app.route('/health')
def health():
    return {"status": "healthy"}

if __name__ == '__main__':
    print("Starting Flask on port 5005...")
    app.run(host='0.0.0.0', port=5005, debug=False)
