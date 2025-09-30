#!/usr/bin/env python3
"""
Test individual components without LLM
"""

import os
import sys
import pandas as pd

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_processing.ingest import load_csv
from data_processing.vector_store import VectorStore
from agents.option_finder import OptionFinderAgent

def test_data_processing():
    """Test data loading and vector store"""
    print("📊 Testing data processing...")
    
    # Create sample data
    data = {
        'description': [
            'Electric car with 300 mile range, fast charging, eco-friendly',
            'Hybrid car with good fuel economy, reliable, lower maintenance',
            'Gas car with powerful engine, affordable, widely available service'
        ],
        'price': [45000, 28000, 22000],
        'category': ['electric', 'hybrid', 'gas']
    }
    
    df = pd.DataFrame(data)
    df.to_csv('test_data.csv', index=False)
    
    try:
        # Test document loading
        docs = load_csv('test_data.csv')
        print(f"   ✅ Loaded {len(docs)} documents")
        
        # Test vector store
        vs = VectorStore()
        vs.add_documents(docs)
        print("   ✅ Vector store created")
        
        # Test similarity search
        results = vs.similarity_search("affordable car", k=2)
        print(f"   ✅ Found {len(results)} similar documents")
        
        # Test option finder agent
        option_finder = OptionFinderAgent(vs)
        state = {"query": "affordable transportation"}
        result_state = option_finder(state)
        print(f"   ✅ Option finder found {len(result_state['candidates'])} candidates")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    finally:
        if os.path.exists('test_data.csv'):
            os.remove('test_data.csv')

if __name__ == "__main__":
    print("🧪 Testing System Components")
    print("=" * 30)
    
    if test_data_processing():
        print("\n✅ Core components working correctly!")
        print("📝 The vector search and option finding are functional")
        print("🤖 LLM integration may need model name adjustment")
    else:
        print("\n❌ Component test failed")