from pydantic import BaseModel, Field
from typing import Any


class AgentState(BaseModel):

    messages: list = Field(default_factory=list)

    findings: dict[str, Any] = Field(
        default_factory=dict
    )

    report: str | None = None

    next_agent: str | None = None

    dataset_path: str | None = None


if __name__ == "__main__":
    
    state = AgentState()

    print(state)