from flask import Flask, render_template, request, jsonify
from arxiv_api import fetch_papers, get_topics
from models import summarize, PROVIDERS

app = Flask(__name__)
@app.route("/")
def index():
    return render_template(
        "index.html",
        topics=get_topics(),
        providers=PROVIDERS,
    )
@app.route("/api/papers")
def api_papers():
    topic = request.args.get("topic", "cs.AI")
    n     = int(request.args.get("n", 10))

    try:
        papers = fetch_papers(topic_code=topic, n=n)
        return jsonify({"ok": True, "papers": papers})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500
@app.route("/api/summarize", methods=["POST"])
def api_summarize():
    body        = request.json or {}
    provider_id = body.get("provider", "groq")
    title       = body.get("title", "")
    abstract    = body.get("abstract", "")

    if not title or not abstract:
        return jsonify({"ok": False, "error": "title and abstract are required"}), 400

    try:
        summary = summarize(
            provider_id=provider_id,
            title=title,
            abstract=abstract,
        )
        return jsonify({"ok": True, "summary": summary})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

@app.route("/api/providers")
def api_providers():
    safe = {
        pid: {k: v for k, v in cfg.items() if k != "secret"}
        for pid, cfg in PROVIDERS.items()
    }
    return jsonify(safe)

if __name__ == "__main__":
    app.run(debug=True, port=5000)