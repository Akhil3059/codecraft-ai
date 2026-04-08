import streamlit as st
from graph import run_all_agents
from utils.zip_builder import build_project_zip

import os
import streamlit as st

st.write("API KEY:", os.getenv("GEMINI_API_KEY_1"))
# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="GenAI Microservice Code Generator",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------
# Sidebar Branding / Logos
# -------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=120)
    st.title("CodeCrafter AI")
    st.markdown("### 🚀 GenAI Builder")
    st.markdown("---")
    st.info("Generate production-ready microservices using AI")

# -------------------------------
# Header Section
# -------------------------------
col_logo, col_title = st.columns([1, 5])

with col_logo:
    # Main logo (top-left)
    st.image("https://cdn-icons-png.flaticon.com/512/2721/2721268.png", width=80)

with col_title:
    st.title("CodeCrafter AI: GenAI-Powered Microservice Builder")
    st.caption("Design scalable microservices instantly with AI 🤖")

# -------------------------------
# Input Form Section
# -------------------------------
with st.form("codecraft_form"):
    # User story input field
    user_story = st.text_area(
        "Enter User Story",
        height=150,
        placeholder="e.g., Build an e-commerce order management system..."
    )

    # Language selection dropdown
    language = st.selectbox(
        "Select Language",
        ["Java", "NodeJS", ".NET", "Python", "Go", "Ruby", "PHP", "Kotlin"]
    )

    # Submit button
    submitted = st.form_submit_button("Generate Microservices")

# -------------------------------
# Main Processing Logic
# -------------------------------
if submitted and user_story.strip():

    # Show loading spinner while AI generates output
    with st.spinner("Generating microservices..."):
        result = run_all_agents(user_story, language)

    # Success message after generation
    st.success("Generation completed successfully ✅")

   

    # -------------------------------
    # Features & Services Section
    # -------------------------------
    st.subheader("Features & Services")

    col1, col2 = st.columns(2)

    # Display extracted features
    with col1:
        st.markdown("### Features")
        for i, feature in enumerate(result.get("features", []), 1):
            st.write(f"{i}. {feature}")

    # Display generated services
    with col2:
        st.markdown("### Services")
        for i, service in enumerate(result.get("services", []), 1):
            st.code(f"{i}. {service}")

    # -------------------------------
    # Architecture Configuration
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
    # Generated Code Preview
    # -------------------------------
    st.subheader("Generated Code Preview")

    # Loop through each service and show generated files
    for service, files in result.get("service_outputs", {}).items():
        with st.expander(service):

            # Controller Layer Code
            st.markdown("### Controller")
            st.code(files.get("controller_code", ""), language=language.lower())

            # Service Layer Code
            st.markdown("### Service")
            st.code(files.get("service_code", ""), language=language.lower())

            # Model Layer Code
            st.markdown("### Model")
            st.code(files.get("model_code", ""), language=language.lower())

    # -------------------------------
    # Swagger Documentation Section
    # -------------------------------
    st.subheader("Swagger Documentation")

    for service, swagger in result.get("swagger_outputs", {}).items():
        with st.expander(service):
            st.code(swagger.get("content", ""), language="yaml")

    # -------------------------------
    # Unit Tests Section
    # -------------------------------
    st.subheader("Unit Tests")

    for service, test in result.get("test_outputs", {}).items():
        with st.expander(service):
            st.code(test.get("content", ""), language=language.lower())

    st.subheader("Frontend Code")

    for service, frontend in result.get("frontend_outputs", {}).items():
        with st.expander(service):
            st.code(frontend.get("content", ""), language="javascript")

    st.subheader("Project Documentation")

    st.text_area(
    "Generated Documentation",
    result.get("documentation_output", ""),
    height=400
    )
    zip_file = build_project_zip(result)
    st.subheader("Download Project")

    st.download_button(
    label="Download Full Project ZIP",
    data=zip_file,
    file_name="codecraft_project.zip",
    mime="application/zip"
)



