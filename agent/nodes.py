# The nodes module
# Define your nodes here

from tools import model, tavily_search, WikipediaLoader
from utils import Perspectives, SearchQuery
import prompts
import states

from langchain_core.messages import HumanMessage, SystemMessage, get_buffer_string


# Nodes definition for analysts sub-graph ================================


def create_analysts(state: states.AnalystsGenerationState):
    """Node to create analysts"""
    topic = state["topic"]
    max_analysts = state["max_analysts"]
    human_analyst_feedback = state.get("human_analyst_feedback", "no feedbacks")

    # instructions
    system_message = prompts.GENERATE_ANALYSTS_PROMPT.format(
        topic=topic, human_analyst_feedback=human_analyst_feedback, max_analysts=max_analysts
    )
    system_message = SystemMessage(content=system_message)
    human_message = HumanMessage(content="Generate the set of analysts.")

    # Enforce structured output
    analysts = model.with_structured_output(Perspectives).invoke([system_message, human_message])

    # Write the list of analysis to state
    return {"analysts": analysts.analysts}


def get_human_feedback(state: states.AnalystsGenerationState):
    """Node to get human feedback about the generated analysts"""
    return {"human_analyst_feedback": None}


# Nodes definition for interview sub-graph ================================


def generate_question(state: states.InterviewState):
    """Node to ask a question by the analyst"""

    # Get state
    analyst = state["analyst"]
    messages = state["messages"]

    # Generate question
    system_message = prompts.ASK_QUESTION_PROMPT.format(analyst_persona=analyst.persona)
    question = model.invoke([SystemMessage(content=system_message)] + messages)

    # Write messages to state as a human (for later formatting)
    return {"messages": [HumanMessage(content=question.content)]}


def search_tavily(state: states.InterviewState):
    """Node to search the web"""

    try:
        # Search query
        system_message = SystemMessage(content=prompts.INFER_QUERY_PROMPT)
        search_query = model.with_structured_output(SearchQuery).invoke([system_message] + state["messages"])

        # Search
        search_results = tavily_search.invoke(search_query.search_query)["results"]
    except Exception as e:
        search_results = []

    # Format
    formatted_search_docs = "\n\n".join(
        [
            (f'url: {doc["url"]}\n' f'document title: {doc["title"]}\n' f'document content: {doc["content"]}\n')
            for doc in search_results
        ]
    )

    return {"context": [formatted_search_docs]}


def search_wikipedia(state: states.InterviewState):
    """Node to search wikipedia"""

    try:
        # Search query
        system_message = SystemMessage(content=prompts.INFER_QUERY_PROMPT)
        search_query = model.with_structured_output(SearchQuery).invoke([system_message] + state["messages"])

        # Search
        search_docs = WikipediaLoader(query=search_query.search_query, load_max_docs=1).load()
    except Exception as e:
        search_docs = []

    # Format
    formatted_search_docs = "\n\n".join(
        [
            (
                f'source: {doc.metadata["source"]}\n'
                f'page: {doc.metadata.get("page", "")}\n'
                f"content: {doc.page_content}\n"
            )
            for doc in search_docs
        ]
    )

    return {"context": [formatted_search_docs]}


def answer_question(state: states.InterviewState):
    """Node to answer a question by the expert"""

    # Get state
    analyst = state["analyst"]
    messages = state["messages"]
    context = state["context"]

    # Answer question
    system_message = prompts.ANSWER_QUESTION_PROMPT.format(analyst_persona=analyst.persona, context=context)
    answer = model.invoke([SystemMessage(content=system_message)] + messages)

    # Name the message as coming from the expert
    answer.name = "expert"

    # Add to messages channel
    return {"messages": [answer]}


from langchain_core.messages import get_buffer_string


def save_interview(state: states.InterviewState):
    """Node to save the full interview as a string"""

    # Get messages
    messages = state["messages"]

    # Convert interview to a string
    interview = get_buffer_string(
        messages=messages,
        human_prefix="Analyst",  # that's why we saved analyst question as human before
        ai_prefix="Expert",
    )

    # Save to interviews key
    return {"interview": interview}


def write_section(state: states.InterviewState):
    """Node to answer a question"""

    # Get the documents and the analyst information
    context = state["context"]
    analyst = state["analyst"]

    # Write section using either the gathered source docs from interview (context) or the interview itself (interview)
    system_message = prompts.WRITE_SECTION_PROMPT.format(analyst_persona=analyst.persona)
    section = model.invoke(
        [SystemMessage(content=system_message)]
        + [HumanMessage(content=f"Use this source to write your section: {context}")]
    )

    # Append it to state
    return {"sections": [section.content]}


# Nodes definition for full research graph ================================


def write_report_content(state: states.ResearchState):
    """ "Node to write the content section of the final report based on the interviews sections"""

    # get necessary channels from the state
    sections = state["sections"]
    topic = state["topic"]

    # Concat all sections together into a single message
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])
    system_message = prompts.CREATE_REPORT_PROMPT.format(topic=topic, context=formatted_str_sections)
    system_message = SystemMessage(content=system_message)

    # Summarize the sections into a final report
    report = model.invoke([system_message] + [HumanMessage(content=f"Write a report based upon these memos.")])
    return {"content": report.content}


def write_report_introduction(state: states.ResearchState):
    """Node to write the introduction section of the final report"""
    sections = state["sections"]
    topic = state["topic"]

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    # Summarize the sections into a final report
    instructions = prompts.CREATE_INTRO_OUTRO_PROMPT.format(topic=topic, formatted_str_sections=formatted_str_sections)
    intro = model.invoke(
        [SystemMessage(content=instructions)] + [HumanMessage(content=f"Write the report introduction")]
    )
    return {"introduction": intro.content}


def write_report_conclusion(state: states.ResearchState):
    """Node to write the conclusion section of the final report"""
    sections = state["sections"]
    topic = state["topic"]

    # Concat all sections together
    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])

    # Summarize the sections into a final report
    instructions = prompts.CREATE_INTRO_OUTRO_PROMPT.format(topic=topic, formatted_str_sections=formatted_str_sections)
    conclusion = model.invoke(
        [SystemMessage(content=instructions)] + [HumanMessage(content=f"Write the report conclusion")]
    )
    return {"conclusion": conclusion.content}


def finalize_report(state: states.ResearchState):
    """Node to finalize the report and make it presentable"""

    # Save full final report
    content = state["content"]
    if content.startswith("## Insights"):
        content = content.strip("## Insights")
    if "## Sources" in content:
        try:
            content, sources = content.split("\n## Sources\n")
        except:
            sources = None
    else:
        sources = None

    final_report = state["introduction"] + "\n\n---\n\n" + content + "\n\n---\n\n" + state["conclusion"]
    if sources is not None:
        final_report += "\n\n## Sources\n" + sources
    return {
        "final_report": final_report,
        "messages": [final_report],  # Overwrite messages with final report for easy viewing in UI
    }
