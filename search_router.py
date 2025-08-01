from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import os

router = APIRouter(prefix="/search")

#response model
class FallbackTool(BaseModel):
    name: str
    description: str
    category: str
    tags: List[str]
    solution_id: str

# Get solution IDs from environment variables
def get_fallback_tools():
    """
    Returns fallback tool suggestions with solution IDs from environment variables.
    """
    fallback_tools = [
        {
            "name": "Expedite",
            "description": "A tool to expedite processes and enhance efficiency.",
            "category": "Productivity",
            "tags": ["efficiency", "automation", "productivity"],
            "solution_id": os.getenv("EXPEDITE_SOLUTION_ID", "default_expedite_001")
        },
        {
            "name": "Manual",
            "description": "A tool to find insights from data and provide actionable recommendations.",
            "category": "Analytics",
            "tags": ["data analysis", "insights", "recommendations"],
            "solution_id": os.getenv("MANUAL_SOLUTION_ID", "default_manual_002")
        }
    ]
    return fallback_tools

@router.get("/fallback", response_model=List[FallbackTool], tags=["Search"])
def get_fallback_tools_endpoint():
    """
     Returns fallback tool suggestions shown when the main search returns no results.
    """
    return get_fallback_tools()