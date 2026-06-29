from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.graph import graph
from src.state import AgentState

# 1. Define lifespan management for startup/shutdown events (Optional but recommended)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code here runs BEFORE the application starts up
    print("Initializing AI Agent resources (connecting to vector DBs, loading models)...")
    yield
    # Code here runs WHEN the application shuts down
    print("Cleaning up AI Agent resources (closing connections)...")


# 2. Instantiate the core FastAPI application object
app = FastAPI(
    title="Supply Guard API Gateway",
    description="Production ready FastAPI backend for Supply Guard Multi-Agent System.",
    version="1.0.0",
    lifespan=lifespan,
)

# 3. Configure Cross-Origin Resource Sharing (CORS)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class AnalysisRequest(BaseModel):
    dataset_path: str
    top_n_risks: int = 5


class AnalysisResponse(BaseModel):
    findings: dict
    report: str


# 4. Define a basic sanity root route
@app.get("/")
async def root():
    return {
        "message": "AI Agent Gateway is running.",
        "docs_url": "/docs",
    }


# 5. Supply Chain Analysis Endpoint
@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_supply_chain(request: AnalysisRequest):
    try:
        print("=" * 60)
        print("Analyze endpoint reached")
        print(request)
        print("=" * 60)
        initial_state = AgentState(
            messages=[],
            findings={},
            report="",
            next_agent=None,
            dataset_path=request.dataset_path)
        
        result = graph.invoke(initial_state)
        
        return AnalysisResponse(
            findings=result["findings"],
            report=result["report"]
        )
    except Exception as e:
        print(f"Error during analysis: {e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )