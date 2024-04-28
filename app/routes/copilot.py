from flask import Blueprint, request, jsonify
from app.functions.copilot_gen import generate_text
bp = Blueprint('copilot', __name__)

@bp.route('/')
def index():
    key = request.args.get('p')
    if key is None:
        return jsonify({"error": "No prompt provided. Go to /help for more information."})
    
    response = generate_text(key)
    return response