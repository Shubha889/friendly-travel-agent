from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class A2ATaskRequest(BaseModel):
    task_id: str
    task_type: str
    session_id: str
    parameters: Dict[str, Any]
    metadata: Dict[str, Any]


class A2ATaskResponse(BaseModel):
    task_id: str
    status: str
    results: List[Dict[str, Any]] = []
    clarification_needed: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict[str, Any]