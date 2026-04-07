from state import CodeCrafterState
from agents.documentation_agent import documentation_agent as documentation_agent_func


async def documentation_node(state: CodeCrafterState) -> CodeCrafterState:
    return documentation_agent_func(state)