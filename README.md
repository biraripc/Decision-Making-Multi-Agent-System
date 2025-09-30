# Multi-Agent Decision Making System

A sophisticated AI-powered decision-making system that uses multiple specialized agents to analyze options, evaluate pros and cons, and provide intelligent recommendations based on your data.

![System Status](https://img.shields.io/badge/Status-Fully%20Functional-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-orange)
![Framework](https://img.shields.io/badge/Framework-LangChain%20%7C%20Streamlit-red)

## 🎯 What It Does

Transform complex decisions into clear, AI-powered recommendations:
- **Upload your options** as a CSV file
- **Ask natural language questions** about what you're looking for
- **Get intelligent analysis** with pros, cons, and detailed reasoning
- **Make confident decisions** backed by AI insights

## 🏗️ Architecture

The system uses a multi-agent approach with specialized AI components:

```
📊 Data Input → 🔍 Option Finder → 📋 Pros/Cons Analyzer → 🎯 Decision Agent → 💡 Recommendation
```

### Core Components:
- **🔍 Option Finder Agent**: Uses vector similarity search to find relevant options
- **📋 Pros & Cons Agent**: Analyzes advantages and disadvantages of each option
- **🎯 Decision Agent**: Synthesizes all analyses into a final recommendation
- **⚙️ LangGraph Orchestrator**: Manages the workflow between agents
- **🌐 Streamlit Interface**: User-friendly web application

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google AI API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd decision-making-multi-agent-system
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API key**:
   ```bash
   # Edit .env file
   GOOGLE_API_KEY=your_google_ai_api_key_here
   ```

4. **Run the application**:
   ```bash
   # Option 1: Use the launcher script
   python run_app.py
   
   # Option 2: Direct Streamlit
   streamlit run ui/app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 📊 Sample Datasets & Demos

We've included 6 comprehensive sample datasets to get you started:

| Dataset | Use Case | Sample Query |
|---------|----------|--------------|
| 💻 **Laptops** | Technology purchases | "Best laptop for programming under $1500" |
| 💰 **Investments** | Financial planning | "Moderate risk investment for retirement" |
| 🏖️ **Vacations** | Travel planning | "Adventurous vacation with nature under $1500" |
| 💼 **Careers** | Professional development | "High-paying tech job with remote options" |
| 🏠 **Housing** | Real estate decisions | "Affordable housing with short commute" |
| 💪 **Fitness** | Health & wellness | "Effective home workout program" |

### Try the Demos:
```bash
# Run all tests and demos
python tests/run_tests.py

# Or run individual tests
python tests/test_components.py    # Component tests (no API key needed)
python tests/test_system.py       # Full system test
python tests/demo_datasets.py     # Dataset demonstrations
```

## 💡 Usage Examples

### 1. **Technology Purchase Decision**
```
Upload: laptops.csv
Query: "I need a laptop for video editing and gaming under $2000"
Result: Detailed analysis of gaming laptops with pros/cons and recommendation
```

### 2. **Investment Planning**
```
Upload: investment_options.csv  
Query: "Safe investment options for my emergency fund"
Result: Comparison of low-risk investments with expected returns
```

### 3. **Career Planning**
```
Upload: career_paths.csv
Query: "High-growth career with good work-life balance"
Result: Analysis of career options with salary, growth, and lifestyle factors
```

## 📁 Project Structure

```
📦 Multi-Agent Decision System
├── 🤖 agents/                    # AI Agent implementations
│   ├── option_finder.py          # Vector similarity search agent
│   ├── pros_cons.py              # Analysis agent
│   └── decision.py               # Final decision agent
├── 📊 data_processing/           # Data handling pipeline
│   ├── document.py               # Document data structure
│   ├── vector_store.py           # FAISS vector database
│   └── ingest.py                 # CSV data loader
├── 🧠 llm/                      # LLM integration
│   └── gemini_wrapper.py         # Google Gemini AI wrapper
├── ⚙️ workflow/                 # Orchestration
│   └── orchestrator.py           # LangGraph workflow manager
├── 🌐 ui/                       # User interface
│   └── app.py                    # Streamlit web application
├── 📋 sample_datasets/           # Example datasets
│   ├── laptops.csv               # Technology options
│   ├── investment_options.csv    # Financial instruments
│   ├── vacation_destinations.csv # Travel destinations
│   ├── career_paths.csv          # Professional opportunities
│   ├── housing_options.csv       # Real estate choices
│   ├── fitness_programs.csv      # Health & fitness options
│   └── README.md                 # Dataset documentation
├── 🧪 tests/                     # Test suite
│   ├── test_system.py            # Full system integration test
│   ├── test_components.py        # Individual component tests
│   ├── demo_datasets.py          # Dataset demonstrations
│   ├── run_tests.py              # Test runner
│   └── README.md                 # Test documentation
├── 🚀 run_app.py                 # Application launcher
├── ⚙️ Configuration
│   ├── config.py                 # Configuration management
│   ├── .env                      # Environment variables (API keys)
│   ├── requirements.txt          # Python dependencies
│   └── .gitignore               # Git ignore rules
└── 📖 README.md                 # This file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:
```bash
GOOGLE_API_KEY=your_google_ai_api_key_here
```

### Model Configuration
The system uses **Gemini 2.5 Flash** by default. Available models:
- `gemini-2.5-flash` (latest, fastest)
- `gemini-1.5-pro` (more capable, higher cost)
- `gemini-1.5-flash` (balanced performance)

Change in `llm/gemini_wrapper.py`:
```python
def __init__(self, api_key, model="gemini-2.5-flash"):
```

## 📝 Data Format Guidelines

### Required Column
- **`description`**: Detailed text about each option (required)

### Optional Columns (enhance analysis)
- **`price`/`cost`**: Numerical values for cost comparison
- **`category`**: Grouping similar options  
- **`rating`**: Quality scores
- **`location`**: Geographic information
- **Custom fields**: Any domain-specific attributes

### Example CSV Format:
```csv
description,price,category,rating
"MacBook Air M2 with 8GB RAM, excellent battery life, perfect for students and professionals",1199,ultrabook,4.8
"Gaming laptop with RTX 4060, high refresh display, powerful performance for gaming and content creation",1599,gaming,4.5
"Budget laptop with solid performance, good for everyday tasks, affordable option for students",549,budget,4.0
```

## 🧪 Testing & Validation

### System Health Check:
```bash
# Run all tests
python tests/run_tests.py

# Individual tests
python tests/test_components.py    # Component tests (no API key needed)
python tests/test_system.py       # Full system test
python tests/demo_datasets.py     # Dataset demonstrations
```

### Expected Output:
```
✅ Configuration: API key loaded
✅ Data Processing: Vector store functional  
✅ LLM Integration: Gemini model responding
✅ Multi-Agent Workflow: All agents operational
✅ Web Interface: Streamlit app ready
```

## 🔍 How It Works

### 1. **Data Ingestion**
- CSV files are parsed and converted to document objects
- Each row becomes a searchable option with metadata

### 2. **Vector Embedding**
- Documents are embedded using Sentence Transformers
- Stored in FAISS vector database for similarity search

### 3. **Query Processing**
- User query is embedded and compared to stored options
- Most relevant options are retrieved using cosine similarity

### 4. **Multi-Agent Analysis**
- **Option Finder**: Retrieves top matching options
- **Pros & Cons Agent**: Analyzes each option's strengths/weaknesses  
- **Decision Agent**: Synthesizes analyses into final recommendation

### 5. **Result Presentation**
- Structured output with found options, analyses, and recommendation
- Displayed in user-friendly Streamlit interface

## 🛠️ Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| ❌ API Key Error | Verify `GOOGLE_API_KEY` in `.env` file |
| ❌ Model Not Found | Use correct model name: `gemini-2.5-flash` |
| ❌ Import Errors | Run `pip install -r requirements.txt` |
| ❌ Memory Issues | Reduce dataset size or use smaller embedding model |
| ❌ Slow Performance | Use `gemini-2.5-flash` for faster responses |

### Dependency Installation:
```bash
# Core packages
pip install langchain langchain-community langchain-huggingface
pip install langgraph faiss-cpu sentence-transformers  
pip install streamlit langchain-google-genai pandas numpy python-dotenv

# If issues persist, try individual installation
pip install --upgrade langchain-google-genai
```

## 🎯 Use Cases

### Business Applications
- **Product Selection**: Compare software tools, equipment, vendors
- **Investment Analysis**: Evaluate financial instruments and strategies
- **Hiring Decisions**: Analyze candidate profiles and qualifications
- **Market Research**: Compare competitors and market opportunities

### Personal Decisions  
- **Major Purchases**: Cars, homes, electronics, appliances
- **Life Choices**: Career paths, education options, lifestyle changes
- **Travel Planning**: Destinations, accommodations, activities
- **Health & Fitness**: Exercise programs, diet plans, wellness options

### Research & Analysis
- **Academic Research**: Compare methodologies, tools, approaches
- **Policy Analysis**: Evaluate policy options and their implications
- **Technology Assessment**: Compare frameworks, platforms, solutions

## 🚀 Advanced Features

### Customization Options
- **Custom Agents**: Add domain-specific analysis agents
- **Multiple LLMs**: Support for different AI models
- **Advanced Queries**: Complex multi-criteria decision making
- **Export Results**: Save analyses and recommendations

### Integration Possibilities
- **API Endpoints**: RESTful API for programmatic access
- **Database Integration**: Connect to existing data sources
- **Workflow Automation**: Integrate with business processes
- **Custom UI**: Build domain-specific interfaces

## 🤝 Contributing

We welcome contributions! Areas for improvement:
- Additional sample datasets
- New agent types for specialized analysis
- UI/UX enhancements
- Performance optimizations
- Integration with other AI models

### Development Setup:
```bash
git clone <repository-url>
cd decision-making-multi-agent-system
pip install -r requirements.txt
# Make your changes
python test_system.py  # Verify functionality
```

## 📊 Performance Metrics

- **Response Time**: ~10-30 seconds for full analysis
- **Accuracy**: High-quality recommendations based on comprehensive analysis
- **Scalability**: Handles datasets up to 1000+ options
- **Cost**: Efficient use of API calls with Gemini Flash model

## 🔮 Future Roadmap

- [ ] Support for additional LLM providers (OpenAI, Anthropic)
- [ ] Advanced visualization of decision factors
- [ ] Multi-language support
- [ ] Mobile-responsive interface
- [ ] Batch processing for multiple decisions
- [ ] Integration with popular data sources (Google Sheets, Airtable)

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

Built with:
- [LangChain](https://langchain.com/) - AI application framework
- [Google Gemini](https://ai.google.dev/) - Large language model
- [Streamlit](https://streamlit.io/) - Web application framework
- [FAISS](https://faiss.ai/) - Vector similarity search
- [Sentence Transformers](https://www.sbert.net/) - Text embeddings

---

**Ready to make better decisions with AI?** 🚀

Start by running `python demo_datasets.py` to see the system in action, then upload your own data and start making smarter choices!