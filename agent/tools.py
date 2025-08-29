# The tools module
# Define your tools here

from langchain_anthropic import ChatAnthropic
from langchain_community.document_loaders import WikipediaLoader
from langchain_tavily import TavilySearch


# LLM
model = ChatAnthropic(model="claude-3-haiku-20240307", max_tokens=1014, temperature=0.5)

# Wikipedia search tool
# Here

# Tavily search tool
tavily_search = TavilySearch(max_results=1)
