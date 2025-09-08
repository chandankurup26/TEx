from flask import Flask, request, jsonify
from text_extractor import extract
from google import genai

app = Flask(__name__)

@app.route('/', methods=['POST'])
def extract_and_clean():
    data = request.get_json()
    url = data.get('website')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        raw_text = extract(url)

        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Clean the given text by removing unnecessary symbols or formatting, then convert it into a properly structured title and paragraph format: {raw_text}"
        )

        return jsonify({'cleaned_text': response.text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500