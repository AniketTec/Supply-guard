from src.tools.analyst_tools import detect_delivery_delays, detect_demand_anomalies, score_region_risk
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

tools = [
    detect_delivery_delays,
    detect_demand_anomalies,
    score_region_risk
]

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    api_key=google_api_key)

llm_groq = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=groq_api_key
)

analyst_agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""You are the SupplyGuard Analyst Agent.

Your responsibility is to analyze structured supply-chain findings.

The analysis tools have already produced verified numerical findings.

Do not recalculate any values.

Your task is to identify the most important operational risks,
patterns and observations.

Provide a concise operational summary that another agent can use
to prepare an executive report.
"""
)


if __name__ == "__main__":

    result = analyst_agent.invoke(
        {"messages": [{"role": "user", "content": "Analyze this supply chain data for risks. Identify: - delivery delays, - demand anomalies, - risky regions?"}]}
    )


    print(result["messages"][-1].content)