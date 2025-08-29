import states
import nodes
import routes

from langgraph.graph import StateGraph, START, END


# Analysts generation sub-graph =============================================================
# Initialization
analysts_flow = StateGraph(states.AnalystsGenerationState)

# Add nodes and edges
analysts_flow.add_node("create_analysts", nodes.create_analysts)
analysts_flow.add_node("get_human_feedback", nodes.get_human_feedback)

analysts_flow.add_edge(START, "create_analysts")
analysts_flow.add_edge("create_analysts", "get_human_feedback")
analysts_flow.add_conditional_edges("get_human_feedback", routes.should_regenerate_anlysts, ["create_analysts", END])

# Compile
graph = analysts_flow.compile(interrupt_after=["get_human_feedback"], name="Generate Analysts")


# Interviews sub-graph =======================================================================
# Initialization
interview_flow = StateGraph(states.InterviewState)

# Add nodes and edges
interview_flow.add_node("ask_question", nodes.generate_question)
interview_flow.add_node("search_web", nodes.search_tavily)
interview_flow.add_node("search_wikipedia", nodes.search_wikipedia)
interview_flow.add_node("answer_question", nodes.answer_question)
interview_flow.add_node("save_interview", nodes.save_interview)
interview_flow.add_node("write_section", nodes.write_section)

interview_flow.add_edge(START, "ask_question")
interview_flow.add_edge("ask_question", "search_web")
interview_flow.add_edge("ask_question", "search_wikipedia")
interview_flow.add_edge("search_web", "answer_question")
interview_flow.add_edge("search_wikipedia", "answer_question")
interview_flow.add_conditional_edges(
    "answer_question", routes.should_continue_interview, ["save_interview", "ask_question"]
)
interview_flow.add_edge("save_interview", "write_section")
interview_flow.add_edge("write_section", END)

# Compile
interview_graph = interview_flow.compile(name="Conduct Interview")


# Full Research graph =========================================================================
# Initialization
workflow = StateGraph(
    state_schema=states.ResearchState,
    input_schema=states.ResearchInputSchema,
    output_schema=states.ResearchOutputSchema,
)

# Add nodes and edges
workflow.add_node("call_analysts", analysts_flow.compile())
workflow.add_node("conduct_interviews", interview_flow.compile())
workflow.add_node("write_report_content", nodes.write_report_content)
workflow.add_node("write_report_introduction", nodes.write_report_introduction)
workflow.add_node("write_report_conclusion", nodes.write_report_conclusion)
workflow.add_node("finalize_report", nodes.finalize_report)

workflow.add_edge(START, "call_analysts")
workflow.add_conditional_edges("call_analysts", routes.route_interviews, ["conduct_interviews"])
workflow.add_edge("conduct_interviews", "write_report_content")
workflow.add_edge("conduct_interviews", "write_report_introduction")
workflow.add_edge("conduct_interviews", "write_report_conclusion")
workflow.add_edge(["write_report_introduction", "write_report_content", "write_report_conclusion"], "finalize_report")
workflow.add_edge("finalize_report", END)

# Compile
research_graph = workflow.compile(name="Research Assistant")
