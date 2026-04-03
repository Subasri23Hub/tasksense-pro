from datetime import date, timedelta


EFFORT_TO_HOURS = {
    "10 min": 0.17,
    "30 min": 0.5,
    "1 hour": 1.0,
    "2 hours": 2.0,
    "3+ hours": 3.0,
}

URGENCY_COLORS = {
    "high": "#FF4B4B",
    "medium": "#FFA500",
    "low": "#21C55D",
}

PRIORITY_COLORS = {
    "Do Now": "#FF4B4B",
    "Do Today": "#FF8C00",
    "Schedule Soon": "#3B82F6",
    "Postpone": "#6B7280",
    "Delegate": "#8B5CF6",
}

CATEGORY_ICONS = {
    "work": "💼",
    "study": "📚",
    "personal": "🏠",
    "interview": "🎯",
    "exam": "📝",
    "errand": "🛒",
    "admin": "📋",
}

OVERLOAD_COLORS = {
    "low": "#21C55D",
    "medium": "#FFA500",
    "high": "#FF4B4B",
}


def get_today() -> str:
    return date.today().strftime("%Y-%m-%d")


def get_tomorrow() -> str:
    return (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")


def effort_to_hours(effort_str: str) -> float:
    return EFFORT_TO_HOURS.get(effort_str, 1.0)


def total_hours(tasks: list) -> float:
    return sum(effort_to_hours(t.effort) for t in tasks)


def get_urgency_badge(urgency: str) -> str:
    colors = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    return colors.get(urgency, "⚪")


def get_priority_emoji(bucket: str) -> str:
    emojis = {
        "Do Now": "🚨",
        "Do Today": "⚡",
        "Schedule Soon": "📅",
        "Postpone": "⏸️",
        "Delegate": "🤝",
    }
    return emojis.get(bucket, "📌")


def get_category_icon(category: str) -> str:
    return CATEGORY_ICONS.get(category.lower(), "📌")


def mode_emoji(mode: str) -> str:
    emojis = {
        "Student Mode": "🎓",
        "Work Mode": "💼",
        "Interview Prep Mode": "🎯",
        "Exam Week Mode": "📚",
        "Personal Life Mode": "🏠",
    }
    return emojis.get(mode, "🧠")
