import states

from langgraph.graph import END
from langgraph.types import Send
from langchain_core.messages import AIMessage, HumanMessage


def should_regenerate_anlysts(state: states.AnalystsGenerationState):
    """Return the next node to execute"""
    # Check if human feedback
    human_analyst_feedback = state.get("human_analyst_feedback", None)
    if human_analyst_feedback:
        return "create_analysts"

    # Otherwise end
    return END


def should_continue_interview(state: states.InterviewState):
    """Decide if the interview should be saved or continued"""

    # Get messages
    messages = state["messages"]
    max_num_turns = state.get("max_num_turns", 2)

    # Check the number of expert answers
    num_responses = len([m for m in messages if isinstance(m, AIMessage) and m.name == "expert"])

    # End if expert has answered more than the max turns
    if num_responses >= max_num_turns:
        return "save_interview"

    # This router is run after each question - answer pair
    # Get the last question asked to check if it signals the end of discussion
    last_question = messages[-2]

    if "Thank you so much for your help" in last_question.content:
        return "save_interview"
    return "ask_question"


def route_interviews(state: states.ResearchState):
    """This is a routing function meant as the "map" step where we run each
    interview sub-graph in parallel using Send() API"""

    topic = state["topic"]
    # Kick off interviews in parallel via Send() API
    return [
        Send(
            node="conduct_interviews",
            arg={
                "analyst": analyst,
                "messages": [HumanMessage(content=f"So you said you were writing an article on {topic}?")],
                "max_num_turns": 2,
            },
        )
        for analyst in state["analysts"]
    ]
