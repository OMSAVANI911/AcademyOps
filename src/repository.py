from sqlalchemy.orm import Session

from src.database import Lead


class LeadNotFoundError(Exception):
    pass


class DuplicateLeadError(Exception):
    pass


class InvalidStageError(Exception):
    pass


PIPELINE_STAGES = [
    "New",
    "Contacted",
    "Qualified",
    "Demo",
    "Enrolled",
    "Lost"
]


class LeadRepository:

    def get(self, db: Session, lead_id: int):

        lead = db.query(Lead).filter(
            Lead.id == lead_id
        ).first()

        if not lead:
            raise LeadNotFoundError(
                f"Lead {lead_id} not found"
            )

        return lead

    def list(self, db: Session):

        return db.query(Lead).all()

    def create(
        self,
        db: Session,
        name: str,
        phone: str,
        source: str,
        stage: str,
        notes: str = None
    ):

        existing = db.query(Lead).filter(
            Lead.phone == phone
        ).first()

        if existing:
            raise DuplicateLeadError(
                "Phone number already exists"
            )

        if stage not in PIPELINE_STAGES:
            raise InvalidStageError(
                "Invalid stage"
            )

        lead = Lead(
            name=name,
            phone=phone,
            source=source,
            stage=stage,
            notes=notes
        )

        db.add(lead)
        db.commit()
        db.refresh(lead)

        return lead.id

    def update_stage(
        self,
        db: Session,
        lead_id: int,
        stage: str
    ):

        if stage not in PIPELINE_STAGES:
            raise InvalidStageError(
                "Invalid stage"
            )

        lead = db.query(Lead).filter(
            Lead.id == lead_id
        ).first()

        if not lead:
            raise LeadNotFoundError(
                f"Lead {lead_id} not found"
            )

        lead.stage = stage

        db.commit()
        db.refresh(lead)

        return lead

    def delete(
        self,
        db: Session,
        lead_id: int
    ):

        lead = db.query(Lead).filter(
            Lead.id == lead_id
        ).first()

        if not lead:
            raise LeadNotFoundError(
                f"Lead {lead_id} not found"
            )

        db.delete(lead)
        db.commit()

        return True