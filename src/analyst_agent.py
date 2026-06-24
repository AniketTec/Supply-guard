from src.tools.analyst_tools import detect_delivery_delays, detect_demand_anomalies, score_region_risk
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")

tools = [
    detect_delivery_delays,
    detect_demand_anomalies,
    score_region_risk
]

llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    api_key=google_api_key)



analyst_agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""You are the SupplyGuard Analyst Agent.

Your job is to analyze supply chain risks using the available tools.

You MUST return ONLY valid JSON.

Do NOT summarize.
Do NOT explain.
Do NOT add markdown.

The JSON MUST follow this exact schema.

{
"delivery_delays": [
{
"Region": "",
"Category": "",
"Total Orders": 0,
"Delayed Orders": 0,
"Delay Rate": 0,
"Average Delay": 0,
"Severity Score": 0
}
],

"demand_anomalies": [
{
"Product": "",
"Date": "",
"Actual Quantity": 0,
"Expected Quantity": 0,
"Demand Change (%)": 0,
"Z Score": 0,
"Anomaly Type": ""
}
],

"region_risks": [
{
"Region": "",
"Total Orders": 0,
"Late Orders": 0,
"Cancelled Orders": 0,
"Late Rate": 0,
"Cancellation Rate": 0,
"Raw Risk Score": 0,
"Risk Score": 0
}
]
}

IMPORTANT:

Preserve every field name EXACTLY as written above.

Do not rename fields.

Do not convert spaces to underscores.

Do not change capitalization.

Do not add or remove fields.

Return only the JSON object.

"""
)


if __name__ == "__main__":

    result = analyst_agent.invoke(
        {"messages": [{"role": "user", "content": "Analyze this supply chain data for risks. Identify: - delivery delays, - demand anomalies, - risky regions?"}]}
    )


    print(result["messages"][-1].content)