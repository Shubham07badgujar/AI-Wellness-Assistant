#!/usr/bin/env python3
"""
Production deployment script for AI Wellness Assistant
Supports multiple cloud platforms and deployment methods
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class ProductionDeployer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.platform = platform.system().lower()
        
    def check_requirements(self):
        """Check if all requirements are met"""
        print("🔍 Checking deployment requirements...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
            print("❌ Python 3.8+ required")
            return False
            
        # Check if git is available
        try:
            subprocess.run(['git', '--version'], check=True, capture_output=True)
            print("✅ Git is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Git is required but not found")
            return False
            
        # Check if requirements.txt exists
        if not (self.project_root / 'requirements.txt').exists():
            print("❌ requirements.txt not found")
            return False
            
        print("✅ All requirements met")
        return True
        
    def install_heroku_cli(self):
        """Install Heroku CLI"""
        print("📦 Installing Heroku CLI...")
        
        if self.platform == 'windows':
            print("Please install Heroku CLI manually:")
            print("1. Visit: https://devcenter.heroku.com/articles/heroku-cli")
            print("2. Download and install Heroku CLI for Windows")
            print("3. Restart your terminal and run this script again")
        elif self.platform == 'darwin':  # macOS
            try:
                subprocess.run(['brew', 'install', 'heroku/brew/heroku'], check=True)
                print("✅ Heroku CLI installed via Homebrew")
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("Please install Heroku CLI manually:")
                print("brew install heroku/brew/heroku")
        else:  # Linux
            try:
                subprocess.run(['curl', 'https://cli-assets.heroku.com/install.sh', '|', 'sh'], 
                             shell=True, check=True)
                print("✅ Heroku CLI installed")
            except subprocess.CalledProcessError:
                print("Please install Heroku CLI manually:")
                print("curl https://cli-assets.heroku.com/install.sh | sh")
                
    def deploy_to_heroku(self, app_name=None):
        """Deploy to Heroku"""
        print("🚀 Deploying to Heroku...")
        
        try:
            # Check if heroku is available
            subprocess.run(['heroku', '--version'], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Heroku CLI not found. Installing...")
            self.install_heroku_cli()
            return False
            
        try:
            # Login to Heroku
            print("🔑 Please login to Heroku...")
            subprocess.run(['heroku', 'auth:login'], check=True)
            
            # Create app if app_name provided
            if app_name:
                print(f"📱 Creating Heroku app: {app_name}")
                try:
                    subprocess.run(['heroku', 'create', app_name], check=True)
                except subprocess.CalledProcessError:
                    print(f"⚠️  App {app_name} might already exist or name unavailable")
            else:
                print("📱 Creating Heroku app with auto-generated name...")
                subprocess.run(['heroku', 'create'], check=True)
            
            # Deploy
            print("🚀 Deploying to Heroku...")
            subprocess.run(['git', 'push', 'heroku', 'main'], check=True)
            
            # Open app
            print("🌐 Opening deployed app...")
            subprocess.run(['heroku', 'open'], check=True)
            
            print("✅ Successfully deployed to Heroku!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Heroku deployment failed: {e}")
            return False
            
    def deploy_to_railway(self):
        """Deploy to Railway"""
        print("🚂 Deploying to Railway...")
        print("📋 Manual Railway deployment:")
        print("1. Visit: https://railway.app")
        print("2. Sign up/Login with GitHub")
        print("3. Click 'New Project' → 'Deploy from GitHub repo'")
        print("4. Select your repository: Shubham07badgujar/Ai-agent")
        print("5. Railway will auto-detect and deploy your Flask app")
        print("6. Set environment variables if needed")
        
    def deploy_to_render(self):
        """Deploy to Render"""
        print("🎨 Deploying to Render...")
        print("📋 Manual Render deployment:")
        print("1. Visit: https://render.com")
        print("2. Sign up/Login with GitHub")
        print("3. Click 'New' → 'Web Service'")
        print("4. Connect your GitHub repository: Shubham07badgujar/Ai-agent")
        print("5. Use these settings:")
        print("   - Build Command: pip install -r requirements.txt")
        print("   - Start Command: gunicorn web_server:app")
        print("   - Environment: Python 3")
        
    def deploy_to_vercel(self):
        """Deploy to Vercel"""
        print("▲ Deploying to Vercel...")
        
        # Create vercel.json for Python deployment
        vercel_config = {
            "version": 2,
            "builds": [
                {
                    "src": "web_server.py",
                    "use": "@vercel/python"
                }
            ],
            "routes": [
                {
                    "src": "/(.*)",
                    "dest": "web_server.py"
                }
            ]
        }
        
        import json
        with open(self.project_root / 'vercel.json', 'w') as f:
            json.dump(vercel_config, f, indent=2)
            
        print("✅ Created vercel.json configuration")
        print("📋 Manual Vercel deployment:")
        print("1. Visit: https://vercel.com")
        print("2. Sign up/Login with GitHub")
        print("3. Click 'New Project'")
        print("4. Import your GitHub repository: Shubham07badgujar/Ai-agent")
        print("5. Vercel will auto-deploy your app")
        
    def create_docker_production(self):
        """Create production Docker setup"""
        print("🐳 Setting up production Docker configuration...")
        
        # Create production docker-compose
        docker_prod_config = '''version: '3.8'

services:
  wellness-assistant:
    build: .
    ports:
      - "80:5000"
    volumes:
      - wellness_data:/app/data
      - wellness_exports:/app/exports
    environment:
      - FLASK_ENV=production
      - PYTHONPATH=/app
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx.prod.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - wellness-assistant
    restart: always

volumes:
  wellness_data:
  wellness_exports:
'''
        
        with open(self.project_root / 'docker-compose.prod.yml', 'w') as f:
            f.write(docker_prod_config)
            
        # Create nginx production config
        nginx_config = '''events {
    worker_connections 1024;
}

http {
    upstream wellness_app {
        server wellness-assistant:5000;
    }

    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        location / {
            proxy_pass http://wellness_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /static {
            alias /app/frontend/static;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
'''
        
        with open(self.project_root / 'nginx.prod.conf', 'w') as f:
            f.write(nginx_config)
            
        print("✅ Created production Docker configuration")
        print("📋 To deploy with Docker:")
        print("docker-compose -f docker-compose.prod.yml up -d")
        
    def show_deployment_options(self):
        """Show all deployment options"""
        print("\n🚀 Production Deployment Options")
        print("=" * 50)
        print("1. 🟢 Heroku (Free tier available, easy setup)")
        print("2. 🚂 Railway (Modern, GitHub integration)")
        print("3. 🎨 Render (Free tier, auto-deploy)")
        print("4. ▲ Vercel (Serverless, fast)")
        print("5. 🐳 Docker Production (Your own server)")
        print("6. 📋 Show all options")
        print("7. 🚪 Exit")
        
    def run(self):
        """Main deployment runner"""
        print("🌟 AI Wellness Assistant - Production Deployment")
        print("=" * 55)
        
        if not self.check_requirements():
            print("❌ Requirements not met. Please fix the issues above.")
            return
            
        while True:
            self.show_deployment_options()
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                app_name = input("Enter Heroku app name (or press Enter for auto-generated): ").strip()
                app_name = app_name if app_name else None
                self.deploy_to_heroku(app_name)
            elif choice == '2':
                self.deploy_to_railway()
            elif choice == '3':
                self.deploy_to_render()
            elif choice == '4':
                self.deploy_to_vercel()
            elif choice == '5':
                self.create_docker_production()
            elif choice == '6':
                print("\n📋 All Deployment Options:")
                print("- Heroku: Easy, free tier, good for beginners")
                print("- Railway: Modern, automatic deployments")
                print("- Render: Free tier, simple setup")
                print("- Vercel: Serverless, very fast")
                print("- Docker: Full control, your own server")
            elif choice == '7':
                break
            else:
                print("❌ Invalid choice. Please select 1-7.")
                
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    deployer = ProductionDeployer()
    deployer.run()
