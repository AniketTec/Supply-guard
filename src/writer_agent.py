from langchain.agents import create_agent
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from src.tools.writer_tools import rank_by_severity, format_briefing
from langchain_groq import ChatGroq




load_dotenv()

tools = [
    rank_by_severity,
    format_briefing
]

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    api_key=os.getenv("GOOGLE_API_KEY")
)

llm_groq = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)


writer_agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""You are the SupplyGuard Reporting Agent.

The findings supplied to you are verified outputs generated
by analytical tools.

Never modify numerical values.

Your job is to:

• rank findings by severity

• create an executive markdown report

Use the available tools whenever appropriate.

Write clearly for operations managers."""
)


if __name__ == "__main__":
    
    result = writer_agent.invoke(
        {"messages": [{"role": "user", "content": "Rank the findings by severity and generate a markdown briefing for the executive team."}]}
    )

    print(result)
