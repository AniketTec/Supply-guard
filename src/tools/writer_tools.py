from langchain.tools import tool

# findings = {
#     "delivery_delays": [{'Region': 'Western Europe', 'Category': 'Cleats', 'Total Orders': 3690, 'Delayed Orders': 900, 'Delay Rate': 24.39, 'Average Delay': 2.54, 'Severity Score': 509.07}, {'Region': 'Western Europe', 'Category': "Men's Footwear", 'Total Orders': 3242, 'Delayed Orders': 796, 'Delay Rate': 24.55, 'Average Delay': 2.52, 'Severity Score': 499.22}, {'Region': 'Central America', 'Category': 'Cleats', 'Total Orders': 4035, 'Delayed Orders': 1001, 'Delay Rate': 24.81, 'Average Delay': 2.42, 'Severity Score': 498.39}, {'Region': 'Central America', 'Category': 'Indoor/Outdoor Games', 'Total Orders': 3239, 'Delayed Orders': 795, 'Delay Rate': 24.54, 'Average Delay': 2.49, 'Severity Score': 493.63}, {'Region': 'Western Europe', 'Category': "Women's Apparel", 'Total Orders': 3165, 'Delayed Orders': 753, 'Delay Rate': 23.79, 'Average Delay': 2.55, 'Severity Score': 489.22}, {'Region': 'Central America', 'Category': "Women's Apparel", 'Total Orders': 3404, 'Delayed Orders': 815, 'Delay Rate': 23.94, 'Average Delay': 2.51, 'Severity Score': 488.36}, {'Region': 'Western Europe', 'Category': 'Indoor/Outdoor Games', 'Total Orders': 2742, 'Delayed Orders': 663, 'Delay Rate': 24.18, 'Average Delay': 2.54, 'Severity Score': 486.21}, {'Region': 'Western Europe', 'Category': 'Fishing', 'Total Orders': 2606, 'Delayed Orders': 637, 'Delay Rate': 24.44, 'Average Delay': 2.52, 'Severity Score': 484.15}, {'Region': 'Western Europe', 'Category': 'Water Sports', 'Total Orders': 2359, 'Delayed Orders': 572, 'Delay Rate': 24.25, 'Average Delay': 2.57, 'Severity Score': 483.63}, {'Region': 'Central America', 'Category': "Men's Footwear", 'Total Orders': 3620, 'Delayed Orders': 875, 'Delay Rate': 24.17, 'Average Delay': 2.42, 'Severity Score': 480.13}],

#     "demand_anomalies": [{'Product': 'Bag Boy Beverage Holder', 'Date': '2015-02-28', 'Actual Quantity': 1, 'Expected Quantity': 3.57, 'demand change (%)': -72.0, 'Z Score': -2.02, 'Anomaly Type': 'Drop'}, {'Product': 'Bag Boy Beverage Holder', 'Date': '2015-04-27', 'Actual Quantity': 2, 'Expected Quantity': 4.57, 'demand change (%)': -56.25, 'Z Score': -2.27, 'Anomaly Type': 'Drop'}, {'Product': 'Bag Boy Beverage Holder', 'Date': '2015-10-01', 'Actual Quantity': 5, 'Expected Quantity': 2.29, 'demand change (%)': 118.75, 'Z Score': 2.17, 'Anomaly Type': 'Spike'}, {'Product': 'Bridgestone e6 Straight Distance NFL Tennesse', 'Date': '2016-08-10', 'Actual Quantity': 4, 'Expected Quantity': 1.43, 'demand change (%)': 180.0, 'Z Score': 2.27, 'Anomaly Type': 'Spike'}, {'Product': 'Bridgestone e6 Straight Distance NFL Tennesse', 'Date': '2016-08-26', 'Actual Quantity': 1, 'Expected Quantity': 4.14, 'demand change (%)': -75.86, 'Z Score': -2.15, 'Anomaly Type': 'Drop'}, {'Product': "Brooks Women's Ghost 6 Running Shoe", 'Date': '2017-07-26', 'Actual Quantity': 1, 'Expected Quantity': 3.57, 'demand change (%)': -72.0, 'Z Score': -2.02, 'Anomaly Type': 'Drop'}, {'Product': 'Clicgear 8.0 Shoe Brush', 'Date': '2016-03-07', 'Actual Quantity': 4, 'Expected Quantity': 2.0, 'demand change (%)': 100.0, 'Z Score': 2.0, 'Anomaly Type': 'Spike'}, {'Product': 'Clicgear 8.0 Shoe Brush', 'Date': '2016-09-07', 'Actual Quantity': 5, 'Expected Quantity': 2.43, 'demand change (%)': 105.88, 'Z Score': 2.02, 'Anomaly Type': 'Spike'}, {'Product': 'Clicgear Rovic Cooler Bag', 'Date': '2016-02-29', 'Actual Quantity': 5, 'Expected Quantity': 2.14, 'demand change (%)': 133.33, 'Z Score': 2.12, 'Anomaly Type': 'Spike'}, {'Product': 'Clicgear Rovic Cooler Bag', 'Date': '2016-07-06', 'Actual Quantity': 5, 'Expected Quantity': 3.14, 'demand change (%)': 59.09, 'Z Score': 2.06, 'Anomaly Type': 'Spike'}],

#     "region_risks": [{'Region': 'Central Africa', 'Total Orders': 1677, 'Late Orders': 972, 'Cancelled Orders': 33, 'Late Rate': 57.96, 'Cancellation Rate': 1.97, 'Raw Risk Score': 41.16, 'Risk Score': 1.0}, {'Region': 'South of  USA ', 'Total Orders': 4045, 'Late Orders': 2256, 'Cancelled Orders': 124, 'Late Rate': 55.77, 'Cancellation Rate': 3.07, 'Raw Risk Score': 39.96, 'Risk Score': 0.809}, {'Region': 'South Asia', 'Total Orders': 7731, 'Late Orders': 4350, 'Cancelled Orders': 132, 'Late Rate': 56.27, 'Cancellation Rate': 1.71, 'Raw Risk Score': 39.9, 'Risk Score': 0.799}, {'Region': 'East Africa', 'Total Orders': 1852, 'Late Orders': 1036, 'Cancelled Orders': 40, 'Late Rate': 55.94, 'Cancellation Rate': 2.16, 'Raw Risk Score': 39.81, 'Risk Score': 0.785}, {'Region': 'Western Europe', 'Total Orders': 27109, 'Late Orders': 15140, 'Cancelled Orders': 537, 'Late Rate': 55.85, 'Cancellation Rate': 1.98, 'Raw Risk Score': 39.69, 'Risk Score': 0.766}, {'Region': 'East of USA', 'Total Orders': 6915, 'Late Orders': 3849, 'Cancelled Orders': 148, 'Late Rate': 55.66, 'Cancellation Rate': 2.14, 'Raw Risk Score': 39.61, 'Risk Score': 0.753}, {'Region': 'Southeast Asia', 'Total Orders': 9539, 'Late Orders': 5297, 'Cancelled Orders': 216, 'Late Rate': 55.53, 'Cancellation Rate': 2.26, 'Raw Risk Score': 39.55, 'Risk Score': 0.744}, {'Region': 'Eastern Europe', 'Total Orders': 3920, 'Late Orders': 2182, 'Cancelled Orders': 61, 'Late Rate': 55.66, 'Cancellation Rate': 1.56, 'Raw Risk Score': 39.43, 'Risk Score': 0.725}, {'Region': 'West Asia', 'Total Orders': 6009, 'Late Orders': 3322, 'Cancelled Orders': 116, 'Late Rate': 55.28, 'Cancellation Rate': 1.93, 'Raw Risk Score': 39.28, 'Risk Score': 0.701}, {'Region': 'US Center ', 'Total Orders': 5887, 'Late Orders': 3252, 'Cancelled Orders': 113, 'Late Rate': 55.24, 'Cancellation Rate': 1.92, 'Raw Risk Score': 39.24, 'Risk Score': 0.694}]
# }

# def get_sample_findings():
#     return findings



@tool
def rank_by_severity(findings: dict, top_n: int = 5):
    
    """Rank findings within each category by severity.

Inputs:
    findings:
        Dictionary containing:
        - delivery_delays
        - demand_anomalies
        - region_risks

    top_n:
        Number of records to keep from each category.

Returns:
    Dictionary containing ranked findings."""

    print("=" * 50)

    print(findings.keys())

    print(findings["delivery_delays"][0])

    print(findings["demand_anomalies"][0])

    print(findings["region_risks"][0])

    print("=" * 50)

    ranked_findings = {}

    delivery_delays = findings.get(
        "delivery_delays",
        []
    )

    print(findings["delivery_delays"][0])

    ranked_findings["delivery_delays"] = sorted(
        delivery_delays,
        key=lambda x: x["Severity Score"],
        reverse=True
    )[:top_n]

    demand_anomalies = findings.get(
        "demand_anomalies",
        []
    )

    ranked_findings["demand_anomalies"] = sorted(
        demand_anomalies,
        key=lambda x: abs(x["Z Score"]),
        reverse=True
    )[:top_n]

    region_risks = findings.get(
        "region_risks",
        []
    )

    ranked_findings["region_risks"] = sorted(
        region_risks,
        key=lambda x: x["Risk Score"],
        reverse=True
    )[:top_n]
    

    return ranked_findings



@tool
def format_briefing(ranked_findings: dict):
    
    """
Convert ranked findings into a markdown briefing.

Inputs:
    ranked_findings:
        Output from rank_by_severity()

Returns:
    Markdown string.
"""
    
    # ranked_findings = rank_by_severity.invoke({ "findings": ranked_findings })

    briefing = "# SupplyGuard Risk Briefing\n\n"

    briefing += "## High Risk Regions\n\n"

    for risk in ranked_findings["region_risks"]:

        briefing += (
            f"- **{risk['Region']}** "
            f"(Risk Score: {risk['Risk Score']})\n"
        )

    briefing += "\n"

    briefing += "## Delivery Delay Risks\n\n"

    for delay in ranked_findings["delivery_delays"]:

        briefing += (
            f"- **{delay['Category']}** in "
            f"**{delay['Region']}** "
            f"(Severity: {delay['Severity Score']}, "
            f"Delay Rate: {delay['Delay Rate']}%)\n"
        )

    briefing += "\n"

    briefing += "## Demand Anomalies\n\n"

    for anomaly in ranked_findings["demand_anomalies"]:

        briefing += (
            f"- **{anomaly['Product']}** "
            f"({anomaly['Anomaly Type']}) "
            f"(Z Score: {anomaly['Z Score']}, "
            f"Demand Change: "
            f"{anomaly['Demand Change (%)']}%)\n"
        )

    return briefing


    

