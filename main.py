import os
import aiohttp
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from dotenv import load_dotenv

from .schemas import IngestResponse, SearchRequest, SearchResponse, Match, IncidentCard
from .storage import save_upload
from .vision import extract_incident_card_from_image
from .embedder import embed_text, canonical_entity_string, get_model
from .scoring import overlap_score, build_why_matched, combine_scores, severity_rank
from .qdrant_store import get_qdrant, ensure_collection

load_dotenv()

app = FastAPI(title="Visual Incident Intelligence")

client = get_qdrant()
SEM_COL = os.getenv("SEMANTIC_COLLECTION", "incidents_semantic")
ENT_COL = os.getenv("ENTITIES_COLLECTION", "incidents_entities")

_dim = len(get_model().encode(["dim"], normalize_embeddings=True)[0])
ensure_collection(client, SEM_COL, _dim)
ensure_collection(client, ENT_COL, _dim)

@app.get("/", include_in_schema=False)
def ui():
    return FileResponse("ui/index.html")

@app.get("/health")
async def health():
    api_ok = True
    qdrant_ok = False
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333").rstrip("/")
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(f"{qdrant_url}/collections", timeout=2) as r:
                qdrant_ok = (r.status == 200)
    except Exception:
        qdrant_ok = False
    return {"api_ok": api_ok, "qdrant_ok": qdrant_ok, "dim": _dim}

@app.post("/ingest", response_model=IngestResponse)
async def ingest(file: UploadFile = File(...), note: str = Form(default="")):
    incident_id, path = save_upload(file.file, file.filename)
    card = extract_incident_card_from_image(path, note)
    card_dict = card.model_dump()

    semantic_text = f"{card.summary}\nSymptoms: {', '.join(card.symptoms)}\nHypotheses: {', '.join(card.hypotheses)}"
    entities_text = canonical_entity_string(card_dict)

    v_sem = embed_text(semantic_text)
    v_ent = embed_text(entities_text)

    payload = {
        "incident_id": incident_id,
        "incident_card": card_dict,
        "severity": card.severity_guess,
        "asset_type": card.asset_type,
        "image_path": path,
    }

    client.upsert(collection_name=SEM_COL, points=[{"id": incident_id, "vector": v_sem, "payload": payload}])
    client.upsert(collection_name=ENT_COL, points=[{"id": incident_id, "vector": v_ent, "payload": payload}])

    return IngestResponse(incident_id=incident_id, incident_card=card)

@app.post("/search", response_model=SearchResponse)
async def search(req: SearchRequest):
    points = client.retrieve(collection_name=SEM_COL, ids=[req.incident_id], with_payload=True, with_vectors=False)
    if not points:
        raise HTTPException(status_code=404, detail="Incident not found. Ingest something first.")

    q_card = points[0].payload["incident_card"]
    semantic_text = f"{q_card.get('summary','')}\nSymptoms: {', '.join(q_card.get('symptoms', []))}\nHypotheses: {', '.join(q_card.get('hypotheses', []))}"
    q_vec = embed_text(semantic_text)

    hits = client.search(collection_name=SEM_COL, query_vector=q_vec, limit=max(req.top_k * 6, 30), with_payload=True)

    matches = []
    for h in hits:
        if str(h.id) == req.incident_id:
            continue
        cand = h.payload
        c_card = cand["incident_card"]

        if req.min_severity and severity_rank(cand.get("severity","unknown")) < severity_rank(req.min_severity):
            continue

        ov = overlap_score(q_card, c_card)
        why = build_why_matched(q_card, c_card)
        final, vscore, oscore = combine_scores(float(h.score), ov)

        matches.append(Match(
            incident_id=str(h.id),
            score=final,
            vector_score=vscore,
            overlap_score=oscore,
            why_matched=why,
            incident_card=IncidentCard(**c_card),
        ))
        if len(matches) >= req.top_k:
            break

    suggested_actions = [
        "Confirm scope: impacted systems/users and timeline.",
        "Collect logs: auth logs, flow logs, WAF, application errors.",
        "Correlate spikes: 5xx/auth failures/egress anomalies by timestamp.",
        "Containment if needed: rate limit, block indicators, rotate credentials.",
        "Create incident ticket with evidence + matched prior incidents.",
    ]
    return SearchResponse(query_incident_id=req.incident_id, matches=matches, suggested_actions=suggested_actions)
