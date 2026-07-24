import os
from flask import Flask, jsonify
from google.cloud import bigquery

app = Flask(__name__)
client = bigquery.Client()

PROJECT_ID = "johanna-github-insights"
DATASET = "mi_dataset"


@app.route("/")
def home():
    return jsonify({
        "servicio": "github-insights-api",
        "version": "1.1",
        "endpoints": ["/top-lenguajes", "/top-repos", "/lenguajes-en-top-repos"],
    })

@app.route("/top-lenguajes")
def top_lenguajes():
    query = f"""
        SELECT lenguaje, num_repos
        FROM `{PROJECT_ID}.{DATASET}.top_lenguajes`
        ORDER BY num_repos DESC
    """
    rows = client.query(query).result()
    return jsonify([dict(row) for row in rows])


@app.route("/top-repos")
def top_repos():
    query = f"""
        SELECT repo_name, num_files
        FROM `{PROJECT_ID}.{DATASET}.top_repos_archivos`
        ORDER BY num_files DESC
    """
    rows = client.query(query).result()
    return jsonify([dict(row) for row in rows])


@app.route("/lenguajes-en-top-repos")
def lenguajes_en_top_repos():
    query = f"""
        SELECT repo_name, num_files, lenguaje, bytes_lenguaje
        FROM `{PROJECT_ID}.{DATASET}.lenguajes_en_top_repos`
        ORDER BY num_files DESC, bytes_lenguaje DESC
    """
    rows = client.query(query).result()
    return jsonify([dict(row) for row in rows])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
