from state import CodeCrafterState
from agents.swagger_agent import swagger_agent as swagger_agent_func


async def swagger_node(state: CodeCrafterState) -> CodeCrafterState:
    return swagger_agent_func(state)