from typing import Annotated, List
from typing_extensions import TypedDict
from utils import Analyst
import operator

from langgraph.graph import MessagesState


# State for generating a roster of analysts for a topic
class AnalystsGenerationState(TypedDict):
    topic: str  # Research topic
    max_analysts: int  # Number of analysts
    human_analyst_feedback: str  # Human feedback
    analysts: List[Analyst]  # Analysts


# Per-analyst interview session state (extends MessagesState)
class InterviewState(MessagesState):
    max_num_turns: int  # Number turns of conversation (analyst-expert pair)
    context: Annotated[list, operator.add]  # Full source docs & links
    analyst: Analyst  # Analyst information
    interview: str  # Interview transcript
    sections: list  # Final key we duplicate in outer state for Send() API


# Global research workflow state aggregating analyst outputs and composing the final report.
class ResearchState(MessagesState):
    topic: str  # Research topic
    max_analysts: int  # Number of analysts
    human_analyst_feedback: str  # Human feedback

    analysts: List[Analyst]  # Analyst asking questions
    sections: Annotated[list, operator.add]  # Send() API key

    introduction: str  # Introduction for the final report
    content: str  # Content for the final report
    conclusion: str  # Conclusion for the final report
    final_report: str  # Final report


# Input schema for starting a research run (topic and desired number of analysts).
class ResearchInputSchema(TypedDict):
    topic: str  # Research topic
    max_analysts: int  # Number of analysts


# Output schema exposing the final compiled report text.
class ResearchOutputSchema(TypedDict):
    final_report: str  # Final report
