import os
import json
import re
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from state import CodeCrafterState, get_file_extension
from langsmith import traceable

load_dotenv()
@traceable(
    name="swagger_agent",
   
)
def swagger_agent(state: CodeCrafterState) -> CodeCrafterState:
    

    swagger_docs = {}

    try:
        llm = ChatGoogleGenerativeAI(
            model = "gemini-2.5-flash-lite",
            google_api_key = os.getenv("GEMINI_API_KEY_3")
        )
        service_outputs = state.get("service_outputs", {})

        for service, files in service_outputs.items():
            controller_code = files.get("controller_code", "").replace("{","{{").replace("}","}}")

            prompt = f"""
            Generate OpenAPI 3.0.0 YAML documentation for this controller.
            
            Controller code:
            {controller_code}
            Return ONLY valid JSON:
            {{
                "filename": "swagger.yaml",
                "content": "openapi: 3.0.0 ..."
            }}
            """
            try:
                response = llm.invoke([HumanMessage(content=prompt)])
                content = response.content.strip()

                content = content.replace("```json","").replace("```","").strip()

                parsed = json.loads(content)
            except Exception:
                parsed = {
                    "filename": "swagger.yaml",
                    "content": f"""openapi: 3.0.0
                    info:
                    title{service} API
                    version:1.0.0
                    paths: {{}}
                    """
                }

            swagger_docs[service] = parsed

        return {
            **state,
            "swagger_outputs":swagger_docs,
            "swagger_output":swagger_docs,
            "swagger_complete": True,
            "swagger_error": ""
        }
    except Exception as e:
        return {
            **state,
            "swagger_outputs": {},
            "swagger_output": {},
            "swagger_complete": True,
            "swagger_error": str(e)
        }
        