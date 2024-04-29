from flask import Flask
from routes.copilot import bp

def project_routes(app):
    app.register_blueprint(bp, url_prefix='/copilot')

    return app