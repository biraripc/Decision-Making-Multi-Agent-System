#!/usr/bin/env python3
"""
Simple script to run the Streamlit app
"""

import subprocess
import sys

if __name__ == "__main__":
    print("🚀 Starting Multi-Agent Decision System")
    print("📱 Opening Streamlit app...")
    print("🌐 The app will open in your browser at http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the app")
    print()
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "ui/app.py"])
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error running app: {e}")