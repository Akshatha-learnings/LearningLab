from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from config import settings

router = APIRouter(prefix="/search")

# Response model
class FallbackTool(BaseModel):
    name: str
    description: str
    category: str
    tags: List[str]
    solution_id: str  # Added solution_id field


def get_fallback_tools_data() -> List[dict]:
    """
    Get fallback tools with solution IDs from environment configuration.
    """
    return [
        {
            "name": "Expedite",
            "description": "A tool to expedite processes and enhance efficiency.",
            "category": "Productivity",
            "tags": ["efficiency", "automation", "productivity"],
            "solution_id": settings.expedite_solution_id
        },
        {
            "name": "Manual",
            "description": "A tool to find insights from data and provide actionable recommendations.",
            "category": "Analytics",
            "tags": ["data analysis", "insights", "recommendations"],
            "solution_id": settings.manual_solution_id
        }
    ]


@router.get("/fallback", response_model=List[FallbackTool], tags=["Search"])
def get_fallback_tools():
    """
    Returns fallback tool suggestions shown when the main search returns no results.
    Solution IDs are configured via environment variables for different environments.
    """
    fallback_tools = get_fallback_tools_data()
    return fallback_tools