from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime

class RiskItem(BaseModel):
    clause: str
    risk_level: str
    reason: str
    suggestion: str
    jurisdiction: Optional[str] = None

class ContractAnalysisResponse(BaseModel):
    contract_id: str
    filename: str
    executive_summary: str
    key_parties: Dict[str, Any]
    key_clauses: Dict[str, str]
    risk_analysis: List[RiskItem]
    overall_risk_score: int
    risk_level: str
    red_flags: List[str]
    recommendations: List[str]
    analysis_date: datetime
    pdf_report: Optional[str] = None
    word_report: Optional[str] = None
    language: str = "en"

class ComparisonResponse(BaseModel):
    contract1: str
    contract2: str
    key_differences: List[str]
    risk_comparison: Dict[str, str]
    