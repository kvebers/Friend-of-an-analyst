from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi


app = Flask(__name__)
CORS(app)


def get_tranctipt_from_id(video_id):
    yt_transcript_api = YouTubeTranscriptApi()
    transcript = yt_transcript_api.fetch(video_id)
    subtitle = ""
    for chunk in transcript:
        subtitle += chunk.text
    return subtitle


@app.route("/v1/video", methods=["POST"])
def get_main_video():
    url_information = request.json.get("url").strip()
    transcript = get_tranctipt_from_id(url_information)
    print(transcript)
    return "Hello " + url_information

@app.route("/v2/video", methods=["POST"])
def get_videos_in_view():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' in request"}), 400
    url_information = data["url"].strip()
    print("Received video ID:", url_information)
    return jsonify({"text": f"Woah Text Was Changed for {url_information}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
