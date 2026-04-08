import os
import json
# from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from state import CodeCrafterState
import streamlit as st



api_key = st.secrets.get("GEMINI_API_KEY_1")

def frontend_agent(state: CodeCrafterState) -> CodeCrafterState:
    frontend_outputs = {}

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            api_key=api_key,
        )

        services = state.get("services", [])
        features = state.get("features", [])

        for service in services:
            prompt = f"""
Generate React frontend code for this service.

Service: {service}
Features: {features}

Return ONLY valid JSON:
{{
  "filename": "{service}.jsx",
  "content": "React component with API calls"
}}
"""

            try:
                response = llm.invoke([HumanMessage(content=prompt)])
                content = response.content.strip()

                content = content.replace("```json", "").replace("```", "").strip()
                parsed = json.loads(content)

            except Exception:
                parsed = {
                    "filename": f"{service}.jsx",
                    "content": f"// frontend stub for {service}"
                }

            frontend_outputs[service] = parsed

        return {
            **state,
            "frontend_outputs": frontend_outputs,
            "frontend_complete": True,
            "frontend_error": ""
        }

    except Exception as e:
        return {
            **state,
            "frontend_outputs": {},
            "frontend_complete": True,
            "frontend_error": str(e)
        }
