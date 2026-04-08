import os
import json
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from state import CodeCrafterState, get_file_extension

import os
import streamlit as st
# from dotenv import load_dotenv




api_key = st.secrets.get("GEMINI_API_KEY_1")

if not api_key:
    raise ValueError("GEMINI_API_KEY_1 is not set")
   
def codegen_agent(state: CodeCrafterState) -> CodeCrafterState:
    service_files = {}

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            api_key=api_key,
        )

        features = state.get("features", [])
        services = state.get("services", [])
        architecture = state.get("architecture_config", {})
        language = state["language"]

        ext = get_file_extension(language)

        for service in services:
            prompt = f"""
Generate production-ready {language} microservice code for:

Service: {service}
Features: {features}
Architecture: {architecture}

Return ONLY valid JSON:

{{
  "controller_filename": "controller.{ext}",
  "controller_code": "...",
  "service_filename": "service.{ext}",
  "service_code": "...",
  "model_filename": "model.{ext}",
  "model_code": "..."
}}
"""

            try:
                response = llm.invoke([HumanMessage(content=prompt)])
                content = response.content.strip()

                content = content.replace("```json", "").replace("```", "").strip()

                parsed = json.loads(content)

            except Exception:
                parsed = {
                    "controller_filename": f"controller.{ext}",
                    "controller_code": f"# {service} controller stub",
                    "service_filename": f"service.{ext}",
                    "service_code": f"# {service} service stub",
                    "model_filename": f"model.{ext}",
                    "model_code": f"# {service} model stub"
                }

            parsed["language"] = language

            service_files[service] = parsed

        return {
            **state,
            "service_outputs": service_files,
            "code_output": service_files,
            "codegen_complete": True,
            "codegen_error": ""
        }

    except Exception as e:
        return {
            **state,
            "service_outputs": {},
            "code_output": {},
            "codegen_complete": True,
            "codegen_error": str(e)
        }
