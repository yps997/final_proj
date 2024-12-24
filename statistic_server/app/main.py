from flask import Flask
from flask_cors import CORS
from .routs.terror_data_routs import terror_data_blueprint

app = Flask(__name__)
CORS(app)


if __name__ == '__main__':
    app.register_blueprint(terror_data_blueprint, url_prefix='/api')
    app.run(port=5002)