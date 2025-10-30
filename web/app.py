# web/app.py
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import httpx
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super-secret-key-change-in-prod")  # ADD THIS

API_URL = os.getenv("API_URL", "http://app:8000")

# ------------------------------------------------------------------
# Home – Chat UI
# ------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_msg = request.form["message"].strip()
        if not user_msg:
            return redirect(url_for("index"))

        # Call FastAPI /ask endpoint
        payload = {"query": user_msg}
        try:
            r = httpx.post(f"{API_URL}/ask", json=payload, timeout=30.0)
            r.raise_for_status()
            data = r.json()
            assistant_msg = data["response"]
            context = data.get("context", {})
        except Exception as e:
            assistant_msg = f"Sorry, something went wrong: {e}"
            context = {}

        # Use Flask session
        if "history" not in session:
            session["history"] = []
        session["history"].append({"user": user_msg, "assistant": assistant_msg, "context": context})

        return redirect(url_for("index"))

    history = session.get("history", [])
    return render_template("index.html", history=history)


# ------------------------------------------------------------------
# Upload CSV
# ------------------------------------------------------------------
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".csv"):
            path = "/app/data/sample_expenses.csv"
            file.save(path)
            try:
                httpx.post(f"{API_URL}/ingest", json={"path": "/app/data/sample_expenses.csv"}, timeout=60.0)
                msg = "CSV imported successfully!"
            except Exception as e:
                msg = f"Import failed: {e}"
        else:
            msg = "Please upload a CSV file."
        return render_template("upload.html", message=msg)
    return render_template("upload.html", message="")


# ------------------------------------------------------------------
# Chart
# ------------------------------------------------------------------
@app.route("/chart")
def chart():
    try:
        r = httpx.get(f"{API_URL}/summary", timeout=10.0)
        r.raise_for_status()
        summary = r.json()
    except Exception:
        summary = {}
    return render_template("chart.html", summary=summary)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)