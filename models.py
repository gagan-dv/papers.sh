from dotenv import load_dotenv
load_dotenv()
import os
os.getenv("GROQ_API_KEY")
os.getenv("GEMINI_API_KEY")
os.getenv("OPENROUTER_API_KEY")
PROVIDERS = {
    "groq": {
        "id": "groq",
        "label": "Groq Llama 3.3 70B (Free)",
        "model": "llama-3.3-70b-versatile",
        "secret": "GROQ_API_KEY",
        "free": True,
        "limit": "14,400 req/day free",
        "docs": "https://console.groq.com",
    },
    "gemini": {
        "id": "gemini",
        "label": "Google Gemini 2.0 Flash (Free)",
        "model": "gemini-2.0-flash",
        "secret": "GEMINI_API_KEY",
        "free": True,
        "limit": "500 req/day free",
        "docs": "https://aistudio.google.com",
    },
    "openrouter": {
        "id": "openrouter",
        "label": "OpenRouter Llama 3.3 70B (Free tier)",
        "model": "meta-llama/llama-3.3-70b-instruct:free",
        "secret": "OPENROUTER_API_KEY",
        "free": True,
        "limit": "50 req/day free",
        "docs": "https://openrouter.ai",
    },
}

def build_prompt(title: str, abstract: str) -> str:
    return (
        "Summarize this ML/AI paper in 2-3 plain English sentences. "
        "Focus on what is new and why it matters.\n\n"
        f"Title: {title}\n"
        f"Abstract: {abstract}"
    )

def summarize_groq(api_key: str, model: str, prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
    res = client.chat.completions.create(
        model=model,
        max_tokens=220,
        messages=[{"role": "user", "content": prompt}],
    )
    return res.choices[0].message.content


def summarize_gemini(api_key: str, model: str, prompt: str) -> str:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    gemini = genai.GenerativeModel(model)
    res = gemini.generate_content(prompt)
    return res.candidates[0].content.parts[0].text


def summarize_openrouter(api_key: str, model: str, prompt: str) -> str:
    from openai import OpenAI
    client = OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers={"HTTP-Referer": "https://arxiv-flashcards.app"},
    )
    res = client.chat.completions.create(
        model=model,
        max_tokens=220,
        messages=[{"role": "user", "content": prompt}],
    )
    return res.choices[0].message.content


SUMMARIZERS = {
    "groq": summarize_groq,
    "gemini": summarize_gemini,
    "openrouter": summarize_openrouter,
}


def summarize(provider_id: str, title: str, abstract: str) -> str:

    if provider_id not in PROVIDERS:
        raise ValueError(f"Unknown provider: {provider_id}")

    if provider_id not in SUMMARIZERS:
        raise ValueError(f"No summarizer implemented for: {provider_id}")

    provider = PROVIDERS[provider_id]

    api_key = os.getenv(provider["secret"])
    if not api_key:
        raise ValueError(
            f"Missing API key for {provider_id} (env: {provider['secret']})"
        )

    model  = provider["model"]
    prompt = build_prompt(title, abstract)
    fn     = SUMMARIZERS[provider_id]

    return fn(api_key, model, prompt)

