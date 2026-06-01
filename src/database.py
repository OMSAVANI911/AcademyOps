import sqlite3
import logging

# Set up logging to track everything that happens (Requirement FR-7)
logging.basicConfig(
    filename='academyops.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

DB_PATH = 'academyops.db'

def init_db():
    """Creates the database schema and table."""
    try:
        # Connect to the database (this creates the file if it doesn't exist)
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            # Create the 'leads' table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL UNIQUE,
                    source TEXT,
                    stage TEXT CHECK(stage IN ('New', 'Contacted', 'Qualified', 'Demo', 'Enrolled', 'Lost')) NOT NULL,
                    notes TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            ''')
            
            # Create indexes to make looking up phones and stages faster
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_leads_phone ON leads(phone)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_leads_stage ON leads(stage)')
            
            conn.commit()
            
            logging.info("Database schema initialized successfully.")
            print("Success! The database has been created.")
            
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        print(f"Error: {e}")

if __name__ == '__main__':
    init_db()