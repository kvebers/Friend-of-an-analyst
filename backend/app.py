from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
from db import db, setup_db, add_or_update_video 
import os
from transcript import get_transcript_from_id
from rag import rag

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/flaskdb')

setup_db(app)

@app.route("/v1/video", methods=["POST"])
def post_main_video():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "xd'"}), 400
    url_information = data["url"].strip()
    transcript = get_transcript_from_id(url_information)
    print(transcript)
    return jsonify({"text": f"Analysis"})

@app.route("/v2/video", methods=["POST"])
def post_videos_in_view():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "xd'"}), 400
    url_information = data["url"].strip()
    return jsonify({"text": f"Proceed with causion"})

@app.route("/v1/rag", methods=["POST"])
def post_rag():
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "xd'"}), 400
    query = data["prompt"].strip()
    print(query)
    return rag(query=query)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
