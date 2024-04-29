from flask import Flask
from routes import copilot_bp_fun

def project_routes(app):
    app.register_blueprint(copilot_bp_fun.copilot_bp, url_prefix='/copilot')

    return app