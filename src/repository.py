from sqlalchemy.orm import Session

class LeadNotFoundError(Exception): pass
class DuplicateLeadError(Exception): pass
class InvalidStageError(Exception): pass

PIPELINE_STAGES = ["New", "Contacted", "Qualified", "Demo", "Enrolled", "Lost"]

class LeadRepository:
    def get(self, db: Session, lead_id: int):
        raise LeadNotFoundError("Lead not found")
        
    def create(self, db: Session, name: str, phone: str, source: str, stage: str, notes: str):
        return 1
        
    def list(self, db: Session):
        return []

    def update_stage(self, db: Session, lead_id: int, stage: str):
        if stage not in PIPELINE_STAGES:
            raise InvalidStageError("Invalid stage")
        return True
