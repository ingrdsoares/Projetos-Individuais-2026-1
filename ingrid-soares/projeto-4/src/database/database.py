import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Tuple

DB_PATH = Path("data/catalog.db")

def get_db_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_db_connection() as conn:
        # Table for tracking processed PDFs (Idempotency and Lineage)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                url TEXT NOT NULL UNIQUE,
                file_hash TEXT NOT NULL UNIQUE,
                filename TEXT NOT NULL,
                downloaded_at DATETIME NOT NULL,
                processed_at DATETIME,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        # Table for structured metrics (The final data)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                year INTEGER NOT NULL,
                quarter TEXT NOT NULL,
                metric_name TEXT NOT NULL,
                metric_value REAL,
                unit TEXT,
                FOREIGN KEY (document_id) REFERENCES documents (id)
            )
        ''')
        conn.commit()

def register_document(company_name: str, url: str, file_hash: str, filename: str) -> Optional[int]:
    """Registers a document in the catalog. Returns document_id if new, else None."""
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO documents (company_name, url, file_hash, filename, downloaded_at) VALUES (?, ?, ?, ?, ?)",
                (company_name, url, file_hash, filename, datetime.now().isoformat())
            )
            conn.commit()
            return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None

def mark_as_processed(document_id: int):
    """Marks a document as successfully processed."""
    with get_db_connection() as conn:
        conn.execute(
            "UPDATE documents SET processed_at = ?, status = 'processed' WHERE id = ?",
            (datetime.now().isoformat(), document_id)
        )
        conn.commit()

def get_processed_hashes() -> List[str]:
    """Returns a list of all hashes already processed."""
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT file_hash FROM documents")
        return [row['file_hash'] for row in cursor.fetchall()]

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
