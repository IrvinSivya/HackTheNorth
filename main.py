import os

from flask import Flask, render_template, request, url_for, redirect, jsonify, send_file
from AI import define_text, detailed_explanation, diagram_text
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

SECRET_KEY = os.getenv("SECRET_KEY")
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/manifest.json')
def serve_manifest():
    return send_file('extensions/manifest.json', mimetype='application/manifest+json')

@app.route("/explain", methods=["POST"])
def explain():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Invalid input"}), 400

    selected_text = data.get("text", "")
    mode = data.get("mode", "simplified")  # default is simplified

    if not selected_text:
        return jsonify({"error": "No text provided"}), 400

    print(f"Selected text: {selected_text}, Mode: {mode}")

    # Call different AI functions depending on mode
    if mode == "simplified":
        reply = define_text(selected_text)
    elif mode == "detailed":
        reply = detailed_explanation(selected_text)
    elif mode == "diagrams":
        reply = diagram_text(selected_text)
    else:
        reply = "Unknown mode."

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)

