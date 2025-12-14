def severity_rank(s: str) -> int:
    order = {"low": 1, "medium": 2, "high": 3, "critical": 4}
    return order.get(s, 0)

def overlap_score(query_card: dict, cand_card: dict) -> float:
    q_e = (query_card.get("entities") or {})
    c_e = (cand_card.get("entities") or {})

    def setify(x): 
        return set([str(v).strip().lower() for v in (x or []) if str(v).strip()])

    overlap = 0.0
    overlap += 1.0 * len(setify(q_e.get("systems")) & setify(c_e.get("systems")))
    overlap += 1.0 * len(setify(q_e.get("vendors")) & setify(c_e.get("vendors")))
    overlap += 1.0 * len(setify(q_e.get("ports")) & setify(c_e.get("ports")))
    overlap += 0.5 * len(setify(q_e.get("protocols")) & setify(c_e.get("protocols")))
    overlap += 0.5 * len(setify(q_e.get("observables")) & setify(c_e.get("observables")))
    return float(overlap)

def build_why_matched(query_card: dict, cand_card: dict) -> dict:
    q_e = (query_card.get("entities") or {})
    c_e = (cand_card.get("entities") or {})

    def inter(k):
        q = set([str(x).strip().lower() for x in (q_e.get(k) or [])])
        c = set([str(x).strip().lower() for x in (c_e.get(k) or [])])
        return sorted([x for x in (q & c) if x])

    return {
        "overlap": {
            "systems": inter("systems"),
            "vendors": inter("vendors"),
            "ports": inter("ports"),
            "protocols": inter("protocols"),
            "observables": inter("observables"),
        },
        "symptoms_overlap": sorted(
            set([str(x).lower() for x in (query_card.get("symptoms") or [])]) &
            set([str(x).lower() for x in (cand_card.get("symptoms") or [])])
        )
    }

def combine_scores(vector_score: float, overlap: float) -> tuple[float, float, float]:
    overlap_norm = min(overlap / 8.0, 1.0)
    final = 0.7 * vector_score + 0.3 * overlap_norm
    return float(final), float(vector_score), float(overlap_norm)
