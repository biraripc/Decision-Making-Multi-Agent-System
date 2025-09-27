# Multi-Agent Decision System

A sophisticated decision-making system that leverages multiple AI agents to analyze data, evaluate options, and provide ranked recommendations using LangChain, LangGraph, FAISS, and Google Gemini.

## Project Structure

```
multi-agent-decision-system/
├── agents/                 # Agent implementations
├── data_processing/        # Data processing utilities
├── ui/                    # Streamlit UI components
├── config/                # Configuration management
├── tests/                 # Test suite
├── data/                  # Data storage (created at runtime)
│   ├── uploads/          # Uploaded files
│   └── faiss_index/      # FAISS vector indices
├── logs/                  # Application logs (created at runtime)
├── main.py               # Main application entry point
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
└── README.md            # This file
```

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your Google API key
   ```

3. **Initialize Application**
   ```bash
   python main.py
   ```

4. **Start UI**
   ```bash
   streamlit run ui/app.py
   ```

## Configuration

The system uses environment variables for configuration. See `.env.example` for all available options.

Required:
- `GOOGLE_API_KEY`: Your Google AI Studio API key

## Architecture

The system consists of three main agents orchestrated through LangGraph:

1. **Option Finder Agent**: Performs semantic search to find relevant options
2. **Pros/Cons Agent**: Analyzes advantages and disadvantages of each option
3. **Decision Agent**: Ranks options and provides final recommendations

## Development

Run tests:
```bash
pytest
```

Code formatting:
```bash
black .
```

Type checking:
```bash
mypy .
```