import sqlite3
import logging
from datetime import datetime

DB_PATH = 'academyops.db'

# Custom domain errors (Requirement FR-6)
class LeadNotFoundError(Exception):
    pass

class DuplicateLeadError(Exception):
    pass

class LeadRepository:
    def __init__(self):
        self.db_path = DB_PATH

    def _get_timestamp(self):
        return datetime.now().isoformat()

    def create(self, name, phone, source, stage, notes=""):
        """Creates a new lead in the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                now = self._get_timestamp()
                
                # Parameterised queries for safety (Requirement FR-4)
                cursor.execute('''
                    INSERT INTO leads (name, phone, source, stage, notes, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (name, phone, source, stage, notes, now, now))
                
                lead_id = cursor.lastrowid
                conn.commit() # Transaction handling (Requirement FR-5)
                
                logging.info(f"Created lead: ID {lead_id}, Name: {name}")
                return lead_id
                
        except sqlite3.IntegrityError:
            logging.error(f"Failed to create lead: Phone {phone} already exists.")
            raise DuplicateLeadError(f"A lead with phone number {phone} already exists.")

    def get(self, lead_id):
        """Retrieves a single lead by ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM leads WHERE id = ?', (lead_id,))
            row = cursor.fetchone()
            
            if not row:
                raise LeadNotFoundError(f"Lead with ID {lead_id} not found.")
            return dict(row)

    def list(self):
        """Retrieves all leads."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM leads')
            return [dict(row) for row in cursor.fetchall()]

    def update_stage(self, lead_id, new_stage):
        """Updates the stage of an existing lead."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            now = self._get_timestamp()
            
            cursor.execute('''
                UPDATE leads 
                SET stage = ?, updated_at = ?
                WHERE id = ?
            ''', (new_stage, now, lead_id))
            
            if cursor.rowcount == 0:
                logging.error(f"Failed to update stage: Lead ID {lead_id} not found.")
                raise LeadNotFoundError(f"Lead with ID {lead_id} not found.")
            
            conn.commit()
            logging.info(f"Updated lead ID {lead_id} to stage {new_stage}")

    def delete(self, lead_id):
        """Deletes a lead from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM leads WHERE id = ?', (lead_id,))
            
            if cursor.rowcount == 0:
                logging.error(f"Failed to delete: Lead ID {lead_id} not found.")
                raise LeadNotFoundError(f"Lead with ID {lead_id} not found.")
            
            conn.commit()
            logging.info(f"Deleted lead ID {lead_id}")