import time
from backend.crew.tasks import create_tasks
from backend.services.report_writer import save_report
from backend.memory.memory_store import save_memory
from backend.crew.agents import (
    data_analyst_agent,
    research_agent,
    manager_agent
)
from litellm.exceptions import RateLimitError


def run_crew(enhanced_prompt: str, original_question: str):
    """
    Manual multi-agent execution.
    No crew.kickoff()
    No execute_task()
    No .prompt errors
    """

    agent_status = []
    max_retries = 2
    attempt = 0

    while attempt <= max_retries:
        try:
            # -----------------------------
            # 1️⃣ DATA AGENT
            # -----------------------------
            agent_status.append("Data Analyst Agent started")

            data_prompt = f"""
Analyze warehouse dataset:

{enhanced_prompt}

Provide:
- Root operational insights (max 3 bullets)
- Delay causes (if any)
- Performance observations

Max 150 words.
"""

            data_output = data_analyst_agent.llm.call(
                messages=[{"role": "user", "content": data_prompt}]
            )

            data_output = str(data_output)[:700]

            # -----------------------------
            # 2️⃣ RESEARCH AGENT
            # -----------------------------
            agent_status.append("Research Agent started")

            research_prompt = f"""
User Question:
{original_question}

Provide:
- 3 industry best practices
- 3 optimization strategies
- 2 benchmark insights

Concise bullet format.
Max 150 words.
"""

            research_output = research_agent.llm.call(
                messages=[{"role": "user", "content": research_prompt}]
            )

            research_output = str(research_output)[:700]

            # -----------------------------
            # 3️⃣ MANAGER AGENT
            # -----------------------------
            agent_status.append("Manager Agent started")

            manager_prompt = f"""
Data Summary:
{data_output}

Research Summary:
{research_output}

User Question:
{original_question}

Generate structured report:

1. Root Cause
2. Insights
3. Industry Best Practices
4. Recommendations

Bullet format.
Max 250 words.
"""

            final_output = manager_agent.llm.call(
                messages=[{"role": "user", "content": manager_prompt}]
            )

            final_output = str(final_output)

            agent_status.append("All agents completed successfully")

            # -----------------------------
            # Save report + memory
            # -----------------------------
            save_report(original_question, final_output)
            save_memory(original_question, final_output)

            return {
                "success": True,
                "status": agent_status,
                "result": final_output
            }

        except RateLimitError:
            attempt += 1

            if attempt > max_retries:
                agent_status.append("Rate limit exceeded after retries")
                return {
                    "success": False,
                    "status": agent_status,
                    "error": "Groq rate limit exceeded. Please wait 60 seconds and try again."
                }

            wait_time = 30
            print(f"Rate limit hit. Waiting {wait_time} seconds...")
            time.sleep(wait_time)

        except Exception as e:
            agent_status.append("Agent execution failed")
            return {
                "success": False,
                "status": agent_status,
                "error": str(e)
            }