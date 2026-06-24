from langchain.agents import create_agent
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from src.tools.writer_tools import rank_by_severity, format_briefing



load_dotenv()

tools = [
    rank_by_severity,
    format_briefing
]

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    api_key=os.getenv("GOOGLE_API_KEY")
)


writer_agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""You are the SupplyGuard Reporting Agent.

Your responsibility is to transform structured supply chain findings into clear executive briefings.

Prioritize operationally significant risks.

Focus on:
- High-risk regions
- Severe delivery delays
- Significant demand anomalies

Always:
- Start with an executive summary
- Highlight the most critical risks first
- Provide concise recommendations

Use the available tools to rank findings and generate a final markdown briefing.

Write for supply chain managers and operations leaders."""
)


if __name__ == "__main__":
    
    result = writer_agent.invoke(
        {"messages": [{"role": "user", "content": "Rank the findings by severity and generate a markdown briefing for the executive team."}]}
    )

    print(result)
