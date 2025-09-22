import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from bs4 import BeautifulSoup
import requests
import google.generativeai as genai

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# --- Flask and DB Setup ---
app = Flask(__name__)
CORS(app)  # allow frontend JS access

# Connect to Neon DB using env var
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL_ENV_VAR", "")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# --- Database Model ---
class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)

# --- Text Extraction ---
def extract(url):
    full_text = ""
    text_parts = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    headers = soup.find_all("h1")
    paragraphs = soup.find_all("p")

    for header in headers:
        text_parts.append(header.get_text())
    for paragraph in paragraphs:
        text_parts.append(paragraph.get_text())

    full_text = "\n".join(text_parts)
    return full_text

# --- Text Cleaning Using Gemini ---
def clean_text_with_gemini(txt):
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Clean the given text by removing unnecessary symbols or formatting, then convert it into a properly structured title and paragraph format: {txt}"
    )
    return response.text

# --- API Route to Extract, Clean, and Store ---
@app.route('/responses', methods=['POST'])
def add_response():
    data = request.get_json()
    if 'link' not in data:
        return jsonify({'error': 'Missing link'}), 400

    try:
        raw_text = extract(data['link'])
        cleaned_text = clean_text_with_gemini(raw_text)

        new_response = Response(text=cleaned_text)
        db.session.add(new_response)
        db.session.commit()

        return jsonify({'message': 'Response added successfully', 'output': cleaned_text}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- Get Latest Response ---
@app.route('/responses/latest', methods=['GET'])
def get_latest_response():
    latest = Response.query.order_by(Response.id.desc()).first()
    if not latest:
        return jsonify({'output': 'No data available'}), 404
    return jsonify({'output': latest.text}), 200

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # ensure tables are created

    port = int(os.environ.get("PORT", 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
