# SupplyGuard

A multi-agent supply chain risk intelligence system built with LangGraph and FastAPI.

SupplyGuard autonomously analyzes supply chain data, detects operational risks across three dimensions — delivery delays, demand anomalies, and regional risk — and generates a structured executive briefing via a REST API.

---

## What it does

A single `POST /analyze` request triggers a LangGraph multi-agent workflow:

1. A **Supervisor** evaluates shared state and decides which agent acts next
2. An **Analyst Agent** runs three pandas-based analytical tools and produces structured findings
3. A **Writer Agent** ranks those findings by severity and formats them into a markdown executive briefing
4. The final report is returned as a JSON API response

No manual orchestration. The agents decide their own tool call order using a ReAct reasoning loop.

---

## Architecture

```
┌─────────────────────────────┐
│     FastAPI  POST /analyze  │
└──────────────┬──────────────┘
               │
               ▼
┌──────────────────────────────┐
│        Supervisor Node       │
│  Reads state → routes next   │
└───────┬──────────────────────┘
        │
        ▼
┌───────────────────┐
│   Analyst Agent   │  ← ReAct loop (reason + act)
│  (Gemini Flash)   │
└──┬────────┬───────┘
   │        │        │
   ▼        ▼        ▼
Delivery  Demand   Region
 Delays  Anomaly    Risk
  Tool    Tool      Tool
   │        │        │
   └────────┴────────┘
               │
               ▼
       Shared AgentState
      { findings: { ... } }
               │
               ▼
┌───────────────────┐
│   Writer Agent    │  ← ReAct loop
│  (Gemini Flash)   │
└──┬────────────────┘
   │              │
   ▼              ▼
rank_by_      format_
severity()    briefing()
               │
               ▼
   Executive Markdown Report
               │
               ▼
┌──────────────────────────────┐
│       FastAPI Response       │
│  { report, findings, risks } │
└──────────────────────────────┘
```

**Key architectural pattern:** Supervisor → Analyst → Supervisor → Writer → Supervisor → END

The supervisor runs after every agent. It re-evaluates state each time and decides whether to route forward, retry, or terminate. This is a proper LangGraph supervisor pattern — not a fixed pipeline.

---

## Tech stack

| Layer | Tool | Purpose |
|---|---|---|
| Language | Python 3.11 | — |
| Agent framework | LangGraph | Supervisor pattern, state graph, conditional edges |
| LLM framework | LangChain | `@tool` decorator, agent creation, LLM abstraction |
| LLM | Google Gemini 1.5 Flash | Analyst reasoning, Writer reasoning, tool selection |
| API | FastAPI + Uvicorn | REST endpoint, Swagger UI, request/response validation |
| Data analysis | Pandas | CSV loading, groupby, rolling statistics, feature engineering |
| Validation | Pydantic | AgentState, request/response models |
| Environment | python-dotenv | API key management |
| Dataset | DataCo Smart Supply Chain | 180k order records (Kaggle, free) |

---

## Folder structure

```
supplyguard/
├── api/
│   └── main.py              # FastAPI app, /analyze endpoint
├── src/
│   ├── tools/
│   │   ├── analyst_tools.py # detect_delivery_delays, detect_demand_anomalies, score_region_risk
│   │   └── writer_tools.py  # rank_by_severity, format_briefing
│   ├── analyst_agent.py     # ReAct agent bound to analyst tools
│   ├── writer_agent.py      # ReAct agent bound to writer tools
│   ├── graph.py             # LangGraph StateGraph: nodes, edges, supervisor routing
│   └── state.py             # AgentState TypedDict (shared state schema)
├── data/
│   └── dataco.csv           # DataCo Supply Chain dataset (not committed — see setup)
├── .env                     # GOOGLE_API_KEY (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## How the agents work

### Analyst Agent

Runs a **ReAct loop** — the LLM reasons about which tool to call, calls it, reads the result, reasons again, and repeats until it has output from all three tools.

**Tools:**

`detect_delivery_delays(threshold_days)` — identifies region-category pairs with the highest delivery delay frequency. Calculates a severity score using delay rate × average delay × log(order volume).

`detect_demand_anomalies(z_threshold)` — computes rolling 7-day mean and standard deviation per product. Flags any day where order quantity deviates beyond the z-score threshold.

`score_region_risk()` — computes a normalized 0–1 risk score per region combining late delivery rate (weighted 70%) and cancellation rate (weighted 30%).

### Writer Agent

Receives the structured findings dict from shared state. Runs two tools in sequence:

`rank_by_severity(findings_json)` — sorts each category (delays, anomalies, regions) by its primary severity metric and returns the top N.

`format_briefing(ranked_findings_json)` — renders a structured markdown executive briefing with sections for regions, delays, and demand anomalies.

### Supervisor

A plain conditional function — no LLM involved. Reads two fields from state:

- `findings` empty → route to Analyst
- `findings` populated, `report` is None → route to Writer  
- Both populated → route to END

This keeps routing logic explicit, deterministic, and debuggable.

---

## Installation

**Prerequisites:** Python 3.11, a Google AI Studio account (free), the DataCo dataset from Kaggle.

```bash
# Clone the repo
git clone https://github.com/aniket-tec/supplyguard
cd supplyguard

# Create virtual environment
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your GOOGLE_API_KEY to .env
```

Get a free Gemini API key at [aistudio.google.com](https://aistudio.google.com). The free tier is sufficient — this project makes 5–15 LLM calls per analysis run.

Place the DataCo dataset CSV at `data/dataco.csv`. Download from [Kaggle: DataCo Smart Supply Chain](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis).

---

## Running locally

**Test each layer independently (recommended order):**

```bash
# 1. Verify analyst tools work (no LLM, just pandas)
python -m src.tools.analyst_tools

# 2. Test the analyst agent end-to-end
python -m src.analyst_agent

# 3. Test the writer agent with hardcoded findings
python -m src.writer_agent

# 4. Run the full graph
python -m src.graph

# 5. Start the API server
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`. Swagger UI is at `http://localhost:8000/docs`.

---

## API documentation

### `POST /analyze`

Triggers the full multi-agent analysis pipeline on the loaded dataset.

**Request body**

```json
{
  "dataset_path": "data/dataco.csv",
  "top_n_risks": 5
}
```

| Field | Type | Description |
|---|---|---|
| `dataset_path` | string | Path to the CSV dataset |
| `top_n_risks` | integer | Number of top risks to surface per category |

**Response**

```json
{
  "report": "# SupplyGuard Risk Briefing\n\n...",
  "findings": {
    "delivery_delays": [...],
    "demand_anomalies": [...],
    "region_risks": [...]
  }
}
```

| Field | Type | Description |
|---|---|---|
| `report` | string | Full markdown executive briefing |
| `findings` | object | Structured findings from the Analyst Agent, keyed by category |

**Status codes:** `200 OK` on success. `422 Unprocessable Entity` if request body is malformed.

---

## Example request

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"dataset_path": "data/dataco.csv", "top_n_risks": 5}'
```

---

## Example output

```markdown
# SupplyGuard Risk Briefing

This briefing outlines high-priority supply chain risks, ranked by severity
to support operational decision-making.

## High Risk Regions

1. **Central Africa** — Risk Score 1.0 (57.96% Late Rate)
2. **South of USA** — Risk Score 0.809 (55.77% Late Rate)
3. **South Asia** — Risk Score 0.799 (56.27% Late Rate)
4. **East Africa** — Risk Score 0.785 (55.94% Late Rate)
5. **Western Europe** — Risk Score 0.766 (55.85% Late Rate)

## Delivery Delay Risks

Priority areas requiring immediate mitigation:

* **Western Europe — Cleats**: Severity 509.07 (24.39% Delay Rate)
* **Western Europe — Men's Footwear**: Severity 499.22 (24.55% Delay Rate)
* **Central America — Cleats**: Severity 498.39 (24.81% Delay Rate)
* **Central America — Indoor/Outdoor Games**: Severity 493.63 (24.54% Delay Rate)
* **Western Europe — Women's Apparel**: Severity 489.22 (23.79% Delay Rate)

## Demand Anomalies

Significant demand spikes detected that may impact inventory replenishment:

* **Bridgestone e6 Straight Distance NFL Tennessee**: Spike (+180%, Z Score 2.27)
* **Bag Boy Beverage Holder**: Spike (+118.75%, Z Score 2.17)
* **Clicgear Rovic Cooler Bag**: Spike (+133.33%, Z Score 2.12)
* **Clicgear 8.0 Shoe Brush**: Spike (+105.88%, Z Score 2.02)
* **Clicgear 8.0 Shoe Brush**: Spike (+100%, Z Score 2.00)
```

---

## Future work

**Streaming responses** — stream the report token by token using LangGraph's `.astream()` and FastAPI's `StreamingResponse`, so clients see output as it's generated rather than waiting for the full run.

**Retry logic in the supervisor** — if the Analyst returns empty findings (tool failure, data issue), the supervisor currently routes to END. A retry counter in state would let it re-route to the Analyst up to N times before failing gracefully.

**Configurable dataset via upload** — accept a CSV file upload in the API rather than a hardcoded path, making the system dataset-agnostic.

**Scheduled runs** — wrap the graph invocation in a cron job or task queue (Celery, APScheduler) to produce daily briefings automatically and store them.

**Richer severity model** — the current severity score is a heuristic formula. A trained regression model on historical supply chain disruption data could produce more calibrated risk scores.

---

## Screenshots

### Swagger UI — POST /analyze

The API tested via FastAPI's built-in Swagger UI at `http://localhost:8000/docs`. Request body sent, `200 OK` returned with the full report and structured findings.

*(See `screenshots/swagger_ui.png`)*

### VS Code — Project structure and graph.py

File tree showing the full project layout: `api/`, `src/`, `src/tools/`, `data/`. The `graph.py` file open showing the `writer_node` implementation with multi-format output handling.

*(See `screenshots/vscode_structure.png`)*

---

## Author

**Aniket Dhamodkar(Patil)**  

[LinkedIn](https://www.linkedin.com/in/aniket-tec/) · [GitHub](https://github.com/AniketTec) · aniket.tec.1@gmail.com
