"""
Data export functionality for the AI Wellness Assistant
"""

import json
import csv
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
from wellness_assistant.core.storage import StorageManager, HabitEntry
from wellness_assistant.utils.config import Config

class DataExporter:
    """Handles data export in various formats"""
    
    def __init__(self, storage_manager: Optional[StorageManager] = None):
        """Initialize data exporter
        
        Args:
            storage_manager: Optional storage manager instance
        """
        self.storage = storage_manager or StorageManager()
        self.export_dir = Path("exports")
        self.export_dir.mkdir(exist_ok=True)
    
    def export_habits_csv(self, 
                         start_date: Optional[datetime] = None,
                         end_date: Optional[datetime] = None,
                         habit_filter: Optional[str] = None) -> str:
        """Export habit data to CSV format
        
        Args:
            start_date: Start date for export (default: 30 days ago)
            end_date: End date for export (default: today)
            habit_filter: Optional filter for specific habit
            
        Returns:
            Path to exported CSV file
        """
        # Set default date range
        if end_date is None:
            end_date = datetime.now()
        if start_date is None:
            start_date = end_date - timedelta(days=30)
        
        # Get habit entries
        entries = self.storage.get_habit_entries(
            habit=habit_filter,
            start_date=start_date,
            end_date=end_date
        )
        
        # Generate filename
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        habit_str = f"_{habit_filter}" if habit_filter else ""
        filename = f"habits{habit_str}_{date_str}.csv"
        filepath = self.export_dir / filename
        
        # Write CSV
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['date', 'time', 'habit', 'value', 'unit', 'notes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for entry in entries:
                writer.writerow({
                    'date': entry.timestamp.strftime('%Y-%m-%d'),
                    'time': entry.timestamp.strftime('%H:%M:%S'),
                    'habit': entry.habit,
                    'value': entry.value,
                    'unit': entry.unit,
                    'notes': entry.notes or ''
                })
        
        return str(filepath)
    
    def export_wellness_report(self, days: int = 30) -> str:
        """Generate a comprehensive wellness report
        
        Args:
            days: Number of days to include in report
            
        Returns:
            Path to generated report file
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Get all entries for the period
        entries = self.storage.get_habit_entries(start_date=start_date, end_date=end_date)
        
        # Generate report data
        report_data = self._generate_report_data(entries, days)
        
        # Generate filename
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"wellness_report_{days}days_{date_str}.json"
        filepath = self.export_dir / filename
        
        # Write report
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        return str(filepath)
    
    def _generate_report_data(self, entries: List[HabitEntry], days: int) -> Dict[str, Any]:
        """Generate comprehensive report data from entries"""
        
        # Group entries by habit
        habits_data = {}
        for entry in entries:
            if entry.habit not in habits_data:
                habits_data[entry.habit] = []
            habits_data[entry.habit].append(entry)
        
        # Calculate statistics for each habit
        habit_stats = {}
        for habit, habit_entries in habits_data.items():
            values = [entry.value for entry in habit_entries]
            habit_stats[habit] = {
                'total_entries': len(habit_entries),
                'average': sum(values) / len(values) if values else 0,
                'min': min(values) if values else 0,
                'max': max(values) if values else 0,
                'unit': habit_entries[0].unit if habit_entries else '',
                'frequency': len(habit_entries) / days,
                'trend': self._calculate_trend(habit_entries)
            }
        
        # Generate overall wellness score
        wellness_score = self._calculate_wellness_score(habit_stats)
        
        return {
            'report_metadata': {
                'generated_at': datetime.now().isoformat(),
                'period_days': days,
                'total_entries': len(entries),
                'habits_tracked': list(habit_stats.keys())
            },
            'wellness_score': wellness_score,
            'habit_statistics': habit_stats,
            'recommendations': self._generate_recommendations(habit_stats),
            'raw_entries': [
                {
                    'timestamp': entry.timestamp.isoformat(),
                    'habit': entry.habit,
                    'value': entry.value,
                    'unit': entry.unit,
                    'notes': entry.notes
                }
                for entry in entries
            ]
        }
    
    def _calculate_trend(self, entries: List[HabitEntry]) -> str:
        """Calculate trend for a habit (improving, declining, stable)"""
        if len(entries) < 2:
            return "insufficient_data"
        
        # Sort by timestamp
        sorted_entries = sorted(entries, key=lambda x: x.timestamp)
        
        # Compare first half vs second half averages
        mid_point = len(sorted_entries) // 2
        first_half_avg = sum(e.value for e in sorted_entries[:mid_point]) / mid_point
        second_half_avg = sum(e.value for e in sorted_entries[mid_point:]) / (len(sorted_entries) - mid_point)
        
        diff_percentage = ((second_half_avg - first_half_avg) / first_half_avg) * 100
        
        if diff_percentage > 5:
            return "improving"
        elif diff_percentage < -5:
            return "declining"
        else:
            return "stable"
    
    def _calculate_wellness_score(self, habit_stats: Dict[str, Dict]) -> Dict[str, Any]:
        """Calculate overall wellness score based on habit statistics"""
        
        # Define ideal ranges for habits (these can be customized)
        ideal_ranges = {
            'sleep': {'min': 7, 'max': 9, 'unit': 'hours'},
            'water': {'min': 2, 'max': 4, 'unit': 'liters'},
            'exercise': {'min': 30, 'max': 120, 'unit': 'minutes'},
            'mood': {'min': 6, 'max': 10, 'unit': 'scale'}
        }
        
        total_score = 0
        max_score = 0
        habit_scores = {}
        
        for habit, stats in habit_stats.items():
            if habit in ideal_ranges:
                ideal = ideal_ranges[habit]
                avg_value = stats['average']
                
                # Calculate score based on how close to ideal range
                if ideal['min'] <= avg_value <= ideal['max']:
                    score = 100  # Perfect score
                elif avg_value < ideal['min']:
                    score = max(0, (avg_value / ideal['min']) * 100)
                else:  # avg_value > ideal['max']
                    score = max(0, 100 - ((avg_value - ideal['max']) / ideal['max']) * 50)
                
                # Factor in consistency (frequency)
                consistency_bonus = min(stats['frequency'] * 20, 20)  # Up to 20 bonus points
                final_score = min(100, score + consistency_bonus)
                
                habit_scores[habit] = {
                    'score': round(final_score, 1),
                    'category': self._get_score_category(final_score)
                }
                
                total_score += final_score
                max_score += 100
        
        overall_score = (total_score / max_score * 100) if max_score > 0 else 0
        
        return {
            'overall_score': round(overall_score, 1),
            'overall_category': self._get_score_category(overall_score),
            'habit_scores': habit_scores,
            'tracked_habits': len(habit_scores),
            'scoring_methodology': 'Based on ideal ranges and consistency'
        }
    
    def _get_score_category(self, score: float) -> str:
        """Get category label for wellness score"""
        if score >= 85:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 55:
            return "Fair"
        else:
            return "Needs Improvement"
    
    def _generate_recommendations(self, habit_stats: Dict[str, Dict]) -> List[str]:
        """Generate wellness recommendations based on habit statistics"""
        recommendations = []
        
        for habit, stats in habit_stats.items():
            avg_value = stats['average']
            frequency = stats['frequency']
            trend = stats['trend']
            
            # Frequency-based recommendations
            if frequency < 0.5:  # Less than every other day
                recommendations.append(f"Consider tracking {habit} more consistently")
            
            # Trend-based recommendations
            if trend == "declining":
                recommendations.append(f"Your {habit} trend is declining - consider ways to improve")
            elif trend == "improving":
                recommendations.append(f"Great job! Your {habit} is improving")
            
            # Habit-specific recommendations
            if habit == "sleep" and avg_value < 7:
                recommendations.append("Consider improving sleep hygiene for better rest")
            elif habit == "water" and avg_value < 2:
                recommendations.append("Try to increase daily water intake")
            elif habit == "exercise" and avg_value < 30:
                recommendations.append("Aim for at least 30 minutes of daily physical activity")
            elif habit == "mood" and avg_value < 6:
                recommendations.append("Consider stress management or speaking with a counselor")
        
        # Add general recommendations
        if len(habit_stats) < 3:
            recommendations.append("Try tracking more aspects of your wellness for better insights")
        
        return recommendations[:5]  # Limit to top 5 recommendations
