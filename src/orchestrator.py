from typing import Literal

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from agents import AgentState, analyst_node, researcher_node, writer_node


def human_approval_node(state: AgentState):
    """Pause point for human-in-the-loop review."""
    return state


def route_after_human(state: AgentState) -> Literal["Writer", "__end__"]:
    """Route to writer for revisions unless human explicitly approves."""
    last_msg = state["messages"][-1].content.lower()
    if "approve" in last_msg:
        return "__end__"
    return "Writer"


workflow = StateGraph(AgentState)

workflow.add_node("Researcher", researcher_node)
workflow.add_node("Analyst", analyst_node)
workflow.add_node("Writer", writer_node)
workflow.add_node("human_approval", human_approval_node)

workflow.set_entry_point("Researcher")
workflow.add_edge("Researcher", "Analyst")
workflow.add_edge("Analyst", "Writer")
workflow.add_edge("Writer", "human_approval")
workflow.add_conditional_edges("human_approval", route_after_human)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory, interrupt_before=["human_approval"])
