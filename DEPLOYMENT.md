# Deployment Configuration for AI Wellness Assistant

## 🚀 **Deployment Options**

This AI Wellness Assistant can be deployed on multiple platforms. Choose the option that best fits your needs:

### 🌐 **1. Local Development/Testing**
```bash
# Clone the repository
git clone https://github.com/Shubham07badgujar/Ai-agent.git
cd Ai-agent

# Install dependencies
pip install -r requirements.txt

# Run the application
python start.py
```

### ☁️ **2. Cloud Deployment (Heroku)**

#### Prerequisites
- Heroku account
- Heroku CLI installed

#### Steps
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-wellness-assistant

# Deploy
git push heroku main

# Open your app
heroku open
```

### 🐳 **3. Docker Deployment**

#### Prerequisites
- Docker installed

#### Steps
```bash
# Build Docker image
docker build -t ai-wellness-assistant .

# Run container
docker run -p 5000:5000 ai-wellness-assistant

# Access at http://localhost:5000
```

### 🌟 **4. Vercel Deployment**

#### Prerequisites
- Vercel account
- Vercel CLI (optional)

#### Steps
1. Fork/Clone the repository
2. Connect to Vercel dashboard
3. Import project from GitHub
4. Deploy automatically

### 🔧 **5. Manual Server Deployment**

#### Prerequisites
- Linux server with Python 3.8+
- SSH access

#### Steps
```bash
# On your server
git clone https://github.com/Shubham07badgujar/Ai-agent.git
cd Ai-agent

# Install dependencies
pip install -r requirements.txt

# Install process manager
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_server:app

# Or use systemd service (recommended)
sudo systemctl enable wellness-assistant
sudo systemctl start wellness-assistant
```

## 🔧 **Environment Variables**

For production deployment, set these environment variables:

```bash
# Optional: For AI features
GEMINI_API_KEY=your_gemini_api_key_here

# Production settings
FLASK_ENV=production
SECRET_KEY=your_secret_key_here
```

## 📊 **Monitoring & Maintenance**

### Health Check Endpoint
- **URL**: `/health` (if implemented)
- **Status**: Returns 200 OK when healthy

### Logs
- **Location**: Check platform-specific log locations
- **Level**: INFO for production

### Backup
- **Data**: Backup `data/` directory regularly
- **Database**: Export wellness data periodically

## 🔒 **Security Considerations**

- Use HTTPS in production
- Set proper CORS origins
- Implement rate limiting
- Regular security updates
- Environment variable protection

## 📈 **Scaling**

### Single Instance
- Good for personal use
- Handles 100+ concurrent users

### Multiple Instances
- Use load balancer
- Shared database/storage
- Session management

## 🐛 **Troubleshooting**

### Common Issues
1. **Port conflicts**: Change port in `web_server.py`
2. **Dependencies**: Update pip and Python version
3. **Database**: Reset `data/wellness.db` if corrupted
4. **Permissions**: Check file system permissions

### Platform-Specific Issues
- **Heroku**: Check dyno status and logs
- **Docker**: Verify port mapping and volume mounts
- **Vercel**: Check build logs and function limits
