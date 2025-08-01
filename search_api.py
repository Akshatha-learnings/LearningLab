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

# static fallback tool list with environment-configured IDs
fallback_tools = [
    {
        "name": "Expedite",
        "description": "A tool to expedite processes and enhance efficiency.",
        "category": "Productivity",
        "tags": ["efficiency", "automation", "productivity"],
        "solution_id": os.getenv("EXPEDITE_SOLUTION_ID")
    },
    {
        "name": "Manual",
        "description": "A tool to find insights from data and provide actionable recommendations.",
        "category": "Analytics",
        "tags": ["data analysis", "insights", "recommendations"],
        "solution_id": os.getenv("MANUAL_SOLUTION_ID")
    }
]

@router.get("/fallback", response_model=List[FallbackTool], tags=["Search"])
def get_fallback_tools():
    """
     Returns fallback tool suggestions shown when the main search returns no results.
    """
    return fallback_tools