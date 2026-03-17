from crewai import Task
from backend.tools.web_search import search_web
from backend.crew.agents import (
    manager_agent,
    data_analyst_agent,
    research_agent
)


def create_tasks(enhanced_prompt: str, original_question: str):

    q = original_question.lower()

    # ----------------------------------------
    # 🔎 INTENT DETECTION
    # ----------------------------------------

    dataset_keywords = [
        "order", "show", "list", "details", "which",
        "how many", "count", "warehouse",
        "delayed", "distance", "picking",
        "transport", "mode"
    ]

    research_keywords = [
        "why", "improve", "optimize", "strategy",
        "best practice", "technology",
        "future", "automation",
        "reduce", "recommendation"
    ]

    is_dataset_query = any(k in q for k in dataset_keywords)
    is_research_query = any(k in q for k in research_keywords)

    # ----------------------------------------
    # ✅ CASE 1: DATASET ONLY
    # ----------------------------------------
    if is_dataset_query and not is_research_query:

        data_task = Task(
            description=f"""
You are a warehouse dataset analyst.

Using the dataset context below:

{enhanced_prompt}

Answer the user's question strictly using dataset data.

Return output ONLY in markdown table format.
Do NOT provide explanations.
Do NOT provide recommendations.
Do NOT provide root cause.
""",
            expected_output="Markdown table from dataset only.",
            agent=data_analyst_agent
        )

        return [data_task]

    # ----------------------------------------
    # ✅ CASE 2: RESEARCH + DATA
    # ----------------------------------------

    web_context = search_web(original_question)[:300]

    data_task = Task(
        description=f"""
Analyze warehouse dataset:

{enhanced_prompt}

Identify:
- Delay causes
- Operational inefficiencies
- Key performance observations

Concise bullet format.
""",
        expected_output="Structured dataset insights.",
        agent=data_analyst_agent
    )

    research_task = Task(
    description=f"""
User Question:
{original_question}

Using industry research below:

{web_context}

Provide:
- Best practices
- Optimization strategies
- Benchmark insights

Maximum 5 bullets total.
""",
    expected_output="Short industry best practices summary.",
    agent=research_agent
)

    manager_task = Task(
    description="""
Combine outputs from Data Analyst and Research agents.

Provide:
1. Root Cause (2 bullets max)
2. Insights (3 bullets max)
3. Industry Best Practices (3 bullets max)
4. Recommendations (3 bullets max)

Keep concise.
Max 200 words.
""",
    expected_output="Concise structured strategic report.",
    agent=manager_agent,
    depends_on=[data_task, research_task]
)

    return [data_task, research_task, manager_task]