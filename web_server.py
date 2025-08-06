#!/usr/bin/env python3
"""
Web server for AI Wellness Assistant
Provides a REST API and serves the HTML frontend
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import json
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from wellness_assistant.core.tracker import HabitTracker
from wellness_assistant.core.advice import WellnessAdvisor
from wellness_assistant.core.symptoms import SymptomDetector
from wellness_assistant.core.export import DataExporter

# Initialize Flask app
app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
CORS(app)

# Initialize wellness components
tracker = HabitTracker()
advisor = WellnessAdvisor()
symptom_detector = SymptomDetector()
exporter = DataExporter()

@app.route('/')
def index():
    """Serve the main dashboard"""
    return render_template('index.html')

@app.route('/api/track', methods=['POST'])
def track_habit():
    """API endpoint to track a habit"""
    try:
        data = request.get_json()
        
        habit = data.get('habit')
        value = float(data.get('value'))
        unit = data.get('unit')
        notes = data.get('notes', '')
        
        success = tracker.track_habit(habit, value, unit, notes)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Successfully tracked {habit}: {value} {unit}'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to track habit'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/api/summary')
def get_summary():
    """API endpoint to get habit summary"""
    try:
        days = request.args.get('days', 7, type=int)
        summary = tracker.get_habit_summary(days)
        
        return jsonify({
            'success': True,
            'summary': summary,
            'period_days': days
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/api/advice', methods=['POST'])
def get_advice():
    """API endpoint to get AI wellness advice"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        include_context = data.get('include_context', True)
        
        advice = advisor.get_personalized_advice(question, include_context)
        
        return jsonify({
            'success': True,
            'advice': advice
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting advice: {str(e)}'
        }), 500

@app.route('/api/symptoms', methods=['POST'])
def check_symptoms():
    """API endpoint to check symptoms"""
    try:
        data = request.get_json()
        description = data.get('description', '')
        
        analysis = symptom_detector.analyze_symptoms(description)
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error analyzing symptoms: {str(e)}'
        }), 500

@app.route('/api/history')
def get_history():
    """API endpoint to get habit history"""
    try:
        habit = request.args.get('habit')
        days = request.args.get('days', 7, type=int)
        limit = request.args.get('limit', 50, type=int)
        
        entries = tracker.get_recent_entries(habit, days)
        
        # Convert entries to JSON-serializable format
        entries_data = []
        for entry in entries[:limit]:
            entries_data.append({
                'habit': entry.habit,
                'value': entry.value,
                'unit': entry.unit,
                'timestamp': entry.timestamp.isoformat(),
                'notes': entry.notes or ''
            })
        
        return jsonify({
            'success': True,
            'entries': entries_data,
            'total': len(entries_data)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting history: {str(e)}'
        }), 500

@app.route('/api/export')
def export_data():
    """API endpoint to export data"""
    try:
        format_type = request.args.get('format', 'json')
        days = request.args.get('days', 30, type=int)
        
        if format_type == 'json':
            filepath = exporter.export_wellness_report(days)
        else:
            filepath = exporter.export_habits_csv(
                start_date=datetime.now() - timedelta(days=days)
            )
        
        return jsonify({
            'success': True,
            'filepath': filepath,
            'message': f'Data exported to {filepath}'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Export failed: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Ensure frontend directories exist
    Path('frontend/templates').mkdir(parents=True, exist_ok=True)
    Path('frontend/static/css').mkdir(parents=True, exist_ok=True)
    Path('frontend/static/js').mkdir(parents=True, exist_ok=True)
    
    print("🌟 AI Wellness Assistant Web Server")
    print("🚀 Starting server at http://localhost:5000")
    print("📊 Web dashboard available at http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
