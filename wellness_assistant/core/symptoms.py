"""
Symptom detection and warning system for the AI Wellness Assistant
"""

import re
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from wellness_assistant.utils.config import Config
from wellness_assistant.utils.validators import Validators

class SymptomDetector:
    """Detects potential red-flag symptoms and provides appropriate warnings"""
    
    def __init__(self):
        """Initialize symptom detector with red flag patterns"""
        self.red_flag_symptoms = Config.RED_FLAG_SYMPTOMS
        self.emergency_advice = {
            "chest": "🚨 URGENT: Chest pain can be a sign of a heart attack. Call emergency services (911) immediately.",
            "breathing": "🚨 URGENT: Difficulty breathing requires immediate medical attention. Call 911.",
            "headache": "🚨 URGENT: Sudden severe headache may indicate stroke or aneurysm. Seek emergency care.",
            "vision": "🚨 URGENT: Sudden vision loss requires immediate medical attention.",
            "weakness": "🚨 URGENT: Sudden weakness may indicate stroke. Call 911 immediately.",
            "consciousness": "🚨 URGENT: Loss of consciousness requires emergency medical care.",
            "blood": "⚠️  Blood in stool, urine, or coughing blood requires immediate medical evaluation.",
            "fever": "⚠️  High fever (over 103°F/39.4°C) requires medical attention.",
            "allergic": "🚨 URGENT: Severe allergic reactions can be life-threatening. Call 911.",
        }
    
    def analyze_symptoms(self, symptom_description: str) -> Dict[str, any]:
        """Analyze symptom description for red flags
        
        Args:
            symptom_description: User's description of symptoms
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Sanitize input
            clean_description = Validators.sanitize_symptom_input(symptom_description)
            
            # Check for red flag symptoms
            red_flags = self._detect_red_flags(clean_description)
            
            # Determine urgency level
            urgency = self._assess_urgency(red_flags)
            
            # Generate appropriate response
            response = self._generate_response(clean_description, red_flags, urgency)
            
            return {
                "original_input": symptom_description,
                "cleaned_input": clean_description,
                "red_flags": red_flags,
                "urgency_level": urgency,
                "response": response,
                "timestamp": datetime.now(),
                "requires_medical_attention": urgency in ["emergency", "urgent"]
            }
            
        except Exception as e:
            return {
                "error": f"Error analyzing symptoms: {e}",
                "response": "Unable to analyze symptoms. Please consult a healthcare professional.",
                "requires_medical_attention": True
            }
    
    def _detect_red_flags(self, description: str) -> List[Dict[str, str]]:
        """Detect red flag symptoms in description
        
        Args:
            description: Cleaned symptom description
            
        Returns:
            List of detected red flag symptoms with categories
        """
        red_flags = []
        description_lower = description.lower()
        
        # Define red flag categories and their patterns
        red_flag_categories = {
            "chest": ["chest pain", "chest pressure", "chest tightness", "heart pain"],
            "breathing": ["shortness of breath", "difficulty breathing", "can't breathe", "trouble breathing"],
            "headache": ["sudden severe headache", "worst headache", "severe headache"],
            "vision": ["vision loss", "loss of vision", "sudden vision changes", "blind", "can't see"],
            "weakness": ["weakness on one side", "facial drooping", "speech problems", "slurred speech"],
            "consciousness": ["loss of consciousness", "fainting", "passed out", "unconscious"],
            "blood": ["blood in stool", "blood in urine", "coughing blood", "vomiting blood"],
            "fever": ["high fever", "fever over 103", "burning up"],
            "allergic": ["severe allergic reaction", "anaphylaxis", "swelling face", "difficulty swallowing"]
        }
        
        for category, patterns in red_flag_categories.items():
            for pattern in patterns:
                if pattern in description_lower:
                    red_flags.append({
                        "category": category,
                        "pattern": pattern,
                        "severity": "high"
                    })
        
        # Check for additional concerning symptoms
        concerning_patterns = [
            "severe pain", "extreme pain", "unbearable pain",
            "sudden onset", "came on suddenly", "started suddenly",
            "getting worse", "worsening", "worse than ever"
        ]
        
        for pattern in concerning_patterns:
            if pattern in description_lower:
                red_flags.append({
                    "category": "concerning",
                    "pattern": pattern,
                    "severity": "medium"
                })
        
        return red_flags
    
    def _assess_urgency(self, red_flags: List[Dict[str, str]]) -> str:
        """Assess urgency level based on detected red flags
        
        Args:
            red_flags: List of detected red flag symptoms
            
        Returns:
            Urgency level: 'emergency', 'urgent', 'moderate', 'low'
        """
        if not red_flags:
            return "low"
        
        emergency_categories = ["chest", "breathing", "consciousness", "allergic"]
        urgent_categories = ["headache", "vision", "weakness", "blood", "fever"]
        
        for flag in red_flags:
            if flag["category"] in emergency_categories:
                return "emergency"
        
        for flag in red_flags:
            if flag["category"] in urgent_categories:
                return "urgent"
        
        # Check for multiple concerning symptoms
        if len(red_flags) >= 3:
            return "urgent"
        
        return "moderate"
    
    def _generate_response(self, description: str, red_flags: List[Dict[str, str]], urgency: str) -> str:
        """Generate appropriate response based on analysis
        
        Args:
            description: Symptom description
            red_flags: Detected red flags
            urgency: Urgency level
            
        Returns:
            Formatted response string
        """
        response = []
        
        # Add urgency-specific warnings
        if urgency == "emergency":
            response.append("🚨 MEDICAL EMERGENCY DETECTED 🚨")
            response.append("This appears to be a medical emergency. Call 911 or emergency services IMMEDIATELY.")
            
            # Add specific emergency advice
            for flag in red_flags:
                if flag["category"] in self.emergency_advice:
                    response.append(self.emergency_advice[flag["category"]])
                    break
        
        elif urgency == "urgent":
            response.append("⚠️  URGENT MEDICAL ATTENTION NEEDED")
            response.append("These symptoms require prompt medical evaluation. Contact your doctor or visit urgent care immediately.")
            
        elif urgency == "moderate":
            response.append("⚠️  Medical Consultation Recommended")
            response.append("Consider scheduling an appointment with your healthcare provider to discuss these symptoms.")
            
        else:
            response.append("ℹ️  General Wellness Information")
            response.append("While these symptoms may not be immediately concerning, monitor them and consult a healthcare professional if they persist or worsen.")
        
        # Add detected symptoms summary
        if red_flags:
            response.append(f"\nDetected concerning symptoms:")
            for flag in red_flags[:3]:  # Limit to top 3 flags
                response.append(f"• {flag['pattern']}")
        
        # Add disclaimer
        response.append(f"\n{Config.MEDICAL_DISCLAIMER}")
        
        # Add general advice
        if urgency in ["low", "moderate"]:
            response.append("\nGeneral self-care tips:")
            response.append("• Stay hydrated")
            response.append("• Get adequate rest")
            response.append("• Monitor symptoms")
            response.append("• Keep a symptom diary")
        
        return "\n".join(response)
    
    def check_symptoms_interactive(self) -> None:
        """Interactive symptom checking session"""
        print("\n🩺 Symptom Checker")
        print("Describe your symptoms below. This tool will help identify if you need immediate medical attention.")
        print(Config.MEDICAL_DISCLAIMER)
        print("\nWhat symptoms are you experiencing?")
        
        try:
            symptoms = input("> ").strip()
            
            if not symptoms:
                print("No symptoms entered.")
                return
            
            # Analyze symptoms
            analysis = self.analyze_symptoms(symptoms)
            
            if "error" in analysis:
                print(f"❌ {analysis['error']}")
                return
            
            # Display results
            print(f"\n{analysis['response']}")
            
            # Log the check (optional)
            if analysis["requires_medical_attention"]:
                print(f"\n📝 This symptom check was logged with urgency level: {analysis['urgency_level']}")
        
        except KeyboardInterrupt:
            print("\n👋 Symptom check cancelled")
        except Exception as e:
            print(f"❌ Error during symptom check: {e}")
    
    def get_symptom_tips(self, symptom_category: str) -> List[str]:
        """Get general tips for common symptom categories
        
        Args:
            symptom_category: Category of symptoms
            
        Returns:
            List of general tips
        """
        tips_database = {
            "headache": [
                "Stay hydrated",
                "Apply cold or warm compress",
                "Practice relaxation techniques",
                "Maintain regular sleep schedule",
                "Limit screen time"
            ],
            "fatigue": [
                "Ensure adequate sleep (7-9 hours)",
                "Exercise regularly",
                "Eat balanced meals",
                "Manage stress",
                "Stay hydrated"
            ],
            "stress": [
                "Practice deep breathing",
                "Try meditation or mindfulness",
                "Exercise regularly",
                "Maintain social connections",
                "Set realistic goals"
            ],
            "digestive": [
                "Eat smaller, more frequent meals",
                "Stay hydrated",
                "Include fiber in your diet",
                "Limit processed foods",
                "Practice mindful eating"
            ]
        }
        
        return tips_database.get(symptom_category, [
            "Monitor symptoms",
            "Stay hydrated",
            "Get adequate rest",
            "Consult healthcare provider if symptoms persist"
        ])
