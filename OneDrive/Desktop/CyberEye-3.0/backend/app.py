from flask import Flask, request, jsonify
from flask_cors import CORS
from model import classify_url
from db import init_db, save_scan, get_scan_history


app = Flask(__name__)
CORS(app)

@app.route("/api/classify", methods=["POST"])
def classify():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    category, reason = classify_url(url)

    # Save to DB
    save_scan(url, category, reason)

    return jsonify({
        "url": url,
        "category": category,
        "reason": reason
    })

@app.route("/api/history", methods=["GET"])
def history():
    scans = get_scan_history()
    history = [
        {
            "id": row[0],
            "url": row[1],
            "category": row[2],
            "reason": row[3],
            "scanned_at": row[4]
        }
        for row in scans
    ]
    return jsonify(history)




if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
