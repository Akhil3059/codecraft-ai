from state import CodeCrafterState
from agents.codegen_agent import codegen_agent as codegen_agent_func


async def codegen_node(state: CodeCrafterState) -> CodeCrafterState:
    return codegen_agent_func(state)