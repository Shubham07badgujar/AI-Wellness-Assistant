"""
AI-powered wellness advice using Google Gemini
"""

import os
from typing import Optional, Dict, Any
from datetime import datetime
import google.generativeai as genai
from wellness_assistant.utils.config import Config
from wellness_assistant.core.storage import StorageManager

class WellnessAdvisor:
    """Provides AI-powered wellness advice using Google Gemini"""
    
    def __init__(self, storage_manager: Optional[StorageManager] = None):
        """Initialize wellness advisor
        
        Args:
            storage_manager: Optional storage manager for context
        """
        self.storage = storage_manager or StorageManager()
        self.api_key = Config.GEMINI_API_KEY
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
            print("⚠️  Warning: GEMINI_API_KEY not found. AI advice features disabled.")
    
    def get_personalized_advice(self, query: str, include_context: bool = True) -> str:
        """Get personalized wellness advice
        
        Args:
            query: User's wellness question
            include_context: Whether to include user's habit data as context
            
        Returns:
            AI-generated wellness advice with disclaimer
        """
        if not self.model:
            return self._get_fallback_advice(query)
        
        try:
            # Build the prompt
            prompt = self._build_advice_prompt(query, include_context)
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            # Format response with disclaimer
            advice = self._format_advice_response(response.text, query)
            
            return advice
            
        except Exception as e:
            print(f"❌ Error getting AI advice: {e}")
            return self._get_fallback_advice(query)
    
    def _build_advice_prompt(self, query: str, include_context: bool) -> str:
        """Build the prompt for AI advice generation
        
        Args:
            query: User's question
            include_context: Whether to include habit context
            
        Returns:
            Formatted prompt for AI
        """
        prompt_parts = []
        
        # System instructions
        prompt_parts.append("""
You are a wellness assistant focused on UN Sustainable Development Goal 3: Good Health and Well-being.
Provide helpful, evidence-based wellness advice while following these guidelines:

IMPORTANT GUIDELINES:
- You are NOT a doctor and cannot diagnose medical conditions
- Always include appropriate disclaimers about seeking professional medical advice
- Focus on general wellness, healthy habits, and lifestyle improvements
- Be supportive and encouraging
- Avoid giving specific medical treatments or medication advice
- If symptoms sound serious, recommend consulting a healthcare professional

Your advice should be:
- Practical and actionable
- Evidence-based when possible
- Supportive and encouraging
- Focused on prevention and wellness
- Appropriate for general audiences
        """)
        
        # Add user context if available
        if include_context:
            context = self._get_user_context()
            if context:
                prompt_parts.append(f"\nUser's recent wellness data:\n{context}")
        
        # Add the user's question
        prompt_parts.append(f"\nUser's question: {query}")
        
        # Add output formatting instructions
        prompt_parts.append("""
Please provide helpful wellness advice in a friendly, supportive tone. 
Keep your response concise but informative (2-3 paragraphs maximum).
Always end with an appropriate disclaimer about consulting healthcare professionals.
        """)
        
        return "\n".join(prompt_parts)
    
    def _get_user_context(self) -> str:
        """Get user's recent habit data for context
        
        Returns:
            Formatted string with user's recent habits
        """
        try:
            summary = self.storage.get_habit_summary(days=7)
            
            if not summary:
                return "No recent habit data available."
            
            context_parts = ["Recent habits (last 7 days):"]
            
            for habit, data in summary.items():
                avg = data['average']
                context_parts.append(f"- {habit}: {avg:.1f} {data['unit']}/day (average)")
            
            return "\n".join(context_parts)
            
        except Exception as e:
            return f"Unable to retrieve context: {e}"
    
    def _format_advice_response(self, ai_response: str, original_query: str) -> str:
        """Format the AI response with proper structure and disclaimer
        
        Args:
            ai_response: Raw AI response
            original_query: Original user question
            
        Returns:
            Formatted response with disclaimer
        """
        formatted_response = []
        
        # Header
        formatted_response.append("🤖 AI Wellness Advice")
        formatted_response.append("=" * 30)
        
        # Main advice
        formatted_response.append(ai_response.strip())
        
        # Disclaimer
        formatted_response.append(f"\n{Config.MEDICAL_DISCLAIMER}")
        
        # Additional resources
        formatted_response.append("\n💡 Additional Resources:")
        formatted_response.append("• Stay hydrated and maintain regular sleep schedule")
        formatted_response.append("• Regular physical activity (150+ minutes/week)")
        formatted_response.append("• Balanced nutrition with fruits and vegetables")
        formatted_response.append("• Stress management and mindfulness practices")
        
        return "\n".join(formatted_response)
    
    def _get_fallback_advice(self, query: str) -> str:
        """Provide fallback advice when AI is unavailable
        
        Args:
            query: User's question
            
        Returns:
            Generic wellness advice
        """
        query_lower = query.lower()
        
        # Basic keyword-based responses
        if any(word in query_lower for word in ["sleep", "tired", "fatigue"]):
            advice = """
For better sleep and energy levels:
• Aim for 7-9 hours of sleep per night
• Maintain a consistent sleep schedule
• Create a relaxing bedtime routine
• Limit screen time before bed
• Keep your bedroom cool and dark
            """
        
        elif any(word in query_lower for word in ["exercise", "fitness", "activity"]):
            advice = """
For physical activity and fitness:
• Aim for at least 150 minutes of moderate exercise per week
• Include both cardio and strength training
• Start slowly and gradually increase intensity
• Find activities you enjoy
• Consider walking, swimming, or cycling
            """
        
        elif any(word in query_lower for word in ["stress", "anxiety", "mental"]):
            advice = """
For stress management and mental wellness:
• Practice deep breathing or meditation
• Maintain social connections
• Get regular physical activity
• Ensure adequate sleep
• Consider professional counseling if needed
            """
        
        elif any(word in query_lower for word in ["nutrition", "diet", "eating"]):
            advice = """
For healthy nutrition:
• Eat a variety of fruits and vegetables
• Choose whole grains over refined grains
• Include lean proteins in your diet
• Stay hydrated with plenty of water
• Limit processed foods and added sugars
            """
        
        else:
            advice = """
General wellness tips:
• Maintain a balanced diet with fruits and vegetables
• Get regular physical activity (150+ minutes/week)
• Ensure adequate sleep (7-9 hours per night)
• Stay hydrated throughout the day
• Practice stress management techniques
• Maintain social connections
            """
        
        return f"""🤖 Wellness Guidance
={30}

{advice.strip()}

{Config.MEDICAL_DISCLAIMER}

Note: AI advice is currently unavailable. These are general wellness guidelines."""
    
    def get_habit_suggestions(self, habit: str) -> str:
        """Get specific suggestions for improving a habit
        
        Args:
            habit: Name of the habit to improve
            
        Returns:
            Suggestions for the specific habit
        """
        suggestions = {
            "sleep": [
                "Maintain a consistent bedtime and wake time",
                "Create a relaxing bedtime routine",
                "Limit caffeine after 2 PM",
                "Keep your bedroom cool and dark",
                "Avoid screens 1 hour before bed",
                "Try relaxation techniques like deep breathing"
            ],
            "water": [
                "Start your day with a glass of water",
                "Carry a water bottle with you",
                "Set reminders to drink water throughout the day",
                "Eat water-rich foods like fruits and vegetables",
                "Flavor water with lemon or cucumber if plain water is boring"
            ],
            "exercise": [
                "Start with 10-15 minutes of activity daily",
                "Choose activities you enjoy",
                "Take the stairs instead of elevators",
                "Park farther away to increase walking",
                "Try bodyweight exercises at home",
                "Find a workout buddy for motivation"
            ],
            "mood": [
                "Practice gratitude by writing down 3 good things daily",
                "Connect with friends and family regularly",
                "Spend time in nature",
                "Practice mindfulness or meditation",
                "Engage in hobbies you enjoy",
                "Limit negative media consumption"
            ]
        }
        
        habit_suggestions = suggestions.get(habit, [
            "Set specific, achievable goals",
            "Track your progress regularly",
            "Celebrate small wins",
            "Be patient with yourself",
            "Seek support when needed"
        ])
        
        formatted = f"""💡 Tips for Improving {habit.title()}:\n"""
        for i, suggestion in enumerate(habit_suggestions, 1):
            formatted += f"{i}. {suggestion}\n"
        
        formatted += f"\n{Config.MEDICAL_DISCLAIMER}"
        
        return formatted
    
    def ask_interactive(self) -> None:
        """Interactive AI advice session"""
        print("\n🤖 AI Wellness Advisor")
        print("Ask me anything about wellness, healthy habits, or general health!")
        print("Type 'quit' to exit.")
        print(Config.MEDICAL_DISCLAIMER)
        
        while True:
            try:
                print("\n💬 What would you like to know about wellness?")
                question = input("> ").strip()
                
                if not question:
                    continue
                
                if question.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Thanks for using the AI Wellness Advisor!")
                    break
                
                # Get and display advice
                print("\n🤔 Thinking...")
                advice = self.get_personalized_advice(question)
                print(f"\n{advice}")
                
            except KeyboardInterrupt:
                print("\n👋 AI Wellness Advisor session ended")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def get_daily_wellness_tip(self) -> str:
        """Get a daily wellness tip
        
        Returns:
            Daily wellness tip
        """
        tips = [
            "💧 Drink a glass of water first thing in the morning to kickstart your metabolism.",
            "🚶 Take a 10-minute walk after meals to aid digestion and boost energy.",
            "😴 Create a wind-down routine 30 minutes before bed for better sleep quality.",
            "🥗 Add one extra serving of vegetables to your meals today.",
            "🧘 Take 5 deep breaths when you feel stressed or overwhelmed.",
            "📱 Put your phone away during meals to practice mindful eating.",
            "🌞 Get 10-15 minutes of sunlight exposure for vitamin D and mood benefits.",
            "💪 Do some light stretching or yoga to improve flexibility and reduce tension.",
            "📝 Write down 3 things you're grateful for to boost your mood.",
            "👥 Reach out to a friend or family member to strengthen social connections."
        ]
        
        # Use current day to get consistent tip for the day
        tip_index = datetime.now().day % len(tips)
        return f"🌟 Daily Wellness Tip:\n{tips[tip_index]}\n\nRemember: Small daily actions lead to big health improvements!"
