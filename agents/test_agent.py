import os
import json
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from state import CodeCrafterState, get_file_extension
from langsmith import traceable

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY_1") or st.secrets["GEMINI_API_KEY_1"]

@traceable(
    name="test_agent",
   
)
def generate_tests(state: CodeCrafterState) -> CodeCrafterState:
   

    test_files = {}

    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=api_key,
        )

        service_outputs = state.get("service_outputs",{})
        language = state["language"]
        ext = get_file_extension(language)

        for service,files in service_outputs.items():
            controller_code=files.get("controller_code","")
            service_code = files.get("service_code","")

            prompt = f"""
            Generate unit tests for this {language} microservice.
            
            Controller:
            {controller_code}
            
            Service:
            {service_code}
            
            Return ONLY valid JSON:
            
            {{
                "filename": "test_{service}.{ext}",
                "content": "..."
            }}
            """

            try:
                response = llm.invoke([HumanMessage(content=prompt)])
                content = response.content.strip()

                content = content.replace("```json", "").replace("```","").strip()

                parsed = json.loads(content)
            
            except Exception:
                parsed= {
                    "filename": f"test_{service}.{ext}",
                    "content": f"# unit test stub for {service}"
                }
            
            test_files[service] = parsed

        return {
            **state,
            "test_outputs": test_files,
            "test_output": test_files,
            "tests_complete": True,
            "test_error": ""
        }
    
    except Exception as e:
        return {
            **state,
            "test_outputs": {},
            "test_output": {},
            "tests_complete": True,
            "test_error": str(e)
        }
