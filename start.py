#!/usr/bin/env python3
"""
Startup script for AI Wellness Assistant
Allows choosing between CLI and Web interfaces
"""

import sys
import subprocess
from pathlib import Path

def show_menu():
    """Display the startup menu"""
    print("🌟 AI Wellness Assistant")
    print("=" * 40)
    print("Choose how to run the application:")
    print()
    print("1. 📱 Web Interface (recommended)")
    print("   - Beautiful web dashboard")
    print("   - Easy habit tracking")
    print("   - Visual charts and summaries")
    print()
    print("2. 💻 Command Line Interface")
    print("   - Terminal-based commands")
    print("   - Quick tracking and queries")
    print("   - Advanced features")
    print()
    print("3. 🛠️ Show CLI help")
    print("4. 🚪 Exit")
    print()

def main():
    """Main startup function"""
    
    # Ensure we're in the right directory
    script_dir = Path(__file__).parent
    
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == "1":
                print("\n🚀 Starting web interface...")
                print("📱 Open http://localhost:5000 in your browser")
                print("🛑 Press Ctrl+C to stop the server")
                print()
                
                # Run the web server
                subprocess.run([
                    sys.executable, "web_server.py"
                ], cwd=script_dir)
                
            elif choice == "2":
                print("\n💻 Starting CLI interface...")
                print("ℹ️  Use 'python main.py --help' for command reference")
                print()
                
                # Show quick commands
                print("Quick commands:")
                print("  python main.py quick          # Interactive tracking")
                print("  python main.py summary        # View summary")
                print("  python main.py track sleep 8 hours")
                print("  python main.py ask 'wellness question'")
                print()
                
                # Start interactive CLI
                subprocess.run([
                    sys.executable, "main.py", "quick"
                ], cwd=script_dir)
                
            elif choice == "3":
                print("\n📖 CLI Help:")
                subprocess.run([
                    sys.executable, "main.py", "--help"
                ], cwd=script_dir)
                print()
                input("Press Enter to continue...")
                
            elif choice == "4":
                print("\n👋 Goodbye! Stay healthy!")
                break
                
            else:
                print("\n❌ Invalid choice. Please enter 1, 2, 3, or 4.")
                input("Press Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Stay healthy!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
