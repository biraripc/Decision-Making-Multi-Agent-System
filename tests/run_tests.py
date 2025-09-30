#!/usr/bin/env python3
"""
Test runner for Multi-Agent Decision System
"""

import os
import sys
import subprocess

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_test(test_name, test_file):
    """Run a specific test"""
    print(f"\n🧪 Running {test_name}...")
    print("-" * 40)
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=False, 
                              text=True, 
                              cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running {test_name}: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Multi-Agent Decision System - Test Suite")
    print("=" * 50)
    
    # Change to tests directory
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(tests_dir)
    
    tests = [
        ("Component Tests", "test_components.py"),
        ("System Integration Test", "test_system.py"),
        ("Dataset Demos", "demo_datasets.py")
    ]
    
    results = []
    
    for test_name, test_file in tests:
        success = run_test(test_name, test_file)
        results.append((test_name, success))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Tests Passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("🎉 All tests passed! System is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check the output above.")
    
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)