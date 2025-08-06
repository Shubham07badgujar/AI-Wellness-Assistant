"""
Input validation utilities for the AI Wellness Assistant
"""

from typing import Union, List, Optional
from datetime import datetime
import re

class ValidationError(Exception):
    """Custom validation error"""
    pass

class Validators:
    """Input validation utilities"""
    
    VALID_HABITS = {
        "sleep": {"units": ["hours"], "min": 0, "max": 24},
        "water": {"units": ["liters", "cups", "ml"], "min": 0, "max": 10},
        "exercise": {"units": ["minutes", "hours"], "min": 0, "max": 480},
        "mood": {"units": ["scale"], "min": 1, "max": 10},
        "meals": {"units": ["count"], "min": 0, "max": 10},
        "weight": {"units": ["kg", "lbs"], "min": 30, "max": 500},
        "steps": {"units": ["count"], "min": 0, "max": 50000}
    }
    
    @classmethod
    def validate_habit(cls, habit: str) -> str:
        """Validate habit name"""
        habit = habit.lower().strip()
        if habit not in cls.VALID_HABITS:
            valid_habits = ", ".join(cls.VALID_HABITS.keys())
            raise ValidationError(f"Invalid habit '{habit}'. Valid habits: {valid_habits}")
        return habit
    
    @classmethod
    def validate_value(cls, habit: str, value: Union[int, float]) -> float:
        """Validate habit value"""
        habit_config = cls.VALID_HABITS[habit]
        
        if not isinstance(value, (int, float)):
            raise ValidationError(f"Value must be a number, got {type(value)}")
        
        if value < habit_config["min"] or value > habit_config["max"]:
            raise ValidationError(
                f"Value {value} is out of range for {habit}. "
                f"Range: {habit_config['min']}-{habit_config['max']}"
            )
        
        return float(value)
    
    @classmethod
    def validate_unit(cls, habit: str, unit: str) -> str:
        """Validate unit for a habit"""
        habit_config = cls.VALID_HABITS[habit]
        unit = unit.lower().strip()
        
        if unit not in habit_config["units"]:
            valid_units = ", ".join(habit_config["units"])
            raise ValidationError(f"Invalid unit '{unit}' for {habit}. Valid units: {valid_units}")
        
        return unit
    
    @classmethod
    def validate_date(cls, date_str: Optional[str] = None) -> datetime:
        """Validate and parse date string"""
        if date_str is None:
            return datetime.now()
        
        try:
            # Try common date formats
            for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"]:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
            
            raise ValueError("Invalid date format")
        except ValueError:
            raise ValidationError(
                f"Invalid date format '{date_str}'. "
                "Use YYYY-MM-DD, DD/MM/YYYY, or MM/DD/YYYY"
            )
    
    @classmethod
    def sanitize_symptom_input(cls, symptom: str) -> str:
        """Sanitize symptom input"""
        # Remove extra whitespace and normalize
        symptom = re.sub(r'\s+', ' ', symptom.strip())
        
        # Remove potentially harmful characters but keep basic punctuation
        symptom = re.sub(r'[^\w\s\-.,!?]', '', symptom)
        
        if len(symptom) < 3:
            raise ValidationError("Symptom description must be at least 3 characters")
        
        if len(symptom) > 500:
            raise ValidationError("Symptom description must be less than 500 characters")
        
        return symptom.lower()
    
    @classmethod
    def validate_mood_scale(cls, mood: Union[int, float]) -> int:
        """Validate mood on 1-10 scale"""
        try:
            mood_int = int(mood)
            if mood_int < 1 or mood_int > 10:
                raise ValidationError("Mood must be between 1 and 10")
            return mood_int
        except (ValueError, TypeError):
            raise ValidationError("Mood must be a number between 1 and 10")
