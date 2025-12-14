import os
from sentence_transformers import SentenceTransformer

_model = None

def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        name = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        _model = SentenceTransformer(name)
    return _model

def embed_text(text: str) -> list[float]:
    m = get_model()
    v = m.encode([text], normalize_embeddings=True)[0]
    return v.tolist()

def canonical_entity_string(card: dict) -> str:
    e = (card.get("entities") or {})
    parts = []
    for k in ["systems", "vendors", "protocols", "ports", "observables"]:
        vals = e.get(k) or []
        vals = [str(x).strip().lower() for x in vals if str(x).strip()]
        vals = sorted(set(vals))
        parts.append(f"{k}:{','.join(vals)}")
    return " | ".join(parts)
