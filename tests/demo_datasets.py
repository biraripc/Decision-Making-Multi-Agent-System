#!/usr/bin/env python3
"""
Demo script showing how to use the sample datasets with the multi-agent system
"""

import os
import sys

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_processing.ingest import load_csv
from data_processing.vector_store import VectorStore
from agents.option_finder import OptionFinderAgent
from agents.pros_cons import ProsConsAgent
from agents.decision import DecisionAgent
from workflow.orchestrator import build_workflow
from llm.gemini_wrapper import GeminiLLMWrapper
from config import GOOGLE_API_KEY

def demo_dataset(csv_file, query, dataset_name):
    """Demo a specific dataset with a query"""
    print(f"\n🎯 DEMO: {dataset_name}")
    print("=" * 50)
    print(f"📊 Dataset: {csv_file}")
    print(f"❓ Query: {query}")
    print()
    
    try:
        # Load and process data
        print("📖 Loading data...")
        docs = load_csv(csv_file)
        print(f"   Loaded {len(docs)} options")
        
        # Initialize system
        print("🔧 Initializing system...")
        vs = VectorStore()
        vs.add_documents(docs)
        llm = GeminiLLMWrapper(api_key=GOOGLE_API_KEY)
        
        # Create agents and workflow
        option_finder = OptionFinderAgent(vs)
        pros_cons = ProsConsAgent(llm)
        decision = DecisionAgent(llm)
        workflow = build_workflow(option_finder, pros_cons, decision)
        
        # Run analysis
        print("🤖 Running multi-agent analysis...")
        state = {"query": query}
        result = workflow.invoke(state)
        
        # Display results
        print(f"\n🎯 Found {len(result.get('candidates', []))} relevant options:")
        for i, candidate in enumerate(result.get('candidates', [])[:3]):  # Show top 3
            print(f"   {i+1}. {candidate.page_content[:80]}...")
        
        print(f"\n💡 AI Recommendation:")
        recommendation = result.get('recommendation', 'No recommendation generated')
        # Show first 300 characters of recommendation
        print(recommendation[:300] + "..." if len(recommendation) > 300 else recommendation)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run demos for all sample datasets"""
    print("🚀 Multi-Agent Decision System - Dataset Demos")
    print("=" * 60)
    
    # Check if API key is available
    if not GOOGLE_API_KEY:
        print("❌ Error: GOOGLE_API_KEY not found. Please check your .env file.")
        return
    
    demos = [
        {
            "file": "sample_datasets/laptops.csv",
            "query": "I need a laptop for programming and software development under $1500",
            "name": "Laptop Selection"
        },
        {
            "file": "sample_datasets/investment_options.csv", 
            "query": "I want to invest $5000 with moderate risk for long-term growth",
            "name": "Investment Planning"
        },
        {
            "file": "sample_datasets/vacation_destinations.csv",
            "query": "I want an adventurous vacation with beautiful nature under $1500",
            "name": "Vacation Planning"
        },
        {
            "file": "sample_datasets/career_paths.csv",
            "query": "I want a high-paying tech career with good work-life balance and remote work options",
            "name": "Career Planning"
        },
        {
            "file": "sample_datasets/housing_options.csv",
            "query": "I need affordable housing with short commute and good amenities",
            "name": "Housing Selection"
        }
    ]
    
    successful_demos = 0
    
    for demo in demos:
        if os.path.exists(demo["file"]):
            if demo_dataset(demo["file"], demo["query"], demo["name"]):
                successful_demos += 1
            print("\n" + "-" * 60)
        else:
            print(f"❌ Dataset not found: {demo['file']}")
    
    print(f"\n🎉 Completed {successful_demos}/{len(demos)} demos successfully!")
    print("\n📝 To use your own data:")
    print("   1. Create a CSV file with a 'description' column")
    print("   2. Add other relevant columns (price, category, etc.)")
    print("   3. Run: streamlit run ui/app.py")
    print("   4. Upload your CSV and ask questions!")

if __name__ == "__main__":
    main()