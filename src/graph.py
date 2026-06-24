from langgraph.graph import StateGraph, START, END
from src.state import AgentState
from src.analyst_agent import analyst_agent
from src.writer_agent import writer_agent

import json


# Supervisor Node

def supervisor_node(state: AgentState):

    """
    Decides which agent should run next.

    Routing Logic:

    No findings  -> Analyst

    Findings exist but no report
                 -> Writer

    Report exists
                 -> END
    """

    if not state.findings:

        state.next_agent = "analyst"

    elif not state.report:

        state.next_agent = "writer"

    else:

        state.next_agent = "end"

    return state



# Analyst Node


def analyst_node(state: AgentState):

    """
    Runs the Analyst Agent.

    The Analyst Agent:
    - calls analysis tools
    - gathers findings
    - returns structured JSON

    We convert the JSON string into a Python dictionary
    and store it in shared state.
    """

    result = analyst_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Analyze this supply chain data for risks. Identify: - delivery delays, - demand anomalies, - risky regions? "
                        "and return structured findings."
                    )
                }
            ]
        }
    )

    json_text = result["messages"][-1].content[0]["text"]

    structured_findings = json.loads(json_text)

    state.findings = structured_findings

    return state



# Writer Node


def writer_node(state: AgentState):

    """
    Runs the Writer Agent.

    Input:
        state.findings

    Output:
        state.report
    """

    findings = state.findings

    result = writer_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""
                    Here are the analyst findings:

                    {json.dumps(findings, indent=2)}

                    Rank the findings by severity and generate
                    an executive markdown briefing.
                    """
                }
            ]
        }
    )

    report = result["messages"][-1].content[0]["text"]
    print("Writer node reached")
    print(type(result["messages"][-1].content))

    state.report = report

    return state



# Routing Function


def route_from_supervisor(state: AgentState):

    """
    Reads the routing decision
    written by supervisor_node.
    """

    return state.next_agent



# Graph


graph_structure = StateGraph(AgentState)

graph_structure.add_node(
    "supervisor",
    supervisor_node
)

graph_structure.add_node(
    "analyst",
    analyst_node
)

graph_structure.add_node(
    "writer",
    writer_node
)



# START


graph_structure.add_edge(
    START,
    "supervisor"
)



# Supervisor Routing


graph_structure.add_conditional_edges(
    "supervisor",
    route_from_supervisor,
    {
        "analyst": "analyst",
        "writer": "writer",
        "end": END
    }
)



# Return To Supervisor


graph_structure.add_edge(
    "analyst",
    "supervisor"
)

graph_structure.add_edge(
    "writer",
    "supervisor"
)



# Compile


graph = graph_structure.compile()



# Test Run


if __name__ == "__main__":

    initial_state = AgentState(
        messages=[],
        findings={},
        report=None,
        next_agent=None
    )

    result = graph.invoke(initial_state)

    print("\n")
    print("=" * 80)
    print("FINAL REPORT")
    print("=" * 80)
    print("\n")

    print(result["report"])