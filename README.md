# TaskSense Pro 🧠

**AI-Powered Planning & Prioritization Assistant**

TaskSense Pro converts your messy, unorganized notes and task dumps into structured, deadline-aware, prioritized execution plans.

---

## Features

- 🔍 **Smart Task Extraction** — paste raw notes, emails, WhatsApp texts
- 📅 **Deadline Normalization** — understands "today", "Friday", "next week"
- ⚡ **Priority Engine** — Do Now / Do Today / Schedule Soon / Postpone
- 🧠 **RAG Knowledge Base** — retrieves productivity frameworks to guide planning
- ⚠️ **Overload Detector** — warns when your plan is unrealistic
- 🗓️ **Daily Planner** — morning / afternoon / evening blocks
- 💬 **Follow-Up Refinement** — refine your plan with natural language
- 📊 **Analytics Dashboard** — task stats, charts, breakdown

---

## Setup

1. Clone or download the project
2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Add your Gemini API key to `.env`:
   ```
   GOOGLE_API_KEY=your_key_here
   ```
5. Run the app:
   ```bash
   streamlit run app.py
   ```

---

## Modes

| Mode | Focus |
|---|---|
| 🎓 Student | Assignments, study blocks, exams |
| 💼 Work | Meetings, deliverables, emails |
| 🎯 Interview Prep | Prep sequencing, practice sessions |
| 📚 Exam Week | Intense prioritization, revision |
| 🏠 Personal Life | Errands, appointments, chores |

---

## Architecture

```
tasksense_pro/
├── app.py               # Main Streamlit entry point
├── core/
│   ├── llm.py           # Gemini model setup
│   ├── prompts.py       # All prompt templates
│   ├── schemas.py       # Pydantic structured output schemas
│   ├── planner.py       # Core planning logic
│   ├── retriever.py     # RAG vector store & retriever
│   ├── parser.py        # Output parsing
│   └── utils.py         # Utility helpers
├── data/
│   └── productivity_knowledge.txt  # RAG knowledge base
├── pages/
│   ├── dashboard.py     # Analytics view
│   └── settings.py      # Preferences
└── assets/
    └── styles.css       # Custom CSS
```

💡 Use Case

Paste messy notes → get a structured, prioritized execution plan.

---

🌟 Future Improvements
- Calendar integration
- Gmail integration
- Task history tracking
- Mobile UI optimization
