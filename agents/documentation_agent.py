import os
# from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from state import CodeCrafterState
import streamlit as st


api_key = st.secrets.get("GEMINI_API_KEY_1")

def documentation_agent(state: CodeCrafterState) -> CodeCrafterState:
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            api_key=api_key,
        )

        services = state.get("services", [])
        language = state.get("language", "")
        features = state.get("features", [])

        prompt = f"""
Generate a complete project documentation for a generated microservice system.

Details:
Services: {services}
Features: {features}
Language: {language}

Include:

1. Project Overview
2. Folder Structure Explanation
3. How to run backend services step-by-step
4. How to run frontend
5. How to connect frontend to backend APIs
6. Required changes in generated code for real-time usage
7. Environment variables required
8. API endpoint usage
9. Common issues and fixes
10. Deployment steps

Return clean text (no markdown formatting).
"""

        response = llm.invoke([HumanMessage(content=prompt)])
        doc_content = response.content.strip()

        return {
            **state,
            "documentation_output": doc_content,
            "documentation_complete": True,
            "documentation_error": ""
        }

    except Exception as e:
        return {
            **state,
            "documentation_output": "Documentation generation failed.",
            "documentation_complete": True,
            "documentation_error": str(e)
        }
