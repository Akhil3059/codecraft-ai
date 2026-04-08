import os
import json
import re
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from state import CodeCrafterState
from langsmith import traceable

load_dotenv(override=True)

api_key = st.secrets["GEMINI_API_KEY_1"]


def extract_json(text: str):
    """Extract JSON object from LLM response."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in LLM output")
    return json.loads(match.group())


@traceable(
    name="planning_agent",

)
def planning_agent(state: CodeCrafterState) -> CodeCrafterState:
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=api_key,
            temperature=0
        )

        user_story = state["user_story"]

        prompt = f"""
You are an expert software architect.

Analyze the user story and design a microservice architecture.

Return ONLY valid JSON.
Do NOT include explanations.
Do NOT include markdown.
Do NOT include text before or after JSON.

User Story:
{user_story}

Return JSON in this format:

{{
  "features": ["feature1", "feature2"],
  "services": ["service1", "service2"],
  "architecture_hints": {{
    "architecture": "REST API",
    "database": "PostgreSQL",
    "messaging": "Kafka",
    "cache": "Redis",
    "api_gateway": "Express Gateway",
    "service_discovery": "Consul"
  }},
  "architecture_config": {{
    "architecture": "REST API",
    "database": "PostgreSQL",
    "messaging": "Kafka",
    "cache": "Redis",
    "api_gateway": "Express Gateway",
    "service_discovery": "Consul"
  }}
}}
"""

        response = llm.invoke([HumanMessage(content=prompt)])

        content = str(response.content).strip()

        print("\n===== RAW LLM RESPONSE =====")
        print(content)
        print("============================\n")

        parsed = extract_json(content)

        return {
            **state,
            "features": parsed.get("features", []),
            "services": parsed.get("services", []),
            "architecture_hints": parsed.get("architecture_hints", {}),
            "architecture_config": parsed.get("architecture_config", {}),
            "planning_complete": True,
            "planning_error": ""
        }

    except Exception as e:
        print("PLANNING ERROR:", e)

        return {
            **state,
            "features": [state["user_story"]],
            "services": ["default-service"],
            "architecture_hints": {"architecture": "REST API"},
            "architecture_config": {"architecture": "REST API"},
            "planning_complete": True,
            "planning_error": str(e)
        }
