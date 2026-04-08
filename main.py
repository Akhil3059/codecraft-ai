import streamlit as st
from graph import run_all_agents
from utils.zip_builder import build_project_zip
import tempfile
import os

# -------------------------------
# Session State Initialization
# -------------------------------
if "result" not in st.session_state:
    st.session_state.result = None

if "generated" not in st.session_state:
    st.session_state.generated = False

if "zip_data" not in st.session_state:
    st.session_state.zip_data = None

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="GenAI Microservice Code Generator",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=120)
    st.title("CodeCrafter AI")
    st.markdown("### 🚀 GenAI Builder")
    st.markdown("---")
    st.info("Generate production-ready microservices using AI")

# -------------------------------
# Header
# -------------------------------
col_logo, col_title = st.columns([1, 5])

with col_logo:
    st.image("https://cdn-icons-png.flaticon.com/512/2721/2721268.png", width=80)

with col_title:
    st.title("CodeCrafter AI: GenAI-Powered Microservice Builder")
    st.caption("Design scalable microservices instantly with AI 🤖")

# -------------------------------
# Input Form
# -------------------------------
with st.form("codecraft_form"):
    user_story = st.text_area(
        "Enter User Story",
        height=150,
        placeholder="e.g., Build an e-commerce order management system..."
    )

    language = st.selectbox(
        "Select Language",
        ["Java", "NodeJS", ".NET", "Python", "Go", "Ruby", "PHP", "Kotlin"]
    )

    submitted = st.form_submit_button("Generate Microservices")

# -------------------------------
# Generate Logic
# -------------------------------
if submitted and user_story.strip():
    with st.spinner("Generating microservices..."):
        result = run_all_agents(user_story, language)

    st.session_state.result = result
    st.session_state.generated = True
    
    # Generate ZIP immediately and store in session state
    try:
        zip_file = build_project_zip(result)
        st.session_state.zip_data = zip_file.getvalue()
    except Exception as e:
        st.error(f"Error generating ZIP: {e}")
        st.session_state.zip_data = None

# -------------------------------
# Use stored result
# -------------------------------
result = st.session_state.result or {}

if st.session_state.generated:

    st.success("Generation completed successfully ✅")

    # -------------------------------
    # Features & Services
    # -------------------------------
    st.subheader("Features & Services")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Features")
        for i, feature in enumerate(result.get("features", []), 1):
            st.write(f"{i}. {feature}")

    with col2:
        st.markdown("### Services")
        for i, service in enumerate(result.get("services", []), 1):
            st.code(f"{i}. {service}")

    # -------------------------------
    # Architecture
    # -------------------------------
    arch = result.get("architecture_config", {})

    if arch:
        st.subheader("Architecture Configuration")
        st.write("Architecture:", arch.get("architecture", ""))
        st.write("Database:", arch.get("database", ""))
        st.write("Messaging:", arch.get("messaging", ""))
        st.write("Cache:", arch.get("cache", ""))
        st.write("API Gateway:", arch.get("api_gateway", ""))
        st.write("Service Discovery:", arch.get("service_discovery", ""))

    # -------------------------------
    # Code Preview
    # -------------------------------
    st.subheader("Generated Code Preview")

    for service, files in result.get("service_outputs", {}).items():
        with st.expander(service):
            st.markdown("### Controller")
            st.code(files.get("controller_code", ""), language=language.lower())

            st.markdown("### Service")
            st.code(files.get("service_code", ""), language=language.lower())

            st.markdown("### Model")
            st.code(files.get("model_code", ""), language=language.lower())

    # -------------------------------
    # Swagger
    # -------------------------------
    st.subheader("Swagger Documentation")

    for service, swagger in result.get("swagger_outputs", {}).items():
        with st.expander(service):
            if isinstance(swagger, list):
                swagger = swagger[0] if swagger else {}
            st.code(swagger.get("content", ""), language="yaml")

    # -------------------------------
    # Tests
    # -------------------------------
    st.subheader("Unit Tests")

    for service, test in result.get("test_outputs", {}).items():
        with st.expander(service):
            if isinstance(test, list):
                test = test[0] if test else {}
            st.code(test.get("content", ""), language=language.lower())

    # -------------------------------
    # Frontend
    # -------------------------------
    st.subheader("Frontend Code")

    for service, frontend in result.get("frontend_outputs", {}).items():
        with st.expander(service):
            if isinstance(frontend, list):
                frontend = frontend[0] if frontend else {}
            st.code(frontend.get("content", ""), language="javascript")

    # -------------------------------
    # Documentation
    # -------------------------------
    st.subheader("Project Documentation")

    st.text_area(
        "Generated Documentation",
        result.get("documentation_output", ""),
        height=400
    )


