# Multi-Agent Decision-Making System

A modular decision support system that uses three specialized AI agents to help users make informed choices from their data. Built with LangChain, LangGraph, and open-source ML tools.

## Features

- **Option Finder Agent**: Semantic search through uploaded data using vector embeddings
- **Pros/Cons Agent**: LLM-powered analysis of options with structured summaries  
- **Decision Agent**: Multi-criteria evaluation and ranked recommendations
- **Free & Open Source**: Uses only free LLM APIs and open-source tools
- **Multiple Interfaces**: Streamlit web app and CLI support

## Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your API keys
# At least one LLM provider key is required:
# - Google AI Studio (Gemini) - Free tier available
# - Groq (Llama 3.3) - Free tier available  
# - Hugging Face - Free tier available
```

### 3. Run the Application

**Web Interface:**
```bash
streamlit run multi_agent_decision_system/interfaces/streamlit_app.py
```

**CLI Interface:**
```bash
python -m multi_agent_decision_system.interfaces.cli --help
```

## Project Structure

```
multi_agent_decision_system/
├── agents/              # Specialized AI agents
├── data_processing/     # File parsing and embeddings
├── workflow/           # LangGraph orchestration
├── interfaces/         # Web and CLI interfaces
├── config/            # Settings and API key management
└── utils/             # Common utilities and data models
```

## Supported File Types

- **CSV**: Structured data with headers
- **JSON**: Nested data structures
- **TXT**: Plain text documents

## Requirements

- Python 3.9+
- At least one LLM API key (Google AI Studio, Groq, or Hugging Face)
- 4GB+ RAM for vector embeddings
- Internet connection for LLM APIs

## Development

```bash
# Install in development mode
pip install -e .

# Run tests
pytest

# Format code
black multi_agent_decision_system/

# Lint code
flake8 multi_agent_decision_system/
```

## License

MIT License - see LICENSE file for details.