"""
Typer-based CLI commands for the AI Wellness Assistant
"""

import typer
from typing import Optional
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from wellness_assistant.core.tracker import HabitTracker
from wellness_assistant.core.advice import WellnessAdvisor
from wellness_assistant.core.symptoms import SymptomDetector
from wellness_assistant.core.export import DataExporter
from wellness_assistant.utils.validators import ValidationError

# Initialize Typer app and Rich console
app = typer.Typer(
    name="wellness",
    help="🌟 AI Wellness Assistant - Track habits, get AI advice, and monitor health",
    add_completion=False
)
console = Console()

# Initialize core components
tracker = HabitTracker()
advisor = WellnessAdvisor()
symptom_detector = SymptomDetector()
exporter = DataExporter()

@app.command("track")
def track_habit(
    habit: str = typer.Argument(..., help="Habit to track (sleep, water, exercise, mood, meals)"),
    value: float = typer.Argument(..., help="Value to record"),
    unit: str = typer.Argument(..., help="Unit of measurement"),
    notes: Optional[str] = typer.Option(None, "--notes", "-n", help="Optional notes"),
    date: Optional[str] = typer.Option(None, "--date", "-d", help="Date (YYYY-MM-DD, defaults to today)")
) -> None:
    """📊 Track a daily habit with timestamp"""
    
    try:
        # Parse date if provided
        timestamp = None
        if date:
            from wellness_assistant.utils.validators import Validators
            timestamp = Validators.validate_date(date)
        
        # Track the habit
        success = tracker.track_habit(habit, value, unit, notes, timestamp)
        
        if success:
            console.print(f"✅ Successfully tracked {habit}: {value} {unit}", style="green")
            if notes:
                console.print(f"📝 Note: {notes}", style="dim")
        else:
            console.print("❌ Failed to track habit", style="red")
            
    except ValidationError as e:
        console.print(f"❌ Validation Error: {e}", style="red")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")
        raise typer.Exit(1)

@app.command("quick")
def quick_track() -> None:
    """🎯 Quick interactive habit tracking session"""
    console.print("🎯 Quick Habit Tracking Session", style="bold blue")
    tracker.quick_track()

@app.command("summary")
def show_summary(
    days: int = typer.Option(7, "--days", "-d", help="Number of days to include"),
    habit: Optional[str] = typer.Option(None, "--habit", "-h", help="Filter by specific habit")
) -> None:
    """📈 Show habit summary and trends"""
    
    if habit:
        console.print(f"📈 Showing trends for {habit}", style="bold blue")
        tracker.show_trends(habit, days)
    else:
        console.print(f"📊 Habit Summary (Last {days} days)", style="bold blue")
        tracker.display_summary(days)

@app.command("ask")
def ask_advice(
    question: str = typer.Argument(..., help="Your wellness question"),
    no_context: bool = typer.Option(False, "--no-context", help="Don't include habit data as context")
) -> None:
    """🤖 Get personalized AI wellness advice"""
    
    console.print("🤖 Getting AI wellness advice...", style="bold blue")
    
    try:
        advice = advisor.get_personalized_advice(question, include_context=not no_context)
        
        # Display advice in a nice panel
        console.print(Panel(advice, title="AI Wellness Advice", border_style="blue"))
        
    except Exception as e:
        console.print(f"❌ Error getting advice: {e}", style="red")
        raise typer.Exit(1)

@app.command("chat")
def interactive_chat() -> None:
    """💬 Interactive AI wellness chat session"""
    console.print("💬 Starting interactive AI wellness chat", style="bold blue")
    advisor.ask_interactive()

@app.command("symptom")
def check_symptoms(
    description: Optional[str] = typer.Argument(None, help="Description of symptoms")
) -> None:
    """🩺 Check symptoms for red flags and warnings"""
    
    if description:
        # Analyze provided symptoms
        console.print("🩺 Analyzing symptoms...", style="bold blue")
        analysis = symptom_detector.analyze_symptoms(description)
        
        if "error" in analysis:
            console.print(f"❌ {analysis['error']}", style="red")
        else:
            # Display results with appropriate styling
            urgency_colors = {
                "emergency": "red",
                "urgent": "yellow",
                "moderate": "blue",
                "low": "green"
            }
            
            urgency = analysis.get("urgency_level", "low")
            color = urgency_colors.get(urgency, "white")
            
            console.print(Panel(
                analysis["response"], 
                title=f"Symptom Analysis - {urgency.title()} Priority",
                border_style=color
            ))
    else:
        # Interactive symptom checker
        console.print("🩺 Interactive Symptom Checker", style="bold blue")
        symptom_detector.check_symptoms_interactive()

@app.command("tips")
def get_tips(
    habit: Optional[str] = typer.Argument(None, help="Get tips for specific habit"),
    daily: bool = typer.Option(False, "--daily", help="Get daily wellness tip")
) -> None:
    """💡 Get wellness tips and suggestions"""
    
    if daily:
        tip = advisor.get_daily_wellness_tip()
        console.print(Panel(tip, title="Daily Wellness Tip", border_style="green"))
    elif habit:
        suggestions = advisor.get_habit_suggestions(habit)
        console.print(Panel(suggestions, title=f"Tips for {habit.title()}", border_style="blue"))
    else:
        console.print("💡 Available tip options:", style="bold blue")
        console.print("• Use --daily for daily wellness tip")
        console.print("• Specify a habit (sleep, water, exercise, mood) for specific tips")

@app.command("history")
def show_history(
    habit: Optional[str] = typer.Option(None, "--habit", "-h", help="Filter by habit"),
    days: int = typer.Option(7, "--days", "-d", help="Number of days to show"),
    limit: int = typer.Option(20, "--limit", "-l", help="Maximum entries to show")
) -> None:
    """📜 Show recent habit entries"""
    
    entries = tracker.get_recent_entries(habit, days)
    
    if not entries:
        console.print(f"📜 No entries found for the last {days} days", style="yellow")
        return
    
    # Create a table for displaying entries
    table = Table(title=f"Recent Habit Entries ({len(entries)} entries)")
    table.add_column("Date", style="cyan")
    table.add_column("Habit", style="magenta")
    table.add_column("Value", style="green")
    table.add_column("Unit", style="blue")
    table.add_column("Notes", style="dim")
    
    for entry in entries[:limit]:
        date_str = entry.timestamp.strftime("%Y-%m-%d %H:%M")
        notes = entry.notes or ""
        table.add_row(
            date_str,
            entry.habit.title(),
            str(entry.value),
            entry.unit,
            notes[:30] + "..." if len(notes) > 30 else notes
        )
    
    console.print(table)

@app.command("export")
def export_data(
    format: str = typer.Option("csv", "--format", "-f", help="Export format (csv, json)"),
    days: int = typer.Option(30, "--days", "-d", help="Number of days to export"),
    habit: Optional[str] = typer.Option(None, "--habit", "-h", help="Filter by specific habit"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output filename")
) -> None:
    """📤 Export habit data to CSV or JSON"""
    
    try:
        console.print(f"📤 Exporting {days} days of data...", style="bold blue")
        
        if format.lower() == "csv":
            filepath = exporter.export_habits_csv(
                habit_filter=habit,
                start_date=datetime.now() - timedelta(days=days)
            )
            console.print(f"✅ CSV exported to: {filepath}", style="green")
            
        elif format.lower() == "json":
            filepath = exporter.export_wellness_report(days=days)
            console.print(f"✅ Wellness report exported to: {filepath}", style="green")
            
        else:
            console.print("❌ Unsupported format. Use 'csv' or 'json'", style="red")
            raise typer.Exit(1)
            
    except Exception as e:
        console.print(f"❌ Export failed: {e}", style="red")
        raise typer.Exit(1)

@app.command("config")
def show_config() -> None:
    """⚙️ Show configuration information"""
    
    from wellness_assistant.utils.config import Config
    
    config_info = f"""
🔧 Configuration Information:

Database: {'SQLite' if tracker.storage.use_sqlite else 'JSON'}
Storage Path: {tracker.storage.db_path if tracker.storage.use_sqlite else tracker.storage.json_path}
AI Service: {'Gemini API' if Config.GEMINI_API_KEY else 'Fallback mode (no API key)'}
Debug Mode: {Config.DEBUG}

📊 Available Habits: {', '.join(tracker.storage.VALID_HABITS.keys() if hasattr(tracker.storage, 'VALID_HABITS') else 'sleep, water, exercise, mood, meals')}

⚠️  Remember to set your GEMINI_API_KEY in .env file for AI features
    """
    
    console.print(Panel(config_info.strip(), title="Configuration", border_style="cyan"))

@app.command("version")
def show_version() -> None:
    """ℹ️ Show version information"""
    
    version_info = """
🌟 AI Wellness Assistant v1.0.0

Focused on UN Sustainable Development Goal 3: Good Health and Well-being

Features:
• Habit tracking with SQLite/JSON storage
• AI-powered wellness advice via Google Gemini
• Red-flag symptom detection with warnings
• Rich terminal interface with Typer

Built with: Python, Typer, Rich, SQLite, Google Gemini API
    """
    
    console.print(Panel(version_info.strip(), title="Version Information", border_style="blue"))

@app.callback()
def main() -> None:
    """
    🌟 AI Wellness Assistant
    
    A terminal-based wellness tracking application focused on 
    UN Sustainable Development Goal 3: Good Health and Well-being.
    
    Track habits, get AI advice, and monitor your wellness journey!
    """
    pass

if __name__ == "__main__":
    app()
