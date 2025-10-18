from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from datetime import datetime
import os


app = Flask(__name__)
CORS(app)

db = SQLAlchemy()

class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    youtube_id = db.Column(db.String(20), unique=True, nullable=False)
    label = db.Column(db.String(50), nullable=True)
    lr = db.Column(db.Float, nullable=True)
    gb = db.Column(db.Float, nullable=True)
    dt = db.Column(db.Float, nullable=True)
    rf = db.Column(db.Float, nullable=True)
    agenda = db.Column(db.String(200), nullable=True)
    sources = db.Column(ARRAY(db.String), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Video {self.youtube_id}>"
    


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/flaskdb')
db = SQLAlchemy(app)


def get_tranctipt_from_id(video_id):
    yt_transcript_api = YouTubeTranscriptApi()
    transcript = yt_transcript_api.fetch(video_id)
    subtitle = ""
    for chunk in transcript:
        subtitle += chunk.text
    return subtitle

@app.route("/v1/video", methods=["POST"])
def get_main_video():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "xd'"}), 400
    url_information = data["url"].strip()
    transcript = get_tranctipt_from_id(url_information)
    print(transcript)
    return jsonify({"text": f"Analysis"})

@app.route("/v2/video", methods=["POST"])
def get_videos_in_view():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "xd'"}), 400
    url_information = data["url"].strip()
    return jsonify({"text": f"Proceed with causion"})

with app.app_context():
    db.create_all()


def add_or_update_video(
    youtube_id: str,
    label: str = None,
    lr: float = None,
    gb: float = None,
    dt: float = None,
    rf: float = None,
    agenda: str = None,
    sources: list[str] = None,
    date_added: datetime = None
):
    if date_added is None:
        date_added = datetime.utcnow()

    with app.app_context():
        video = Video.query.filter_by(youtube_id=youtube_id).first()
        if video:
            if label is not None:
                video.label = label
            if lr is not None:
                video.lr = lr
            if gb is not None:
                video.gb = gb
            if dt is not None:
                video.dt = dt
            if rf is not None:
                video.rf = rf
            if agenda is not None:
                video.agenda = agenda
            if sources is not None:
                video.sources = sources
            video.date_added = date_added
            print(f"Updated existing video {youtube_id}")
        else:
            video = Video(
                youtube_id=youtube_id,
                label=label,
                lr=lr,
                gb=gb,
                dt=dt,
                rf=rf,
                agenda=agenda,
                sources=sources,
                date_added=date_added
            )
            db.session.add(video)
            print(f"Added new video {youtube_id}")

        db.session.commit()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
