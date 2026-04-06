# papers.sh
A small web app that pulls the latest AI/ML papers from arXiv and gives quick summaries using different LLM providers. Basically turns long abstracts into something you can scan in seconds. Not fancy, just useful.

## Features
- Browse papers by topic (AI, ML, CV, NLP, etc.)
- Get short AI-generated summaries
- Switch between models (Groq, Gemini, OpenRouter)
  
## Example usage
Open the app, pick a topic, hit fetch, scroll.
You’ll see papers one by one with a short summary. If it looks interesting, open the full paper. If not, move on.

## Running locally
```bash
pip install -r requirements.txt
python app.py
