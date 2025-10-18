
from flask import Flask, request, jsonify

app = Flask(__name__)
@app.route("/v1/video", methods=["POST"])
def get_query_and_return_embeding():
    query = request.json.get("url")
    query = query.strip()
    process_data = {
        
    }
    return "Hello " + query


@app.route("/v2/video", methods=["POST"])
def get_query_and_return_embeding():
    query = request.json.get("url")
    query = query.strip()
    return "Hello " + query

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)

