import io
import zipfile


def build_project_zip(result):
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:

        # Backend
        for service, files in result.get("service_outputs", {}).items():
            base_path = f"project/{service}/"

            zf.writestr(base_path + "controller.py", files.get("controller_code", ""))
            zf.writestr(base_path + "service.py", files.get("service_code", ""))
            zf.writestr(base_path + "model.py", files.get("model_code", ""))

        # Swagger
        for service, swagger in result.get("swagger_outputs", {}).items():
            zf.writestr(f"swagger/{service}/swagger.yaml", swagger.get("content", ""))

        # Tests
        for service, test in result.get("test_outputs", {}).items():
            filename = test.get("filename", "test.py")
            zf.writestr(f"tests/{service}/{filename}", test.get("content", ""))

        # Frontend
        for service, frontend in result.get("frontend_outputs", {}).items():
            filename = frontend.get("filename", "app.jsx")
            zf.writestr(f"frontend/{service}/{filename}", frontend.get("content", ""))

        # Documentation
        zf.writestr("README.txt", result.get("documentation_output", ""))

        # Requirements
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
"""
        zf.writestr("requirements.txt", requirements)

    zip_buffer.seek(0)
    return zip_buffer