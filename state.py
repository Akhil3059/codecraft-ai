from typing import Dict, List, TypedDict
import os
import re



class CodeCrafterState(TypedDict):
    """
    Defines the shared state structure used across all agents
    in the CodeCrafter pipeline.

    This acts as a contract ensuring all agents read/write
    consistent keys during execution.
    """

    # Input fields
    user_story: str              # User requirement or feature description
    language: str                # Target programming language

    # Planning outputs
    features: List[str]          # Extracted features from the user story
    services: List[str]          # Identified microservices/modules
    architecture_hints: Dict     # Suggestions for system design
    architecture_config: Dict    # Finalized architecture structure

    # Error tracking per stage
    planning_error: str
    service_outputs: Dict        # Generated service code files
    codegen_error: str
    swagger_outputs: Dict        # Generated Swagger/OpenAPI specs
    swagger_error: str
    test_outputs: Dict           # Generated test cases
    test_error: str

    # Output configuration
    output_base: str             # Base directory (e.g., "output")
    output_dir: str              # Final resolved output path

    # Execution status flags
    planning_complete: bool
    codegen_complete: bool
    swagger_complete: bool
    tests_complete: bool
    error_occurred: bool         # Global error flag

    frontend_outputs: Dict
    frontend_complete: bool
    frontend_error: str

    documentation_output: str
    documentation_complete: bool
    documentation_error: str

def get_file_extension(language: str) -> str:
    """
    Returns the appropriate file extension for a given programming language.

    This helps standardize file generation across multiple languages.

    Args:
        language (str): Programming language name

    Returns:
        str: File extension (without dot)
    """

    # Mapping of language → file extension
    mapping = {
        "Java": "java",
        "NodeJS": "js",
        ".NET": "cs",
        "Python": "py",
        "Go": "go",
        "Ruby": "rb",
        "PHP": "php",
        "Kotlin": "kt"
    }

    # Default to 'txt' if language is unknown (safe fallback)
    return mapping.get(language, "txt")