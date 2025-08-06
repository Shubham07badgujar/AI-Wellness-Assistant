"""
Data storage management for the AI Wellness Assistant
Supports both JSON and SQLite storage
"""

import json
import sqlite3
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from wellness_assistant.utils.config import Config

@dataclass
class HabitEntry:
    """Data structure for habit tracking entry"""
    habit: str
    value: float
    unit: str
    timestamp: datetime
    notes: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HabitEntry':
        """Create from dictionary"""
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)

class StorageManager:
    """Manages data storage for habit tracking"""
    
    def __init__(self, use_sqlite: bool = True):
        """Initialize storage manager
        
        Args:
            use_sqlite: If True, use SQLite; if False, use JSON
        """
        Config.ensure_data_dir()
        self.use_sqlite = use_sqlite
        
        if use_sqlite:
            self.db_path = Config.DATA_DIR / "wellness.db"
            self._init_sqlite()
        else:
            self.json_path = Config.DATA_DIR / "habits.json"
            self._init_json()
    
    def _init_sqlite(self) -> None:
        """Initialize SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS habit_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit TEXT NOT NULL,
                    value REAL NOT NULL,
                    unit TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    notes TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_habit_timestamp 
                ON habit_entries(habit, timestamp)
            """)
    
    def _init_json(self) -> None:
        """Initialize JSON storage"""
        if not self.json_path.exists():
            self._save_json_data([])
    
    def _load_json_data(self) -> List[Dict[str, Any]]:
        """Load data from JSON file"""
        try:
            with open(self.json_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_json_data(self, data: List[Dict[str, Any]]) -> None:
        """Save data to JSON file"""
        with open(self.json_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def add_habit_entry(self, entry: HabitEntry) -> bool:
        """Add a new habit entry
        
        Args:
            entry: HabitEntry to add
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.use_sqlite:
                return self._add_entry_sqlite(entry)
            else:
                return self._add_entry_json(entry)
        except Exception as e:
            print(f"Error adding habit entry: {e}")
            return False
    
    def _add_entry_sqlite(self, entry: HabitEntry) -> bool:
        """Add entry to SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO habit_entries (habit, value, unit, timestamp, notes)
                VALUES (?, ?, ?, ?, ?)
            """, (
                entry.habit,
                entry.value,
                entry.unit,
                entry.timestamp.isoformat(),
                entry.notes
            ))
        return True
    
    def _add_entry_json(self, entry: HabitEntry) -> bool:
        """Add entry to JSON file"""
        data = self._load_json_data()
        data.append(entry.to_dict())
        self._save_json_data(data)
        return True
    
    def get_habit_entries(
        self, 
        habit: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[HabitEntry]:
        """Get habit entries with optional filtering
        
        Args:
            habit: Filter by specific habit
            start_date: Filter entries after this date
            end_date: Filter entries before this date
            limit: Maximum number of entries to return
            
        Returns:
            List of HabitEntry objects
        """
        if self.use_sqlite:
            return self._get_entries_sqlite(habit, start_date, end_date, limit)
        else:
            return self._get_entries_json(habit, start_date, end_date, limit)
    
    def _get_entries_sqlite(
        self,
        habit: Optional[str],
        start_date: Optional[datetime],
        end_date: Optional[datetime],
        limit: Optional[int]
    ) -> List[HabitEntry]:
        """Get entries from SQLite database"""
        query = "SELECT habit, value, unit, timestamp, notes FROM habit_entries WHERE 1=1"
        params = []
        
        if habit:
            query += " AND habit = ?"
            params.append(habit)
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date.isoformat())
        
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date.isoformat())
        
        query += " ORDER BY timestamp DESC"
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, params)
            entries = []
            for row in cursor.fetchall():
                entries.append(HabitEntry(
                    habit=row[0],
                    value=row[1],
                    unit=row[2],
                    timestamp=datetime.fromisoformat(row[3]),
                    notes=row[4]
                ))
        
        return entries
    
    def _get_entries_json(
        self,
        habit: Optional[str],
        start_date: Optional[datetime],
        end_date: Optional[datetime],
        limit: Optional[int]
    ) -> List[HabitEntry]:
        """Get entries from JSON file"""
        data = self._load_json_data()
        entries = [HabitEntry.from_dict(item) for item in data]
        
        # Apply filters
        if habit:
            entries = [e for e in entries if e.habit == habit]
        
        if start_date:
            entries = [e for e in entries if e.timestamp >= start_date]
        
        if end_date:
            entries = [e for e in entries if e.timestamp <= end_date]
        
        # Sort by timestamp (newest first)
        entries.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Apply limit
        if limit:
            entries = entries[:limit]
        
        return entries
    
    def get_habit_summary(self, days: int = 7) -> Dict[str, Dict[str, Any]]:
        """Get summary statistics for habits over the last N days
        
        Args:
            days: Number of days to include in summary
            
        Returns:
            Dictionary with habit statistics
        """
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = start_date.replace(day=start_date.day - days + 1)
        
        entries = self.get_habit_entries(start_date=start_date)
        
        summary = {}
        for entry in entries:
            if entry.habit not in summary:
                summary[entry.habit] = {
                    "total": 0,
                    "count": 0,
                    "average": 0,
                    "unit": entry.unit,
                    "entries": []
                }
            
            summary[entry.habit]["total"] += entry.value
            summary[entry.habit]["count"] += 1
            summary[entry.habit]["entries"].append(entry)
        
        # Calculate averages
        for habit_data in summary.values():
            if habit_data["count"] > 0:
                habit_data["average"] = habit_data["total"] / habit_data["count"]
        
        return summary
