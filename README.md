# 🌟 AI Wellness Assistant

<div align="center">

![AI Wellness Assistant](https://img.shields.io/badge/🌟%20AI%20Wellness%20Assistant-Health%20%26%20Wellbeing-brightgreen?style=for-the-badge&labelColor=4CAF50&color=45a049)

**A comprehensive AI-powered wellness tracking and advisory system**  
*Supporting UN Sustainable Development Goal 3: Good Health and Well-being*

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

---

## � **Overview**

The AI Wellness Assistant is a modern, user-friendly application designed to help users track their health habits, receive personalized AI-powered wellness advice, and monitor their overall well-being. With both web and command-line interfaces, it offers flexibility and convenience for all types of users.

<div align="center">

| 🏠 **Dashboard** | 📊 **Tracking** | 🤖 **AI Advice** | 🚨 **Symptoms** |
|:---:|:---:|:---:|:---:|
| Beautiful overview | Smart habit logging | Personalized guidance | Health monitoring |
| Real-time charts | Progress visualization | Gemini AI integration | Emergency detection |
| Quick actions | Trend analysis | Contextual responses | Safety protocols |

</div>

### 📱 **Dual Interface Experience**
- **🌐 Web Dashboard**: Stunning Tailwind CSS interface with animations
- **💻 CLI Interface**: Powerful terminal commands for power users

### 📊 **Smart Habit Tracking**
- 🎯 Track: Sleep, Water, Exercise, Mood, Meals
- ⏰ Timestamp validation and smart suggestions
- 📈 Visual progress tracking with animated charts
- 🎨 Beautiful data visualization components

### 🤖 **AI-Powered Wellness**
- 🧠 Google Gemini AI integration
- 💡 Personalized health recommendations
- 🛡️ Ethical guidelines and privacy protection
- 📝 Context-aware response generation

### 🚨 **Health Monitoring**
- ⚠️ Real-time symptom analysis
- 🚑 Emergency alert system
- 🏥 Professional medical guidance
- 📋 Health trend monitoring

---

## 🚀 **Quick Start Guide**

### 📦 **Installation**

```bash
# Clone the repository
git clone https://github.com/your-username/ai-wellness-assistant.git
cd ai-wellness-assistant

# Install dependencies
pip install -r requirements.txt

# Set up environment (optional, for AI features)
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 🎮 **Launch Options**

<table>
<tr>
<td width="50%">

#### 🌐 **Web Interface** (Recommended)
```bash
# Interactive startup menu
python start.py

# Or direct web server
python web_server.py
```

Then visit: **http://localhost:5000**

</td>
<td width="50%">

#### 💻 **CLI Interface**
```bash
# Show all commands
python main.py --help

# Quick interactive mode
python main.py quick

# Direct tracking
python main.py track sleep 8 hours
```

</td>
</tr>
</table>

---

## 💻 **Command Line Usage**

<details>
<summary><b>🔽 Click to expand CLI commands</b></summary>

```bash
# 📊 Habit Tracking
python main.py track sleep 8 hours --notes "Great sleep!"
python main.py track water 2.5 liters
python main.py track exercise 45 minutes --notes "Morning run"
python main.py track mood 8 --notes "Feeling energetic"

# 🤖 AI Wellness Advice
python main.py ask "How can I improve my energy levels?"
python main.py ask "What's the best sleep schedule?"

# 🚨 Symptom Checking
python main.py symptom "I have a mild headache"
python main.py symptom "feeling tired lately"

# 📈 Analytics & Reports
python main.py summary --days 7
python main.py history --habit sleep
python main.py export --format csv --days 30
```

</details>

---

## 🎨 **UI Screenshots**

<div align="center">

### 🏠 **Dashboard Overview**
![Dashboard](https://via.placeholder.com/600x300/667eea/ffffff?text=🏠+Modern+Dashboard+with+Glassmorphism)

### 📊 **Habit Tracking**
![Tracking](https://via.placeholder.com/600x300/4CAF50/ffffff?text=📊+Beautiful+Habit+Tracking)

### 🤖 **AI Assistant**
![AI Assistant](https://via.placeholder.com/600x300/2196F3/ffffff?text=🤖+AI+Powered+Advice)

</div>

---

## 🛠️ **Technology Stack**

<div align="center">

| **Frontend** | **Backend** | **AI/ML** | **Tools** |
|:---:|:---:|:---:|:---:|
| ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) | ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) | ![Google AI](https://img.shields.io/badge/Google%20AI-4285F4?style=for-the-badge&logo=google&logoColor=white) | ![VS Code](https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white) |
| ![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white) | ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) | ![Gemini](https://img.shields.io/badge/Gemini%20AI-8E75B2?style=for-the-badge&logo=google&logoColor=white) | ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white) |
| ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) | ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white) | ![Typer](https://img.shields.io/badge/Typer-009639?style=for-the-badge&logo=python&logoColor=white) | ![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white) |

</div>

---

## 📁 **Project Structure**

```
🌟 ai-wellness-assistant/
├── 📁 frontend/                    # Modern UI components
│   ├── 📁 static/
│   │   ├── 📁 css/                # Tailwind CSS + Custom styles
│   │   │   └── 🎨 style.css       # Enhanced glassmorphism design
│   │   └── 📁 js/                 # Interactive JavaScript
│   │       └── ⚡ app.js          # Dynamic functionality
│   └── 📁 templates/              # HTML templates
│       └── 🏠 index.html          # Main dashboard
├── 📁 wellness_assistant/          # Core Python package
│   ├── 📁 core/                   # Business logic
│   │   ├── 📊 tracker.py          # Habit tracking engine
│   │   ├── 🤖 advice.py           # AI advice system
│   │   ├── 🚨 symptoms.py         # Health monitoring
│   │   ├── 💾 storage.py          # Data management
│   │   └── 📤 export.py           # Data export utilities
│   ├── 📁 cli/                    # Command line interface
│   │   └── 💻 commands.py         # Typer CLI commands
│   └── 📁 utils/                  # Utilities
│       ├── ⚙️ config.py           # Configuration
│       └── ✅ validators.py       # Input validation
├── 📁 data/                       # Local data storage
│   ├── 📊 habits.json             # User habit data
│   └── 🗃️ wellness.db            # SQLite database
├── 📁 exports/                    # Data exports
│   └── 📝 README.md               # Export documentation
├── 🐍 main.py                     # CLI entry point
├── 🌐 web_server.py               # Flask web server
├── 🚀 start.py                    # Interactive startup
├── 📋 requirements.txt            # Python dependencies
├── 🙈 .gitignore                  # Git ignore rules
├── 📖 README.md                   # This documentation
└── ⚙️ .env.example                # Environment template
```

---

## 🚀 **Publishing to GitHub**

<details>
<summary><b>🔽 Ready to share your project? Click here!</b></summary>

### 1. **Initialize Repository**
```bash
git init
git add .
git commit -m "🎉 Initial commit: AI Wellness Assistant with Tailwind CSS UI"
```

### 2. **Create GitHub Repository**
1. Go to [GitHub](https://github.com) → **New Repository**
2. Name: `ai-wellness-assistant`
3. Description: `🌟 Modern AI Wellness Assistant with Tailwind CSS and Glassmorphism Design`
4. **Don't** initialize with README (we have our own!)

### 3. **Connect and Push**
```bash
git remote add origin https://github.com/YOUR_USERNAME/ai-wellness-assistant.git
git branch -M main
git push -u origin main
```

### 4. **Setup Instructions for Users**
Add these steps to your GitHub repository description:
- 📥 Clone the repository
- 📝 Copy `.env.example` to `.env`
- 🔑 Add Google Gemini API key
- 📦 Run `pip install -r requirements.txt`
- 🚀 Launch with `python start.py`

</details>

---

## 🎯 **Contributing**

<div align="center">

[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen?style=for-the-badge&logo=github)](CONTRIBUTING.md)
[![Code of Conduct](https://img.shields.io/badge/Code%20of%20Conduct-Ethical%20AI-blue?style=for-the-badge)](CODE_OF_CONDUCT.md)

</div>

We welcome contributions that align with our ethical AI principles and focus on supporting users' health and well-being journey.

### 🌟 **Ways to Contribute**
- 🐛 **Bug Reports**: Help us improve stability
- ✨ **Feature Requests**: Suggest new wellness features
- 🎨 **UI Improvements**: Enhance the visual experience
- 📖 **Documentation**: Improve guides and tutorials
- 🔧 **Code Quality**: Refactoring and optimization

---

## 📜 **License & Ethics**

<div align="center">

[![MIT License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Ethical AI](https://img.shields.io/badge/Ethical%20AI-Committed-green?style=for-the-badge)](https://www.partnershiponai.org/)

</div>

### 🛡️ **Ethical Guidelines**
- 🏥 **Medical Disclaimer**: General wellness guidance only
- 👨‍⚕️ **Professional Care**: Not a substitute for medical advice
- 🔒 **Privacy First**: All data stored locally
- 🤖 **Responsible AI**: Ethical AI responses with disclaimers

---

<div align="center">

## 🌟 **Ready to Transform Your Wellness Journey?**

[![Get Started](https://img.shields.io/badge/🚀%20Get%20Started-Launch%20Now-success?style=for-the-badge&labelColor=4CAF50&color=45a049)](https://github.com/your-username/ai-wellness-assistant)
[![View Demo](https://img.shields.io/badge/👀%20View%20Demo-Live%20Preview-blue?style=for-the-badge&labelColor=2196F3&color=1976D2)](http://localhost:5000)

**Your beautiful AI wellness assistant with modern Tailwind CSS design is ready to help you achieve better health and well-being!** ✨

---

*Made with ❤️ for better health and well-being | Supporting UN SDG 3*

</div>
