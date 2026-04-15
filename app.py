from flask import Flask, render_template, request, jsonify
import os
import time
import subprocess

app = Flask(__name__)

# Ensure directories exist
UPLOAD_FOLDER = os.path.join("static", "uploads")
OUTPUT_FOLDER = os.path.join("static", "detected")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Add host validation
ALLOWED_HOSTS = [h for h in os.environ.get("ALLOWED_HOSTS", "").split(",") if h]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/detect", methods=["POST"])
def detect():
    try:
        file = request.files["image"]

        filename = f"img_{int(time.time())}.jpg"
        input_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, filename))

        file.save(input_path)

        # Run YOLOv3
        # Use python3 to ensure the same environment
        subprocess.run([
            "python3", "yolo.py",
            "--image", input_path.replace("\\", "/")
        ], check=True)
        time.sleep(0.5)

        return jsonify({
            "input": f"/{UPLOAD_FOLDER}/{filename}",
            "output": f"/static/detected/output.jpg?t={int(time.time())}"
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    # Standard Flask port for development; gunicorn will override this
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
