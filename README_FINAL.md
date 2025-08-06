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

## 🎯 **Overview**

The AI Wellness Assistant is a modern, user-friendly application designed to help users track their health habits, receive personalized AI-powered wellness advice, and monitor their overall well-being. With both web and command-line interfaces, it offers flexibility and convenience for all types of users.

## ✨ **Key Features**

### 🏥 **Health Tracking**
- **Habit Monitoring**: Track sleep, water intake, exercise, mood, and custom habits
- **Progress Visualization**: View detailed summaries and historical data
- **Data Export**: Export your wellness data in JSON and CSV formats
- **Smart Analytics**: Get insights into your health patterns

### 🤖 **AI-Powered Advice**
- **Personalized Recommendations**: Get tailored wellness advice based on your data
- **Natural Language Processing**: Ask questions in plain English
- **Context-Aware Responses**: Advice considers your tracking history
- **Evidence-Based Suggestions**: Recommendations based on health best practices

### 🩺 **Symptom Analysis**
- **Symptom Checker**: Analyze symptoms with severity tracking
- **Risk Assessment**: Identify when to seek professional medical care
- **Health Monitoring**: Track symptom patterns over time
- **Medical Disclaimers**: Clear guidance on when to consult healthcare professionals

### 🌐 **Dual Interface Options**
- **Web Dashboard**: Beautiful, intuitive web interface
- **Command Line**: Powerful CLI for quick interactions and automation
- **Cross-Platform**: Works on Windows, macOS, and Linux

---

## 🚀 **Quick Start**

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-wellness-assistant.git
   cd ai-wellness-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python start.py
   ```

### Usage Options

#### 🌐 Web Interface (Recommended)
```bash
python start.py
# Choose option 1: Web Interface
# Visit http://localhost:5000
```

#### 💻 Command Line Interface
```bash
python start.py
# Choose option 2: CLI
# OR
python main.py --help
```

#### ⚡ Quick Tracking
```bash
python main.py quick
```

---

## 📁 **Project Structure**

```
ai-wellness-assistant/
├── 📄 main.py                 # CLI entry point
├── 🌐 web_server.py           # Flask web server
├── 🚀 start.py                # Application launcher
├── 📋 requirements.txt        # Python dependencies
├── 📝 README.md               # This file
├── 🔒 .gitignore              # Git ignore rules
├── 📊 data/                   # Data storage
│   ├── habits.json           # Habit tracking data
│   └── wellness.db           # SQLite database
├── 📤 exports/                # Exported data files
├── 🎨 frontend/               # Web interface
│   ├── templates/
│   │   ├── index.html         # Main web dashboard
│   │   └── index_complex.html # Advanced UI backup
│   └── static/
│       ├── css/
│       │   └── style.css      # Stylesheet
│       └── js/
│           └── app.js         # JavaScript functionality
└── 🧠 wellness_assistant/     # Core application
    ├── cli/                   # Command line interface
    ├── core/                  # Core functionality
    │   ├── tracker.py         # Habit tracking
    │   ├── advice.py          # AI advice system
    │   ├── symptoms.py        # Symptom analysis
    │   ├── storage.py         # Data persistence
    │   └── export.py          # Data export
    └── utils/                 # Utilities
        ├── config.py          # Configuration
        └── validators.py      # Input validation
```

---

## 🎨 **Web Interface Features**

### 📊 Dashboard
- **Quick Overview**: See your wellness summary at a glance
- **Quick Actions**: Fast-track common habits with one-click buttons
- **Recent Activity**: View your latest tracking entries
- **Progress Charts**: Visual representation of your wellness journey

### 📝 Habit Tracking
- **Multiple Habit Types**: Sleep, water, exercise, mood, and custom habits
- **Flexible Units**: Track in hours, glasses, minutes, scale ratings, etc.
- **Notes Support**: Add context and observations to your entries
- **Instant Feedback**: Immediate confirmation and success messages

### 🤖 AI Wellness Advisor
- **Chat Interface**: Natural conversation with the AI assistant
- **Personalized Advice**: Get recommendations based on your specific situation
- **Topic Variety**: Sleep, exercise, nutrition, stress management, and more
- **Evidence-Based**: All advice backed by health and wellness research

### 🩺 Symptom Checker
- **Symptom Description**: Describe symptoms in your own words
- **Severity Rating**: Rate symptoms on a 1-10 scale
- **Duration Tracking**: Track how long symptoms have persisted
- **Risk Assessment**: Get guidance on whether to seek medical attention

### 📈 History & Analytics
- **Detailed History**: View all your tracking entries with timestamps
- **Filtering Options**: Filter by habit type, date range, or keywords
- **Export Options**: Download your data for external analysis
- **Pattern Recognition**: Identify trends in your wellness data

---

## 🔧 **Technical Details**

### Backend Technologies
- **Python 3.8+**: Core programming language
- **Flask**: Lightweight web framework
- **SQLite**: Local database for data persistence
- **JSON**: Configuration and data interchange

### Frontend Technologies
- **HTML5**: Modern semantic markup
- **CSS3**: Clean, responsive styling with gradients and animations
- **JavaScript ES6+**: Interactive functionality and API communication
- **Font Awesome**: Beautiful icons throughout the interface
- **Responsive Design**: Mobile-first approach for all screen sizes

### API Endpoints
- `GET /` - Main dashboard
- `POST /api/track` - Track a habit
- `GET /api/summary` - Get wellness summary
- `POST /api/advice` - Get AI advice
- `POST /api/symptoms` - Analyze symptoms
- `GET /api/history` - Get tracking history
- `GET /api/export` - Export data

---

## 📝 **Usage Examples**

### Habit Tracking via CLI
```bash
# Track sleep
python main.py track sleep 8 hours

# Track water intake
python main.py track water 6 glasses

# Track exercise with notes
python main.py track exercise 45 minutes --notes "Morning jog in the park"

# Get summary
python main.py summary

# Quick mood check
python main.py quick
```

### Web Interface
1. **Start the web server**: `python start.py` → Choose option 1
2. **Open your browser**: Visit `http://localhost:5000`
3. **Track habits**: Use the simple forms or quick-action buttons
4. **Get AI advice**: Ask questions in the AI advisor tab
5. **Check symptoms**: Use the symptom checker for health insights
6. **View history**: See all your entries in the history tab

---

## 🔒 **Privacy & Security**

- **Local Data Storage**: All data is stored locally on your device
- **No External Servers**: Your personal health data never leaves your computer
- **Open Source**: Full transparency - review the code yourself
- **No Tracking**: No analytics or user behavior tracking
- **GDPR Compliant**: Designed with privacy regulations in mind

---

## 🤝 **Contributing**

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**: Add features, fix bugs, improve documentation
4. **Run tests**: Ensure everything works correctly
5. **Commit changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**: Describe your changes and submit for review

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/ai-wellness-assistant.git
cd ai-wellness-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python web_server.py
```

---

## 📋 **Roadmap**

### Upcoming Features
- [ ] **Data Visualization**: Charts and graphs for habit trends
- [ ] **Goal Setting**: Set and track wellness goals
- [ ] **Reminders**: Notifications for habit tracking
- [ ] **Mobile App**: Native mobile applications
- [ ] **Advanced Analytics**: Machine learning insights
- [ ] **Integration**: Connect with fitness devices and health apps
- [ ] **Social Features**: Share progress with friends (optional)
- [ ] **Backup & Sync**: Cloud backup options

### Technical Improvements
- [ ] **Docker Support**: Containerized deployment
- [ ] **API Documentation**: Comprehensive API docs
- [ ] **Unit Tests**: Complete test coverage
- [ ] **Performance**: Database optimization
- [ ] **Security**: Enhanced security measures

---

## 🐛 **Troubleshooting**

### Common Issues

**Issue**: Web server won't start
**Solution**: Check if port 5000 is available, or modify the port in `web_server.py`

**Issue**: Dependencies not installing
**Solution**: Ensure you have Python 3.8+ and try `pip install --upgrade pip`

**Issue**: Database errors
**Solution**: Delete `data/wellness.db` to reset the database

**Issue**: AI advice not working
**Solution**: Ensure all dependencies are installed correctly

### Getting Help
- **Check the Issues**: Look for existing solutions on GitHub
- **Create an Issue**: Report bugs or request features
- **Contact**: Reach out via GitHub or email

---

## 📜 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 AI Wellness Assistant

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 **Acknowledgments**

- **UN Sustainable Development Goals**: Inspired by Goal 3 - Good Health and Well-being
- **Open Source Community**: For the amazing tools and libraries
- **Health & Wellness Experts**: For evidence-based guidance
- **Users & Contributors**: For feedback and improvements

---

<div align="center">

**Made with ❤️ for better health and well-being**

![Health](https://img.shields.io/badge/🏥%20Health-First-blue?style=flat-square)
![Wellness](https://img.shields.io/badge/🧘%20Wellness-Focused-green?style=flat-square)
![Privacy](https://img.shields.io/badge/🔒%20Privacy-Protected-orange?style=flat-square)
![Open Source](https://img.shields.io/badge/💝%20Open%20Source-Forever-red?style=flat-square)

**⭐ If this project helped you, please consider giving it a star! ⭐**

</div>
