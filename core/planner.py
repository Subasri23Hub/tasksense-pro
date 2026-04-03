from core.llm import get_llm
from core.prompts import MAIN_PLANNER_PROMPT, FOLLOWUP_PROMPT
from core.retriever import retrieve_context
from core.parser import parse_planner_output
from core.utils import get_today
from core.schemas import PlannerOutput


def run_planner(
    user_input: str,
    mode: str = "Work Mode",
    available_hours: int = 8
) -> tuple[PlannerOutput | None, str]:
    """
    Main planning pipeline.
    Returns:
        (PlannerOutput, raw_json_string)
        or
        (None, error_message)
    """
    try:
        llm = get_llm(temperature=0.3)

        # Step 1: Retrieve relevant productivity/planning context
        context = retrieve_context(user_input, k=5)

        # Step 2: Build final prompt
        prompt_text = MAIN_PLANNER_PROMPT.format(
            user_input=user_input,
            mode=mode,
            today_date=get_today(),
            context=context,
            available_hours=available_hours,
        )

        # Step 3: Call LLM
        response = llm.invoke(prompt_text)
        raw = response.content if hasattr(response, "content") else str(response)

        # Step 4: Parse structured JSON output
        result = parse_planner_output(raw)
        if result is None:
            return None, f"Failed to parse LLM response:\n{raw}"

        return result, raw

    except Exception as e:
        return None, f"Error running planner: {str(e)}"


def run_followup(
    existing_plan_json: str,
    followup_request: str,
    mode: str = "Work Mode"
) -> tuple[PlannerOutput | None, str]:
    """
    Follow-up refinement pipeline.
    Returns:
        (PlannerOutput, raw_json_string)
        or
        (None, error_message)
    """
    try:
        llm = get_llm(temperature=0.3)

        prompt_text = FOLLOWUP_PROMPT.format(
            existing_plan=existing_plan_json,
            followup_request=followup_request,
            today_date=get_today(),
            mode=mode,
        )

        response = llm.invoke(prompt_text)
        raw = response.content if hasattr(response, "content") else str(response)

        result = parse_planner_output(raw)
        if result is None:
            return None, f"Failed to parse follow-up response:\n{raw}"

        return result, raw

    except Exception as e:
        return None, f"Error running follow-up: {str(e)}"