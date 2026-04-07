from state import CodeCrafterState
from agents.test_agent import generate_tests as generate_tests_func


async def test_node(state: CodeCrafterState) -> CodeCrafterState:
    return generate_tests_func(state)