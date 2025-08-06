"""
Habit tracking functionality for the AI Wellness Assistant
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from wellness_assistant.core.storage import StorageManager, HabitEntry
from wellness_assistant.utils.validators import Validators, ValidationError

class HabitTracker:
    """Main class for tracking user habits"""
    
    def __init__(self, storage_manager: Optional[StorageManager] = None):
        """Initialize habit tracker
        
        Args:
            storage_manager: Optional storage manager instance
        """
        self.storage = storage_manager or StorageManager()
    
    def track_habit(
        self,
        habit: str,
        value: float,
        unit: str,
        notes: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ) -> bool:
        """Track a habit entry
        
        Args:
            habit: Name of the habit (e.g., 'sleep', 'water', 'exercise')
            value: Numeric value for the habit
            unit: Unit of measurement
            notes: Optional notes about the entry
            timestamp: Optional timestamp (defaults to now)
            
        Returns:
            True if successfully tracked, False otherwise
            
        Raises:
            ValidationError: If input validation fails
        """
        try:
            # Validate inputs
            habit = Validators.validate_habit(habit)
            value = Validators.validate_value(habit, value)
            unit = Validators.validate_unit(habit, unit)
            
            if timestamp is None:
                timestamp = datetime.now()
            
            # Create habit entry
            entry = HabitEntry(
                habit=habit,
                value=value,
                unit=unit,
                timestamp=timestamp,
                notes=notes
            )
            
            # Store the entry
            success = self.storage.add_habit_entry(entry)
            
            if success:
                print(f"✅ Tracked {habit}: {value} {unit}")
                if notes:
                    print(f"   Note: {notes}")
            else:
                print(f"❌ Failed to track {habit}")
            
            return success
            
        except ValidationError as e:
            print(f"❌ Validation Error: {e}")
            return False
        except Exception as e:
            print(f"❌ Error tracking habit: {e}")
            return False
    
    def get_recent_entries(self, habit: Optional[str] = None, days: int = 7) -> List[HabitEntry]:
        """Get recent habit entries
        
        Args:
            habit: Optional filter by specific habit
            days: Number of days to look back
            
        Returns:
            List of recent habit entries
        """
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = start_date.replace(day=start_date.day - days + 1)
        
        return self.storage.get_habit_entries(
            habit=habit,
            start_date=start_date,
            limit=50  # Reasonable limit for recent entries
        )
    
    def get_habit_summary(self, days: int = 7) -> Dict[str, Dict[str, Any]]:
        """Get summary statistics for all habits
        
        Args:
            days: Number of days to include in summary
            
        Returns:
            Dictionary with habit statistics
        """
        return self.storage.get_habit_summary(days)
    
    def display_summary(self, days: int = 7) -> None:
        """Display a formatted summary of habits
        
        Args:
            days: Number of days to include in summary
        """
        summary = self.get_habit_summary(days)
        
        if not summary:
            print(f"📊 No habit data found for the last {days} days.")
            return
        
        print(f"\n📊 Habit Summary (Last {days} days)")
        print("=" * 50)
        
        for habit, data in summary.items():
            print(f"\n🔹 {habit.title()}")
            print(f"   Total: {data['total']:.1f} {data['unit']}")
            print(f"   Average: {data['average']:.1f} {data['unit']}/day")
            print(f"   Entries: {data['count']}")
            
            # Provide habit-specific insights
            self._display_habit_insights(habit, data)
    
    def _display_habit_insights(self, habit: str, data: Dict[str, Any]) -> None:
        """Display insights for specific habits
        
        Args:
            habit: Name of the habit
            data: Habit summary data
        """
        avg = data['average']
        
        if habit == 'sleep':
            if avg >= 7 and avg <= 9:
                print("   💚 Great sleep duration!")
            elif avg < 7:
                print("   ⚠️  Consider getting more sleep (7-9 hours recommended)")
            else:
                print("   ⚠️  You might be oversleeping")
        
        elif habit == 'water':
            if avg >= 2.0:
                print("   💧 Good hydration!")
            else:
                print("   ⚠️  Try to drink more water (2+ liters recommended)")
        
        elif habit == 'exercise':
            if avg >= 30:
                print("   💪 Excellent exercise routine!")
            elif avg >= 15:
                print("   👍 Good activity level, try to reach 30+ minutes daily")
            else:
                print("   ⚠️  Consider increasing physical activity (30+ minutes recommended)")
        
        elif habit == 'mood':
            if avg >= 7:
                print("   😊 Great mood overall!")
            elif avg >= 5:
                print("   😐 Moderate mood, consider stress management techniques")
            else:
                print("   😟 Low mood detected, consider speaking with a healthcare professional")
    
    def quick_track(self) -> None:
        """Interactive quick tracking session"""
        print("\n🎯 Quick Habit Tracking")
        print("Enter your habits for today (press Enter to skip):")
        
        common_habits = [
            ('sleep', 'hours', 'How many hours did you sleep?'),
            ('water', 'liters', 'How much water did you drink? (liters)'),
            ('exercise', 'minutes', 'How many minutes of exercise?'),
            ('mood', 'scale', 'Rate your mood (1-10):')
        ]
        
        for habit, unit, prompt in common_habits:
            try:
                response = input(f"{prompt} ").strip()
                if response:
                    value = float(response)
                    self.track_habit(habit, value, unit)
            except ValueError:
                print(f"❌ Invalid input for {habit}")
            except KeyboardInterrupt:
                print("\n👋 Tracking session cancelled")
                break
        
        print("\n✅ Quick tracking complete!")
    
    def show_trends(self, habit: str, days: int = 30) -> None:
        """Show trends for a specific habit
        
        Args:
            habit: Name of the habit to analyze
            days: Number of days to analyze
        """
        entries = self.get_recent_entries(habit, days)
        
        if not entries:
            print(f"📈 No data found for {habit} in the last {days} days")
            return
        
        print(f"\n📈 {habit.title()} Trends (Last {days} days)")
        print("=" * 40)
        
        # Group by date
        daily_values = {}
        for entry in entries:
            date_key = entry.timestamp.date()
            if date_key not in daily_values:
                daily_values[date_key] = []
            daily_values[date_key].append(entry.value)
        
        # Calculate daily averages and display
        dates = sorted(daily_values.keys())
        for date in dates[-10:]:  # Show last 10 days
            avg_value = sum(daily_values[date]) / len(daily_values[date])
            print(f"{date}: {avg_value:.1f} {entries[0].unit}")
        
        # Simple trend analysis
        if len(dates) >= 2:
            recent_avg = sum(daily_values[dates[-1]]) / len(daily_values[dates[-1]])
            older_avg = sum(daily_values[dates[0]]) / len(daily_values[dates[0]])
            
            if recent_avg > older_avg:
                print(f"\n📈 Trending up! (+{recent_avg - older_avg:.1f})")
            elif recent_avg < older_avg:
                print(f"\n📉 Trending down! ({recent_avg - older_avg:.1f})")
            else:
                print(f"\n➡️  Stable trend")
