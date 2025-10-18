from flask import Flask, request, jsonify
from transcript import get_tranctipt_from_id

app = Flask(__name__)

@app.route("/v1/video", methods=["GET"])
def get_main_video():
    url_information = request.json.get("url").strip()
    transcript = get_tranctipt_from_id(url_information)
    print(transcript)
    return "Hello " + url_information

@app.route("/v2/video", methods=["GET"])
def get_videos_in_view():
    url_information = request.json.get("url")
    url_information = url_information.strip()
    return "Woah Text Was Changed"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)

