#!/bin/bash
# Production deployment script for AI Wellness Assistant

echo "🚀 AI Wellness Assistant - Production Deployment"
echo "================================================"

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "⚠️  Please don't run this script as root"
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8+ required. Found: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Create application directory
APP_DIR="/opt/wellness-assistant"
echo "📁 Creating application directory: $APP_DIR"

sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Clone or update repository
if [ -d "$APP_DIR/.git" ]; then
    echo "🔄 Updating existing installation"
    cd $APP_DIR
    git pull
else
    echo "📥 Cloning repository"
    git clone https://github.com/Shubham07badgujar/Ai-agent.git $APP_DIR
    cd $APP_DIR
fi

# Create virtual environment
echo "🐍 Setting up virtual environment"
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies"
pip install --upgrade pip
pip install -r requirements.txt

# Create data directories
echo "📊 Creating data directories"
mkdir -p data exports logs

# Set permissions
chmod 755 $APP_DIR
chmod 644 $APP_DIR/data
chmod 644 $APP_DIR/exports

# Create systemd service
echo "⚙️  Creating systemd service"
sudo tee /etc/systemd/system/wellness-assistant.service > /dev/null <<EOF
[Unit]
Description=AI Wellness Assistant
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
Environment=FLASK_ENV=production
ExecStart=$APP_DIR/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 web_server:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start service
echo "🔄 Starting service"
sudo systemctl daemon-reload
sudo systemctl enable wellness-assistant
sudo systemctl start wellness-assistant

# Check service status
echo "📊 Service status:"
sudo systemctl status wellness-assistant --no-pager -l

# Setup log rotation
echo "📝 Setting up log rotation"
sudo tee /etc/logrotate.d/wellness-assistant > /dev/null <<EOF
$APP_DIR/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    notifempty
    create 644 $USER $USER
}
EOF

# Create nginx configuration (optional)
if command -v nginx &> /dev/null; then
    echo "🌐 Creating nginx configuration"
    sudo tee /etc/nginx/sites-available/wellness-assistant > /dev/null <<EOF
server {
    listen 80;
    server_name your-domain.com;  # Change this to your domain
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location /static {
        alias $APP_DIR/frontend/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF
    
    echo "🔗 To enable nginx:"
    echo "  sudo ln -s /etc/nginx/sites-available/wellness-assistant /etc/nginx/sites-enabled/"
    echo "  sudo systemctl reload nginx"
fi

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Next steps:"
echo "  1. Update domain in nginx config (if using nginx)"
echo "  2. Set up SSL certificate (recommended: certbot)"
echo "  3. Configure firewall rules"
echo "  4. Set up monitoring and backups"
echo ""
echo "🔧 Management commands:"
echo "  Start:   sudo systemctl start wellness-assistant"
echo "  Stop:    sudo systemctl stop wellness-assistant"
echo "  Restart: sudo systemctl restart wellness-assistant"
echo "  Status:  sudo systemctl status wellness-assistant"
echo "  Logs:    journalctl -u wellness-assistant -f"
echo ""
echo "🌐 Your AI Wellness Assistant should now be running on http://localhost:5000"
