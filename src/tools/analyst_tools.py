import pandas as pd
import math
from langchain.tools import tool


def load_data():
    df = pd.read_csv(
        "data/dataco.csv",
        encoding="ISO-8859-1"
    )
    return df

@tool
def detect_delivery_delays(threshold_days: int):
    """
Analyze delivery performance across regions and product categories.

This tool identifies region-category combinations with the highest delivery delay risk.
An order is considered delayed when the actual shipping duration exceeds the scheduled
shipping duration by more than the provided threshold.

Inputs:
    threshold_days:
        Minimum number of delay days required for an order to be classified as delayed.

Returns:
    List of dictionaries ranked by severity score.

Each result contains:
    - Region
    - Category
    - Total Orders
    - Delayed Orders
    - Delay Rate
    - Average Delay
    - Severity Score

Use this tool when investigating delivery performance issues,
shipping bottlenecks, or categories experiencing excessive delays.
"""
    df = load_data()

    analysis_df = df.copy()

    analysis_df["delay_days"] = (
        analysis_df["Days for shipping (real)"]
        - analysis_df["Days for shipment (scheduled)"]
    )

    results = []

    for (region, category), group in analysis_df.groupby(
        ["Order Region", "Category Name"]
    ):

        total_orders = len(group)

        delayed_group = group[group["delay_days"] > threshold_days]

        delayed_orders = len(delayed_group)

        if delayed_orders > 0:
            average_delay = delayed_group["delay_days"].mean()
        else:
            average_delay = 0
        

        if total_orders == 0:
            continue

        delay_rate = (delayed_orders / total_orders) * 100

        severity_score = delay_rate * average_delay * math.log(total_orders + 1)

        results.append(
            {
                "Region": region,
                "Category": category,
                "Total Orders": total_orders,
                "Delayed Orders": delayed_orders,
                "Delay Rate": round(delay_rate, 2),
                "Average Delay": float(round(average_delay, 2)),
                "Severity Score": float(round(severity_score, 2))
            }
        )

    results = sorted(
        results,
        key=lambda x: x["Severity Score"],
        reverse=True
    )

    return results[:10]


if __name__ == "__main__":
     df = pd.read_csv("data/dataco.csv", encoding="ISO-8859-1")

     print("delay_days" in df.columns)

     threshold_days = 1

     delay_results = detect_delivery_delays(threshold_days)

     print("delay_days" in df.columns)

     print(f"Top Regions and Categories with most delayed order frequency: {delay_results}")





@tool
def detect_demand_anomalies(z_threshold: int):
    """
Detect unusual product demand behavior using rolling statistical analysis.

This tool aggregates daily product demand and compares each day's sales quantity
against the product's recent historical behavior using rolling averages and
rolling standard deviations.

Demand anomalies are identified using a Z-score threshold.

Inputs:
    z_threshold:
        Minimum absolute Z-score required for a demand anomaly to be detected.

Returns:
    List of anomaly findings ranked by anomaly magnitude.

Each result contains:
    - Product
    - Date
    - Actual Quantity
    - Expected Quantity
    - Demand Change (%)
    - Z Score
    - Anomaly Type (Spike or Drop)

Use this tool when investigating unexpected demand spikes,
demand drops, inventory planning issues, or forecasting risks.
"""
    df = load_data()

    analysis_df = df.copy()

    analysis_df["order date (DateOrders)"] = pd.to_datetime(
        analysis_df["order date (DateOrders)"]
    )

    daily_demand = (analysis_df.groupby(["Product Name", "order date (DateOrders)"])["Order Item Quantity"].sum().reset_index())


    daily_demand = daily_demand.sort_values(
        ["Product Name", "order date (DateOrders)"]
    )

    daily_demand["rolling_mean"] = (daily_demand.groupby("Product Name")["Order Item Quantity"]
                                    .transform(lambda x: x.rolling(window=7, min_periods=3).mean()))

    
    daily_demand["rolling_std"] = (daily_demand.groupby("Product Name")["Order Item Quantity"]
                                   .transform(lambda x: x.rolling(window=7, min_periods=3).std()))


    daily_demand  = daily_demand[daily_demand["rolling_mean"] > 0]
    
    daily_demand["z_score"] = (
        (daily_demand["Order Item Quantity"] - daily_demand["rolling_mean"]) / daily_demand["rolling_std"]
    )

    daily_demand["demand change"] = (daily_demand["Order Item Quantity"] - daily_demand["rolling_mean"]) / daily_demand["rolling_mean"] * 100

    anomalies = daily_demand[
        abs(daily_demand["z_score"]) > z_threshold
    ]

    anomalies["Anomaly Type"] = anomalies["z_score"].apply(
        lambda x: "Spike" if x > 0 else "Drop"
    )

    

    results = []

    for _, row in anomalies.head(10).iterrows():

        results.append(
            {
                "Product": row["Product Name"],
                "Date": str(row["order date (DateOrders)"].date()),
                "Actual Quantity": int(row["Order Item Quantity"]),
                "Expected Quantity": round(row["rolling_mean"], 2),
                "demand change (%)": round(row["demand change"], 2),
                "Z Score": round(row["z_score"], 2),
                "Anomaly Type": row["Anomaly Type"]
            }
        )

    return results

if __name__ == "__main__":
    df = pd.read_csv("data/dataco.csv", encoding="ISO-8859-1")

    z_threshold = 2

    anomaly_results = detect_demand_anomalies(z_threshold)

    print(f"Top Demand Anomalies: {anomaly_results}")


@tool
def score_region_risk():
    """
Calculate operational risk scores for geographic regions.

This tool evaluates the overall risk level of each order region by combining
late delivery frequency and order cancellation frequency into a single
normalized risk score.

The resulting risk score is scaled between 0 and 1, where:

    0 = Lowest observed risk
    1 = Highest observed risk

Inputs:
    None

Returns:
    List of regions ranked by risk score.

Each result contains:
    - Region
    - Total Orders
    - Late Orders
    - Cancelled Orders
    - Late Rate
    - Cancellation Rate
    - Raw Risk Score
    - Risk Score

Use this tool when identifying high-risk geographic regions,
supply chain instability, or areas requiring operational intervention.
"""
    
    df = load_data()

    analysis_df = df.copy()

    results = []

    for region, group in analysis_df.groupby("Order Region"):

        total_orders = len(group)

        if total_orders == 0:
            continue

        late_orders = len(
            group[group["Delivery Status"] == "Late delivery"]
        )

        cancelled_orders = len(
            group[group["Order Status"] == "CANCELED"]
        )

        late_rate = (late_orders / total_orders) * 100

        cancellation_rate = (
            cancelled_orders / total_orders
        ) * 100

        raw_risk_score = (
            0.7 * late_rate
            +
            0.3 * cancellation_rate
        )

        results.append(
            {
                "Region": region,
                "Total Orders": total_orders,
                "Late Orders": late_orders,
                "Cancelled Orders": cancelled_orders,
                "Late Rate": round(late_rate, 2),
                "Cancellation Rate": round(cancellation_rate, 2),
                "Raw Risk Score": round(raw_risk_score, 2)
            }
        )

    min_risk = min(
        item["Raw Risk Score"]
        for item in results
    )

    max_risk = max(
        item["Raw Risk Score"]
        for item in results
    )

    for item in results:

        if max_risk == min_risk:
            item["Risk Score"] = 0

        else:
            item["Risk Score"] = round(
                (item["Raw Risk Score"] - min_risk) /
                (max_risk - min_risk),
                3
)

    results = sorted(
        results,
        key=lambda x: x["Risk Score"],
        reverse=True
    )

    return results[:10]


if __name__ == "__main__":
    df = pd.read_csv("data/dataco.csv", encoding="ISO-8859-1")

    risk_results = score_region_risk(df)

    print(f"Top Regions with highest risk scores: {risk_results}")