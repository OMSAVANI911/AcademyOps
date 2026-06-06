from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from repository import LeadRepository, LeadNotFoundError, DuplicateLeadError

app = FastAPI()
repo = LeadRepository()
templates = Jinja2Templates(directory="src/templates")

class LeadSchema(BaseModel):
    id: int
    name: str
    phone: str
    source: str
    stage: str
    notes: str

class PaginatedLeadsResponse(BaseModel):
    data: List[LeadSchema]
    page: int
    limit: int
    total: int

class CreateLeadRequest(BaseModel):
    name: str
    phone: str
    source: Optional[str] = ""
    stage: Optional[str] = "New"
    notes: Optional[str] = ""

class UpdateStageRequest(BaseModel):
    stage: str

# --- Serve the HTML Webpage ---
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/v1/leads/{lead_id}", response_model=LeadSchema)
def get_lead(lead_id: int):
    try:
        lead = repo.get(lead_id)
        return lead
    except LeadNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/api/v1/leads", response_model=PaginatedLeadsResponse)
def list_leads(
    stage: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1)
):
    # Keep original database logic
    leads = repo.list()
        
    # Exact same filtering logic as the Flask implementation
    if stage:
        leads = [l for l in leads if l['stage'].lower() == stage.lower()]
    if source:
        leads = [l for l in leads if l['source'].lower() == source.lower()]

    # Exact same pagination logic
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_leads = leads[start_idx:end_idx]

    return {
        "data": paginated_leads,
        "page": page,
        "limit": limit,
        "total": len(leads)
    }

@app.post("/api/v1/leads", status_code=201)
def create_lead(data: CreateLeadRequest):
    try:
        lead_id = repo.create(
            name=data.name,
            phone=data.phone,
            source=data.source,
            stage=data.stage,
            notes=data.notes
        )
        return {"id": lead_id, "message": "Lead created successfully"}
    except DuplicateLeadError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.patch("/api/v1/leads/{lead_id}/stage")
def update_stage(lead_id: int, data: UpdateStageRequest):
    try:
        repo.update_stage(lead_id, data.stage)
        return {"message": f"Stage updated to {data.stage}"}
    except LeadNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/api/v1/leads/{lead_id}", status_code=204)
def delete_lead(lead_id: int):
    try:
        repo.delete(lead_id)
        return None
    except LeadNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

if __name__ == '__main__':
    uvicorn.run('api:app', host='127.0.0.1', port=8000, reload=True)
