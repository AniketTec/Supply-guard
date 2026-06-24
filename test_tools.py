from src.tools.analyst_tools import detect_delivery_delays, detect_demand_anomalies, score_region_risk
import pandas as pd


result_1 = detect_delivery_delays.invoke(
    {
        "threshold_days": 1
    }
)

print(result_1)

result_2 = detect_demand_anomalies.invoke(
    {
        "z_threshold": 2
    }
)
print(result_2)

result_3 = score_region_risk.invoke(
    {
        
    }
)
print(result_3)

