import json
import re
from typing import Optional
from core.schemas import PlannerOutput, Task, Summary, DailyPlan


def clean_json_string(raw: str) -> str:
    """Remove markdown code fences and clean up JSON string."""
    # Remove ```json ... ``` blocks
    raw = re.sub(r"```json\s*", "", raw)
    raw = re.sub(r"```\s*", "", raw)
    raw = raw.strip()
    return raw


def parse_planner_output(raw_response: str) -> Optional[PlannerOutput]:
    """Parse raw LLM response into a PlannerOutput object."""
    try:
        cleaned = clean_json_string(raw_response)
        data = json.loads(cleaned)
        
        tasks = [Task(**t) for t in data.get("tasks", [])]
        summary = Summary(**data.get("summary", {}))
        daily_plan = DailyPlan(**data.get("daily_plan", {}))
        warnings = data.get("warnings", [])
        recommendations = data.get("recommendations", [])
        
        return PlannerOutput(
            tasks=tasks,
            summary=summary,
            daily_plan=daily_plan,
            warnings=warnings,
            recommendations=recommendations
        )
    except Exception as e:
        return None


def parse_raw_json(raw_response: str) -> Optional[dict]:
    """Parse raw JSON from LLM response, return as dict."""
    try:
        cleaned = clean_json_string(raw_response)
        return json.loads(cleaned)
    except Exception:
        return None
