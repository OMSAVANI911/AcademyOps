"""
src/api.py
FastAPI entrypoint for AcademyOps.
"""

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

from src.classifier import classify_message
from src.database import get_db, init_db
from src.repository import (
    LeadRepository,
    DuplicateLeadError,
    InvalidStageError,
    LeadNotFoundError,
)
from src.schemas import (
    CreateLeadRequest,
    CreateLeadResponse,
    LeadResponse,
    MessageRequest,
    MessageResponse,
    PaginatedLeadsResponse,
    UpdateStageRequest,
    UpdateStageResponse,
)

app = FastAPI(title="AcademyOps API")
repo = LeadRepository()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get(
    "/api/v1/leads/{lead_id}",
    response_model=LeadResponse
)
def get_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    try:
        return repo.get(db, lead_id)

    except LeadNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@app.get(
    "/api/v1/leads",
    response_model=PaginatedLeadsResponse
)
def list_leads(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    all_leads = repo.list(db)

    start = (page - 1) * limit
    end = start + limit

    return PaginatedLeadsResponse(
        data=all_leads[start:end],
        page=page,
        limit=limit,
        total=len(all_leads)
    )


@app.post(
    "/api/v1/leads",
    response_model=CreateLeadResponse,
    status_code=201
)
def create_lead(
    data: CreateLeadRequest,
    db: Session = Depends(get_db)
):
    try:
        lead_id = repo.create(
            db=db,
            name=data.name,
            phone=data.phone,
            source=data.source,
            stage=data.stage,
            notes=data.notes
        )

        return CreateLeadResponse(id=lead_id)

    except DuplicateLeadError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except InvalidStageError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.patch(
    "/api/v1/leads/{lead_id}/stage",
    response_model=UpdateStageResponse
)
def update_stage(
    lead_id: int,
    data: UpdateStageRequest,
    db: Session = Depends(get_db)
):
    try:
        repo.update_stage(
            db,
            lead_id,
            data.stage
        )

        return UpdateStageResponse(
            message=f"Stage updated to {data.stage}."
        )

    except LeadNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except InvalidStageError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.post(
    "/api/v1/leads/{lead_id}/message",
    response_model=MessageResponse
)
def handle_lead_message(
    lead_id: int,
    req: MessageRequest,
    db: Session = Depends(get_db)
):
    try:
        repo.get(db, lead_id)

    except LeadNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    return classify_message(req.message)


if __name__ == "__main__":
    uvicorn.run(
        "src.api:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )