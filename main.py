import os

from flask import Flask, render_template, request, url_for, redirect, jsonify, send_file
from AIResponses import summarize_text

app = Flask(__name__)

SECRET_KEY = os.getenv("SECRET_KEY")
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

@app.route("/summarize", methods=['POST'])
def summarize():
    data = request.get_json()

    #Checks if the data is valid and contains the 'text' key
    if not data or "text" not in data:
        return jsonify({"error": "Invalid input"}), 400 #TODO reaplce jsonify with error page
    
    selected_text = data.get("text", "")

    if not selected_text:
        return jsonify({"error": "No text provided"}), 400 #TODO reaplce jsonify with error page
    
    summarized_text = summarize_text(selected_text)

    return render_template("summary.html", summarized_text=summarized_text)

if __name__ == "__main__":
    app.run(debug=True)
