# tracker/db.py - Database operations
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import os

class TrackerDB:
    def __init__(self):
        self.db_dir = Path.home() / ".viscli"
        self.db_dir.mkdir(exist_ok=True)
        self.db_path = self.db_dir / "tracker.db"
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT NOT NULL,
                    start_time TIMESTAMP NOT NULL,
                    end_time TIMESTAMP,
                    duration INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS active_session (
                    id INTEGER PRIMARY KEY,
                    file_path TEXT NOT NULL,
                    start_time TIMESTAMP NOT NULL
                )
            """)
            conn.commit()

    def start_session(self, file_path: str) -> bool:
        """Start a new tracking session."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT COUNT(*) FROM active_session")
                if cursor.fetchone()[0] > 0:
                    return False

                now = datetime.now()
                conn.execute(
                    "INSERT INTO active_session (file_path, start_time) VALUES (?, ?)",
                    (file_path, now)
                )
                conn.commit()
                return True
        except Exception:
            return False

    def stop_session(self) -> Optional[Dict]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT file_path, start_time FROM active_session LIMIT 1"
                )
                row = cursor.fetchone()

                if not row:
                    return None

                file_path, start_time_str = row
                start_time = datetime.fromisoformat(start_time_str)
                end_time = datetime.now()
                duration = int((end_time - start_time).total_seconds())

                conn.execute(
                    (file_path, start_time, end_time, duration)
                )

                conn.execute("DELETE FROM active_session")
                conn.commit()

                return {
                    "file_path": file_path,
                    "start_time": start_time,
                    "end_time": end_time,
                    "duration": duration
                }
        except Exception:
            return None

    def get_active_session(self) -> Optional[Dict]:
        """Get the current active session."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute(
                    "SELECT file_path, start_time FROM active_session LIMIT 1"
                )
                row = cursor.fetchone()

                if row:
                    return {
                        "file_path": row[0],
                        "start_time": datetime.fromisoformat(row[1])
                    }
                return None
        except Exception:
            return None

    def get_time_report(self) -> List[Dict]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("""
                    SELECT file_path, SUM(duration) as total_duration, COUNT(*) as session_count
                    FROM sessions 
                    WHERE end_time IS NOT NULL
                    GROUP BY file_path
                    ORDER BY total_duration DESC
                """)

                return [
                    {
                        "file_path": row[0],
                        "total_duration": row[1],
                        "session_count": row[2]
                    }
                    for row in cursor.fetchall()
                ]
        except Exception:
            return []
