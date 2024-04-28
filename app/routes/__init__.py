from flask import Flask
from app.routes.copilot import bp as copilot_bp

def project_routes(app):
    app.register_blueprint(copilot_bp, url_prefix='/copilot')

    return app