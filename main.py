from flask import Flask
from flask_cors import CORS
from controller.counter_controller import counter_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(counter_bp, url_prefix='/erkai/visualnet')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)