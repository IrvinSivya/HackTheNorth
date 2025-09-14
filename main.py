import os

from flask import Flask, render_template, request, url_for, redirect, jsonify, send_file
from AI import define_text
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

SECRET_KEY = os.getenv("SECRET_KEY")
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/manifest.json')
def serve_manifest():
    return send_file('extensions/manifest.json', mimetype='application/manifest+json')

@app.route("/summarize", methods=['POST'])
def summarize():
    data = request.get_json()

    #Checks if the data is valid and contains the 'text' key
    if not data or "text" not in data:
        return jsonify({"error": "Invalid input"}), 400 #TODO replace jsonify with error page
    
    selected_text = data.get("text", "")

    if not selected_text:
        return jsonify({"error": "No text provided"}), 400 #TODO replace jsonify with error page
    
    defined_text = define_text(selected_text)

    return render_template("popup.html", defined_text = defined_text)

@app.route("/log", methods=["POST","GET"])
def log():
    data = request.get_json()
    print("📌 Selected text:", data.get("selected_text"))
    return "ok", 200

if __name__ == "__main__":
    app.run(debug=True)
