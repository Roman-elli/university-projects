import logging

from flask import Flask
from flask_cors import CORS
from config import Config
from routes import init_routes

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    @app.route('/')
    def landing_page():
        return """
        Hello Teacher (Python Native)!  <br/>
        <br/>
        Main page of the Project!<br/>
        <br/>
        BD 2023-2024 Team<br/>
        <br/>
        """
    init_routes(app)

    return app

if __name__ == '__main__':
    logging.basicConfig(
        filename='log_file.log',
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s]:  %(message)s',
        datefmt='%H:%M:%S'
    )

    app = create_app()
    host = '127.0.0.1'
    port = 8080
    app.run(host=host, port=port, debug=True, threaded=True)
    logging.info(f'API v1.0 online: http://{host}:{port}')

