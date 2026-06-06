from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class LeadResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    phone: str
    source: str
    stage: str
    notes: Optional[str] = None


class CreateLeadRequest(BaseModel):
    name: str
    phone: str
    source: str
    stage: str = "New"
    notes: Optional[str] = None


class CreateLeadResponse(BaseModel):
    id: int


class UpdateStageRequest(BaseModel):
    stage: str


class UpdateStageResponse(BaseModel):
    message: str


class PaginatedLeadsResponse(BaseModel):
    data: List[LeadResponse]
    page: int
    limit: int
    total: int


class MessageRequest(BaseModel):
    message: str


class MessageResponse(BaseModel):
    intent: str
    suggested_stage: str
    reply: str