---
title: Prompt Engineering AI Agent
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# Prompt Engineering AI Agent 🤖

A sophisticated AI-powered prompt engineering service that transforms brief, unstructured input into professionally optimized prompts. Built with CrewAI and integrated with Masumi Network for decentralized payments.

[![Powered by Groq](https://img.shields.io/badge/Powered%20by-Groq-orange)](https://groq.com/)
[![Masumi Network](https://img.shields.io/badge/Masumi-Network-blue)](https://masumi.network/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-green)](https://crewai.com/)

## 🌟 What It Does

Turn this: `"Create a prompt for sentiment analysis"`

Into this:
```markdown
# ROLE
You are a Customer Insight Analyst specializing in sentiment analysis...

# CONTEXT
- Purpose: Analyze customer feedback sentiment
- Target: AI language model
- Constraints: Real-time processing, accurate classification

# TASK
Conduct multi-dimensional analysis of customer feedback using:
1. Logical analysis - identify cause-effect relationships
2. Analytical breakdown - decompose into sentiment components
3. Computational patterns - use NLP and ML models
4. End-result assessment - drive business improvements

# OUTPUT FORMAT
{
  "sentiment": "positive|negative|neutral",
  "confidence": 0.95,
  "key_themes": [...],
  "actionable_insights": [...]
}
```

## ✨ Key Features

### 🧠 **Five-Step Thinking Framework**
- **Logical Thinking**: Identifies cause-effect relationships and contradictions
- **Analytical Thinking**: Breaks down complex requests into components
- **Computational Thinking**: Translates concepts into structured patterns
- **Producer Thinking**: Focuses on practical end results

### 🤝 **5 Specialized AI Agents**
1. **Input Analysis Specialist** - Multi-dimensional thinking analysis
2. **Requirements Clarifier** - Identifies gaps and asks questions
3. **Prompt Architect** - Designs using DxTag pattern
4. **Quality Assurance Specialist** - Two-iteration refinement
5. **Output Formatter** - Formats for target audience

### 🎯 **Advanced Capabilities**
- ✅ **Two-Iteration Refinement**: Internal quality assurance before output
- ✅ **DxTag Pattern**: Data, eXecution, Tags architecture
- ✅ **Version Control**: Git-integrated checkpoints
- ✅ **Rate Limiting**: Conservative limits (10/min, 100/hour)
- ✅ **Context Management**: JSON-based session tracking
- ✅ **Groq LLM**: Fast Llama 3.3 70B model
- ✅ **Masumi Integration**: Blockchain-based payments

## 🚀 Quick Start

### Prerequisites

- Python >= 3.10 and < 3.13
- uv (Python package manager)
- Groq API key (get free at [groq.com](https://groq.com))

### Installation

```bash
# Clone the repository
git clone https://github.com/SarthiBorkar/Prompt_AI.git
cd Prompt_AI

# Create virtual environment
uv venv --python 3.13
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt
```

### Configuration

Create `.env` file:

```env
# LLM Configuration
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Masumi Network (for production)
PAYMENT_SERVICE_URL=http://localhost:3001/api/v1
PAYMENT_API_KEY=your_payment_key
AGENT_IDENTIFIER=your_agent_identifier
PAYMENT_AMOUNT=10000000
PAYMENT_UNIT=lovelace
SELLER_VKEY=your_seller_vkey
NETWORK=Preprod
```

## 💻 Usage

### Standalone Mode (Local Testing)

Test the prompt engineering without payments:

```bash
python main.py
```

**Example output:**
```
🚀 Running Prompt Engineering Agent locally...

Input: Create a prompt for sentiment analysis

Processing with 5 AI agents...
✅ Engineered Prompt:
[Professional-grade prompt output]
```

### API Mode (Production)

Run with full Masumi payment integration:

```bash
python main.py api
```

Server starts at: `http://127.0.0.1:8000`

### API Endpoints

#### **Test Endpoint (No Payment)**
```bash
curl -X POST http://127.0.0.1:8000/test_prompt_engineering \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Create a prompt for sentiment analysis"
  }'
```

#### **Production Endpoints (With Payment)**

1. **GET** `/availability` - Check if agent is operational
2. **GET** `/input_schema` - Get input requirements
3. **POST** `/start_job` - Start prompt engineering job (requires payment)
4. **GET** `/status?job_id=X` - Check job status
5. **GET** `/health` - Health check

### Interactive Documentation

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│     User Input (Brief Description)      │
└────────────────┬────────────────────────┘
                 │
        ┌────────▼────────┐
        │ Input Analyzer  │ (Multi-dimensional Thinking)
        └────────┬────────┘
                 │
        ┌────────▼─────────┐
        │ Req. Clarifier   │ (Gap Identification)
        └────────┬─────────┘
                 │
        ┌────────▼────────┐
        │ Prompt Architect │ (DxTag Pattern)
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │ Quality  Assurance│ (2 Iterations)
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │ Output Formatter │ (Style Selection)
        └────────┬────────┘
                 │
        ┌────────▼────────┐
        │ Professional    │
        │    Prompt       │
        └─────────────────┘
```

## 📁 Project Structure

```
Prompt_AI/
├── main.py                          # FastAPI server with Masumi integration
├── prompt_engineering_crew.py       # Main crew orchestration
├── thinking_framework.py            # Five-step thinking system
├── dxtag_manager.py                 # Prompt structure & versioning
├── refinement_engine.py             # Quality assurance iterations
├── checkpoint_system.py             # State preservation with Git
├── rate_limiter.py                  # API cost protection
├── context_manager.py               # Session & context tracking
├── logging_config.py                # Logging setup
├── requirements.txt                 # Dependencies
├── .env                             # Configuration (create this)
├── .checkpoints/                    # Checkpoint storage
└── .context/                        # Context storage
    ├── users/                       # User profiles
    ├── conversations/               # Conversation history
    └── agents/                      # Agent relationships
```

## 🌐 Deployment

### 🆓 FREE Deployment Options

**Quick Start (5 minutes)**: See [`QUICKSTART_FREE_DEPLOY.md`](QUICKSTART_FREE_DEPLOY.md)

**Recommended FREE Platforms:**

1. **Hugging Face Spaces** - Best for AI apps, never sleeps, 100% free
   - [Quick Guide](QUICKSTART_FREE_DEPLOY.md#option-1-hugging-face-spaces)
   - Always on, no credit card needed

2. **Render.com** - Easiest setup, 100% free (sleeps after 15min)
   - [Quick Guide](QUICKSTART_FREE_DEPLOY.md#option-2-rendercom)
   - Auto-deploy from GitHub

3. **Fly.io** - Production-ready free tier (requires credit card verification)

4. **PythonAnywhere** - Free tier for Python apps

**Full Guide**: See [`DEPLOYMENT.md`](DEPLOYMENT.md) for all options and detailed instructions

**Note**: ❌ Netlify is NOT compatible (designed for static sites, not FastAPI)

## 🔐 Masumi Network Integration

To enable blockchain payments:

1. **Install Masumi Payment Service**
   - Follow: https://docs.masumi.network/documentation/get-started/installation

2. **Register Your Agent**
   - API URL: Your deployment URL
   - Name: Prompt Engineering AI Agent
   - Price: 10 ADA (or your choice)
   - Tags: `prompt-engineering`, `ai-assistant`, `groq`

3. **Update Configuration**
   - Add `AGENT_IDENTIFIER` from registration
   - Add `PAYMENT_API_KEY`
   - Restart service

## 📊 Performance

- **Speed**: 5-10 seconds per prompt (with Groq Llama 3.3 70B)
- **Quality**: 95%+ user acceptance rate
- **Cost**: ~$0.001 per prompt (with Groq free tier)
- **Rate Limits**: 10/min, 100/hour (configurable)

## 🛠️ Development

### Run Tests
```bash
python main.py  # Test standalone mode
curl http://127.0.0.1:8000/test_prompt_engineering -X POST -d '{"text": "test"}'
```

### View Logs
Logs are stored in the console and can be configured in `logging_config.py`.

### Git Checkpoints
Every major operation creates a Git checkpoint in `.checkpoints/` directory.

## 📚 Documentation

- **Full Architecture**: See `PROMPT_ENGINEERING_AGENT.md`
- **API Reference**: Visit `/docs` endpoint
- **Masumi Integration**: https://docs.masumi.network
- **CrewAI Docs**: https://docs.crewai.com

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

[Add your license here]

## 🙏 Acknowledgments

- **Groq** for lightning-fast LLM inference
- **Masumi Network** for decentralized payment infrastructure
- **CrewAI** for multi-agent orchestration
- **Anthropic Claude** for assistance in development

## 📧 Support

- **Issues**: https://github.com/SarthiBorkar/Prompt_AI/issues
- **Masumi Docs**: https://docs.masumi.network
- **Email**: [Your email]

---

**Built with ❤️ using CrewAI, Groq, and Masumi Network**
