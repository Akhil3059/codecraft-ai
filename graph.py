from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages  
from typing import Dict
import os


from state import CodeCrafterState

from agents.planning_agent import planning_agent
from agents.codegen_agent import codegen_agent
from agents.swagger_agent import swagger_agent
from agents.test_agent import generate_tests
from agents.frontend_agent import frontend_agent
from agents.documentation_agent import documentation_agent


def create_codecrafter_graph():
    """
    Creates and compiles a LangGraph workflow that orchestrates
    multiple agents (planning → codegen → swagger → tests).

    Returns:
        Compiled graph object ready to be executed.
    """

    # Initialize the graph with a predefined state schema
    builder = StateGraph(CodeCrafterState)

    # Register nodes (each node represents an agent step in the pipeline)
    builder.add_node("planning", planning_agent)   # Converts user story into structured plan
    builder.add_node("codegen", codegen_agent)     # Generates actual service code
    builder.add_node("swagger", swagger_agent)     # Generates API documentation (Swagger/OpenAPI)
    builder.add_node("tests", generate_tests)      # Generates test cases for the services
    builder.add_node("frontend", frontend_agent)
    builder.add_node("documentation", documentation_agent)

    # Define where execution starts
    builder.set_entry_point("planning")

    # Define execution flow (directed edges between nodes)
    builder.add_edge("planning", "codegen")  # Planning output feeds into code generation
    builder.add_edge("codegen", "swagger")  # Generated code used for API docs
    builder.add_edge("swagger", "tests")    # Swagger used to derive test cases
    builder.add_edge("tests", "frontend")
    builder.add_edge("frontend", "documentation")

    # Define the final step of the workflow
    builder.set_finish_point("documentation")

    # Compile the graph into an executable workflow
    return builder.compile()


def run_all_agents(user_story: str, language: str) -> Dict:
    """
    Executes the full CodeCrafter pipeline:
    1. Planning
    2. Code generation
    3. Swagger generation
    4. Test generation

    Args:
        user_story (str): Functional requirement or feature description.
        language (str): Target programming language.

    Returns:
        Dict: Final state containing outputs from all stages.
    """

    # Initial state passed into the graph
    # This acts as shared memory between all agents
   

    initial_state = {
        "user_story": user_story,
        "language": language,

        "features": [],
        "services": [],
        "architecture_hints": {},
        "architecture_config": {},

        "service_outputs": {},
        "swagger_outputs": {},
        "test_outputs": {},
        "frontend_outputs": {},

        "documentation_output": "",

        "planning_complete": False,
        "codegen_complete": False,
        "swagger_complete": False,
        "tests_complete": False,
        "frontend_complete": False,
        "documentation_complete": False,

        "planning_error": "",
        "codegen_error": "",
        "swagger_error": "",
        "test_error": "",
        "frontend_error": "",
        "documentation_error": ""
    }

    graph = create_codecrafter_graph()

    result = graph.invoke(initial_state)

    return result