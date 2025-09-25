#!/usr/bin/env python3
"""
Verification script for Multi-Agent Decision System setup.

This script verifies that the project structure, dependencies, and configuration
are set up correctly. Run this after installation to ensure everything is working.

Usage:
    python verify_setup.py

Exit codes:
    0: All checks passed
    1: One or more checks failed
"""

import sys
import os
from pathlib import Path

def check_project_structure():
    """Verify project directory structure."""
    print("🔍 Checking project structure...")
    
    required_dirs = [
        "multi_agent_decision_system",
        "multi_agent_decision_system/agents",
        "multi_agent_decision_system/data_processing", 
        "multi_agent_decision_system/workflow",
        "multi_agent_decision_system/interfaces",
        "multi_agent_decision_system/config",
        "multi_agent_decision_system/utils",
        "data",
        "tests"
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not Path(dir_path).exists():
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"❌ Missing directories: {missing_dirs}")
        return False
    
    print("✅ Project structure is correct")
    return True

def check_required_files():
    """Verify required files exist."""
    print("🔍 Checking required files...")
    
    required_files = [
        "requirements.txt",
        "setup.py", 
        "README.md",
        ".env.example",
        "multi_agent_decision_system/__init__.py",
        "multi_agent_decision_system/config/settings.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def check_configuration():
    """Test configuration system."""
    print("🔍 Testing configuration system...")
    
    try:
        sys.path.insert(0, '.')
        from multi_agent_decision_system.config.settings import settings, security_config
        
        # Test basic settings
        assert settings.vector_db_path
        assert settings.embedding_model
        assert settings.max_file_size_mb > 0
        assert len(settings.supported_file_types) > 0
        
        # Test security config
        api_status = security_config.validate_api_keys(settings)
        providers = security_config.get_available_llm_providers(settings)
        
        assert isinstance(api_status, dict)
        assert isinstance(providers, list)
        assert "local_transformers" in providers  # Always available as fallback
        
        print("✅ Configuration system working")
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def check_env_file():
    """Check if .env file exists and provide guidance."""
    print("🔍 Checking environment configuration...")
    
    if Path(".env").exists():
        print("✅ .env file found")
        print("💡 Make sure to add your API keys to the .env file")
    else:
        print("⚠️  .env file not found")
        print("💡 Copy .env.example to .env and add your API keys")
        print("   At least one LLM provider API key is required:")
        print("   - Google AI Studio (Gemini)")
        print("   - Groq (Llama 3.3)")  
        print("   - Hugging Face")
    
    return True

def main():
    """Run all verification checks."""
    print("🚀 Multi-Agent Decision System Setup Verification")
    print("=" * 50)
    
    checks = [
        check_project_structure,
        check_required_files,
        check_configuration,
        check_env_file
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
        print()
    
    if all_passed:
        print("🎉 Setup verification completed successfully!")
        print("\nNext steps:")
        print("1. Create/edit .env file with your API keys")
        print("2. Create virtual environment: python -m venv venv")
        print("3. Activate virtual environment:")
        print("   Windows: venv\\Scripts\\activate")
        print("   macOS/Linux: source venv/bin/activate")
        print("4. Install dependencies: pip install -r requirements.txt")
        print("5. Run the application!")
    else:
        print("❌ Setup verification failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()