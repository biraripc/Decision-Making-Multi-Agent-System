#!/usr/bin/env python3
"""
Test script for the multi-agent decision making system
"""

import os
import sys
import pandas as pd

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

def create_sample_data():
    """Create a sample CSV file for testing"""
    data = {
        'description': [
            'Electric car with 300 mile range, fast charging, eco-friendly',
            'Hybrid car with good fuel economy, reliable, lower maintenance',
            'Gas car with powerful engine, affordable, widely available service',
            'Motorcycle with excellent fuel economy, easy parking, fun to ride',
            'Public transportation pass, very affordable, no maintenance needed'
        ],
        'price': [45000, 28000, 22000, 8000, 1200],
        'category': ['electric', 'hybrid', 'gas', 'motorcycle', 'public_transport']
    }
    
    df = pd.DataFrame(data)
    df.to_csv('sample_transportation.csv', index=False)
    return 'sample_transportation.csv'

def test_system():
    """Test the complete multi-agent system"""
    print("🚀 Testing Multi-Agent Decision System")
    
    # Check if API key is available
    if not GOOGLE_API_KEY:
        print("❌ Error: GOOGLE_API_KEY not found in environment")
        return False
    
    try:
        # Create sample data
        print("📊 Creating sample data...")
        csv_file = create_sample_data()
        
        # Load documents
        print("📖 Loading documents...")
        docs = load_csv(csv_file)
        print(f"   Loaded {len(docs)} documents")
        
        # Initialize vector store
        print("🔍 Initializing vector store...")
        vs = VectorStore()
        vs.add_documents(docs)
        print("   Vector store ready")
        
        # Initialize LLM
        print("🤖 Initializing LLM...")
        llm = GeminiLLMWrapper(api_key=GOOGLE_API_KEY)
        print("   LLM ready")
        
        # Initialize agents
        print("👥 Initializing agents...")
        option_finder = OptionFinderAgent(vs)
        pros_cons = ProsConsAgent(llm)
        decision = DecisionAgent(llm)
        print("   Agents ready")
        
        # Build workflow
        print("⚙️ Building workflow...")
        workflow = build_workflow(option_finder, pros_cons, decision)
        print("   Workflow ready")
        
        # Test query
        query = "I need affordable transportation for daily commuting"
        print(f"❓ Query: {query}")
        
        # Run workflow
        print("🔄 Running workflow...")
        state = {"query": query}
        result = workflow.invoke(state)
        
        # Display results
        print("\n" + "="*50)
        print("📋 RESULTS")
        print("="*50)
        
        print(f"\n🎯 Found {len(result.get('candidates', []))} options:")
        for i, candidate in enumerate(result.get('candidates', [])):
            print(f"   {i+1}. {candidate.page_content}")
        
        print(f"\n📊 Generated {len(result.get('analyses', []))} analyses")
        
        print(f"\n💡 Final Recommendation:")
        print(result.get('recommendation', 'No recommendation generated'))
        
        print("\n✅ Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Clean up
        if os.path.exists('sample_transportation.csv'):
            os.remove('sample_transportation.csv')

if __name__ == "__main__":
    test_system()