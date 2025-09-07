from flask import Flask, request, jsonify
from text_extractor import extract

app = Flask(__name__)

@app.route("/extract", methods=["POST"])
def extract_text():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    try:
        text = extract(url)
        # Optionally clean text with AI here before returning
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)