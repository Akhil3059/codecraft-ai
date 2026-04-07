from state import CodeCrafterState
from agents.planning_agent import planning_agent as planning_agent_func


async def planning_node(state: CodeCrafterState) -> CodeCrafterState:
    return planning_agent_func(state)