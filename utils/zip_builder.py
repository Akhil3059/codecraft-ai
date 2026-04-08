import io
import zipfile
import re


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def normalize(item):
    """Ensure LLM output is always a dict (handles list issue)."""
    if isinstance(item, list):
        return item[0] if item else {}
    return item or {}


def build_project_zip(result):
    zip_buffer = io.BytesIO()

    # Dynamic project name
    user_story = result.get("user_story", "generated_project")
    project_name = slugify(user_story)[:30] or "generated_project"

    root = f"{project_name}/"

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:

        # -------------------------------
        # Backend Services
        # -------------------------------
        for service, files in result.get("service_outputs", {}).items():
            files = normalize(files)
            safe_service = slugify(service)
            base = f"{root}services/{safe_service}/"

            zf.writestr(base + "controller.py", files.get("controller_code", ""))
            zf.writestr(base + "service.py", files.get("service_code", ""))
            zf.writestr(base + "model.py", files.get("model_code", ""))

        # -------------------------------
        # Swagger Docs
        # -------------------------------
        for service, swagger in result.get("swagger_outputs", {}).items():
            swagger = normalize(swagger)
            safe_service = slugify(service)

            zf.writestr(
                f"{root}swagger/{safe_service}/swagger.yaml",
                swagger.get("content", "")
            )

        # -------------------------------
        # Tests
        # -------------------------------
        for service, test in result.get("test_outputs", {}).items():
            test = normalize(test)
            safe_service = slugify(service)

            filename = test.get("filename", "test.py")

            zf.writestr(
                f"{root}tests/{safe_service}/{filename}",
                test.get("content", "")
            )

        # -------------------------------
        # Frontend
        # -------------------------------
        for service, frontend in result.get("frontend_outputs", {}).items():
            frontend = normalize(frontend)
            safe_service = slugify(service)

            filename = frontend.get("filename", "app.jsx")

            zf.writestr(
                f"{root}frontend/{safe_service}/{filename}",
                frontend.get("content", "")
            )

        # -------------------------------
        # Documentation
        # -------------------------------
        zf.writestr(
            f"{root}README.md",
            result.get("documentation_output", "Project Documentation")
        )

        # -------------------------------
        # Environment Template
        # -------------------------------
        env_example = """GEMINI_API_KEY_1=your_api_key_here
"""
        zf.writestr(f"{root}.env.example", env_example)

        # -------------------------------
        # Requirements
        # -------------------------------
        requirements = """streamlit
langgraph
langchain
langchain-core
langchain-community
langchain-google-genai
google-generativeai
python-dotenv
requests
pydantic
pytest
"""
        zf.writestr(f"{root}requirements.txt", requirements)

    zip_buffer.seek(0)
    return zip_buffer
