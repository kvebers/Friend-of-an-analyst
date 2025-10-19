from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
from db import Video, db, setup_db, add_or_update_video 
import os
from transcript import get_transcript_from_id
from rag import rag
from clasify import predict_label



app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/flaskdb')

setup_db(app)

@app.route("/v1/video", methods=["POST"])
def post_main_video():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "URL is required"}), 400
    url_information = data["url"].strip()
    print(url_information)    
    transcript = get_transcript_from_id(url_information)
    label = predict_label(transcript)    
    add_or_update_video(
        youtube_id=url_information,
        label=label
    )
    return jsonify({"text": label})


@app.route("/v2/video", methods=["POST"])
def post_videos_in_view():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "URL is required"}), 400
    url_information = data["url"].strip()
    video = Video.query.filter_by(youtube_id=url_information).first()
    if video and video.label:
        return jsonify({"text": video.label})
    else:
        return jsonify({"text": "Proceed with caution"})

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
