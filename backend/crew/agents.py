import os
from crewai import Agent
from crewai import LLM
from dotenv import load_dotenv

load_dotenv()

# Proper CrewAI Groq LLM configuration
groq_llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
    max_tokens=800  # VERY IMPORTANT
)

# -----------------------------
# Manager Agent
# -----------------------------
manager_agent = Agent(
    role="Manager Agent",
    goal="Interpret user query and delegate tasks to appropriate agents.",
    backstory="You orchestrate warehouse intelligence and combine analytical insights.",
    verbose=True,
    allow_delegation=True,
    llm=groq_llm
)

# -----------------------------
# Data Analyst Agent
# -----------------------------
data_analyst_agent = Agent(
    role="Data Analyst Agent",
    goal="Analyze structured warehouse dataset and identify operational insights.",
    backstory="Expert in warehouse KPIs and delay pattern analysis.",
    verbose=True,
    allow_delegation=False,
    llm=groq_llm
)

# -----------------------------
# Research Agent
# -----------------------------
research_agent = Agent(
    role="Research Agent",
    goal="Perform logistics research and identify industry best practices.",
    backstory="Specialist in global logistics optimization strategies.",
    verbose=True,
    allow_delegation=False,
    llm=groq_llm
)