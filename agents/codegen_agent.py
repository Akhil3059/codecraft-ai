import os
import json
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_groq import ChatGroq
from state import CodeCrafterState, get_file_extension
from langsmith import traceable
import streamlit as st

load_dotenv(override=True)

api_key = st.secrets["GEMINI_API_KEY_1"]
@traceable(
    name="codegen_agent",
   
)
def codegen_agent(state: CodeCrafterState) -> CodeCrafterState:
    service_files = {}

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=api_key,
            # model="llama-3.1-8b-instant",
            # api_key=os.getenv("GROQ_API_KEY")
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
