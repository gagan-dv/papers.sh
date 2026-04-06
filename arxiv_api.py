import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import ssl
import certifi

NS = "http://www.w3.org/2005/Atom"
ARXIV_API_URL = "https://export.arxiv.org/api/query"

TOPICS = {
    "cs.AI":   "AI",
    "cs.LG":   "Machine Learning",
    "cs.CV":   "Computer Vision",
    "cs.CL":   "NLP",
    "cs.RO":   "Robotics",
    "stat.ML": "Stats ML",
    "cs.SY":   "Systems",
    "cs.CR":   "Security",
    "cs.NE":   "Neural & Evolutionary",
    "cs.IR":   "Information Retrieval",
}


SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())

def _clean(text: str) -> str:
    return (text or "").strip().replace("\n", " ")


def _parse_entry(entry) -> dict:
    title     = _clean(entry.findtext(f"{{{NS}}}title"))
    abstract  = _clean(entry.findtext(f"{{{NS}}}summary"))
    link      = _clean(entry.findtext(f"{{{NS}}}id"))
    published = _clean(entry.findtext(f"{{{NS}}}published"))
    authors = [
        _clean(a.findtext(f"{{{NS}}}name"))
        for a in entry.findall(f"{{{NS}}}author")
    ]

    return {
        "title":     title,
        "abstract":  abstract,
        "authors":   authors[:4],
        "link":      link,
        "published": published[:10],
    }

def fetch_papers(topic_code: str, n: int = 10) -> list[dict]:
    n = min(n, 20)
    if topic_code not in TOPICS:
        raise ValueError(f"Unknown topic: {topic_code}")
    params = urllib.parse.urlencode({
        "search_query": f"cat:{topic_code}",
        "sortBy":       "submittedDate",
        "sortOrder":    "descending",
        "max_results":  n,
    })
    url = f"{ARXIV_API_URL}?{params}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    try:
        with urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=15) as response:
            raw = response.read()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch arXiv data: {repr(e)}")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        raise RuntimeError("Invalid XML response from arXiv")

    entries = root.findall(f"{{{NS}}}entry")

    papers = []
    for entry in entries:
        try:
            paper = _parse_entry(entry)
            paper["topic"] = TOPICS[topic_code]
            paper["topic_code"] = topic_code
            papers.append(paper)
        except Exception:
            continue

    return papers

def get_topics() -> dict:
    return TOPICS