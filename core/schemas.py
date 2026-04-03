from pydantic import BaseModel, Field
from typing import List, Optional


class Task(BaseModel):
    task: str = Field(description="The task name")
    category: str = Field(description="Category: work, study, personal, interview, exam, errand, admin")
    deadline_text: str = Field(description="Original deadline text from input")
    normalized_deadline: str = Field(description="Normalized deadline as YYYY-MM-DD or 'No deadline'")
    urgency: str = Field(description="high, medium, or low")
    importance: str = Field(description="high, medium, or low")
    effort: str = Field(description="Estimated effort: 10 min, 30 min, 1 hour, 2 hours, 3+ hours")
    priority_bucket: str = Field(description="Do Now, Do Today, Schedule Soon, Postpone, or Delegate")
    reason: str = Field(description="Brief reason for this priority assignment")


class Summary(BaseModel):
    total_tasks: int = Field(description="Total number of tasks extracted")
    urgent_tasks: int = Field(description="Number of high-urgency tasks")
    high_priority_tasks: int = Field(description="Number of Do Now tasks")
    estimated_hours: float = Field(description="Total estimated hours for all tasks")
    overload_risk: str = Field(description="low, medium, or high")
    overload_message: str = Field(description="Human-readable overload assessment")


class DailyPlan(BaseModel):
    morning: List[str] = Field(description="Tasks for morning block", default_factory=list)
    afternoon: List[str] = Field(description="Tasks for afternoon block", default_factory=list)
    evening: List[str] = Field(description="Tasks for evening block", default_factory=list)


class PlannerOutput(BaseModel):
    tasks: List[Task] = Field(description="List of extracted and prioritized tasks")
    summary: Summary = Field(description="Summary statistics")
    daily_plan: DailyPlan = Field(description="Suggested daily execution plan")
    warnings: List[str] = Field(description="Warnings about overload, conflicts, risks", default_factory=list)
    recommendations: List[str] = Field(description="Actionable recommendations", default_factory=list)
