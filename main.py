"""Main entry point for the multi-agent decision system."""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from config.settings import settings
from config.logging import setup_logging


def main():
    """Main application entry point."""
    # Set up logging
    setup_logging(level="INFO")
    
    # Create necessary directories
    os.makedirs(settings.faiss_index_path, exist_ok=True)
    os.makedirs("data/uploads", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    print("Multi-Agent Decision System")
    print("=" * 30)
    print(f"FAISS Index Path: {settings.faiss_index_path}")
    print(f"Embedding Model: {settings.embedding_model}")
    print(f"Search Top-K: {settings.search_top_k}")
    print("\nTo start the Streamlit UI, run:")
    print("streamlit run ui/app.py")


if __name__ == "__main__":
    main()