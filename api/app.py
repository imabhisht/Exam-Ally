from flask import Flask
from flask_cors import CORS
from routes import project_routes
import logging


def configure_logging(app):
    # Set log level
    log_level = logging.DEBUG
    app.logger.setLevel(log_level)

    # Create a stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)

    # Create a formatter and set it for the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(formatter)

    # Add the handler to the logger
    app.logger.addHandler(stream_handler)

app = Flask(__name__)
configure_logging(app)
project_routes(app)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)

