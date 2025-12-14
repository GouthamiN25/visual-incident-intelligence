from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal, Any

AssetType = Literal["network_diagram", "dashboard", "architecture", "unknown"]
Severity = Literal["low", "medium", "high", "critical", "unknown"]

class Entities(BaseModel):
    systems: List[str] = []
    vendors: List[str] = []
    protocols: List[str] = []
    ports: List[str] = []
    observables: List[str] = []

class IncidentCard(BaseModel):
    asset_type: AssetType = "unknown"
    entities: Entities = Field(default_factory=Entities)
    symptoms: List[str] = []
    hypotheses: List[str] = []
    severity_guess: Severity = "unknown"
    recommended_logs: List[str] = []
    summary: str = "unknown"

class IngestResponse(BaseModel):
    incident_id: str
    incident_card: IncidentCard

class SearchRequest(BaseModel):
    incident_id: str
    top_k: int = 5
    min_severity: Optional[Literal["low", "medium", "high", "critical"]] = None

class Match(BaseModel):
    incident_id: str
    score: float
    vector_score: float
    overlap_score: float
    why_matched: Dict[str, Any]
    incident_card: IncidentCard

class SearchResponse(BaseModel):
    query_incident_id: str
    matches: List[Match]
    suggested_actions: List[str]
