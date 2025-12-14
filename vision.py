from .schemas import IncidentCard, Entities

def extract_incident_card_from_image(image_path: str, user_note: str | None = None) -> IncidentCard:
    """
    MVP stub:
    - We don't parse image contents yet.
    - We use the note so the pipeline works end-to-end immediately.
    Replace this with Gemini Vision extraction later.
    """
    note = (user_note or "").strip()
    symptoms = [x.strip() for x in note.split(",") if x.strip()] if note else []

    return IncidentCard(
        asset_type="unknown",
        entities=Entities(systems=[], vendors=[], protocols=[], ports=[], observables=[]),
        symptoms=symptoms,
        hypotheses=["possible service outage"] if "down" in note.lower() else [],
        severity_guess="medium" if symptoms else "unknown",
        recommended_logs=["auth logs", "vpc flow logs", "waf logs"],
        summary=note or "Evidence uploaded. (MVP stub: replace with Gemini Vision extraction.)",
    )
