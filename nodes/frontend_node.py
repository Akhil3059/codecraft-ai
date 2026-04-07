from state import CodeCrafterState
from agents.frontend_agent import frontend_agent as frontend_agent_func


async def frontend_node(state: CodeCrafterState) -> CodeCrafterState:
    return frontend_agent_func(state)