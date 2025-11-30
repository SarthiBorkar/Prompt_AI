# Quick Start - Prompt Engineering AI Agent

Simple guide to test your AI agent (no Masumi integration).

## 🚀 Setup

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure API key**

Edit `.env` file:
```env
# Choose your LLM provider
LLM_PROVIDER=groq  # or openai

# Add your API key
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

## 🎯 Usage

### Option 1: Interactive Mode (Recommended)
```bash
python main_simple.py
```

This will start an interactive session where you can keep entering prompts:
```
💭 What prompt do you need? > Create a prompt for sentiment analysis
⏳ Processing with 5 AI agents...

✅ Engineered Prompt
----------------------------------------------------------------------
[Your professional prompt will appear here]
----------------------------------------------------------------------
```

### Option 2: Single Test
```bash
python main_simple.py "Your prompt description here"
```

Example:
```bash
python main_simple.py "Create a prompt for analyzing customer feedback"
```

### Option 3: Run Multiple Tests
```bash
./test_simple.sh
```

This will run 3 pre-configured test cases.

## 📋 What You Have

**Core AI Agent Files** (all working together):
- `prompt_engineering_crew.py` - 5 AI agents working together
- `thinking_framework.py` - Multi-dimensional analysis
- `dxtag_manager.py` - Prompt structure management
- `refinement_engine.py` - Quality assurance (2 iterations)
- `checkpoint_system.py` - State tracking
- `context_manager.py` - Conversation history
- `rate_limiter.py` - Request limiting
- `logging_config.py` - Logging setup

**Entry Point**:
- `main_simple.py` - Simple interface (no payment integration)

**Documentation**:
- `README.md` - Full documentation
- `MIP-003_COMPLIANCE.md` - For when you add Masumi later
- `TESTING_GUIDE.md` - Comprehensive testing guide

## 🧪 Test Examples

```bash
# Test 1: Sentiment analysis
python main_simple.py "Create a prompt for analyzing customer feedback sentiment"

# Test 2: Code review
python main_simple.py "Generate a prompt for code review with security focus"

# Test 3: Technical prompt
python main_simple.py "Draft a prompt for making a stablecoin MVP for Cardano"
```

## 📊 What the Agent Does

Your 5-agent pipeline:
1. **Input Analyzer** - Analyzes with 4 thinking modes
2. **Requirements Clarifier** - Identifies gaps
3. **Prompt Architect** - Structures with DxTag pattern
4. **Quality Specialist** - 2 iterations of refinement
5. **Output Formatter** - Formats for your needs

## ⏱️ Expected Performance

- Processing time: 30-60 seconds per prompt
- Quality: Professional-grade prompts
- Output: Structured, clear, and ready to use

## 🐛 Troubleshooting

**"API key not set"**
→ Check your `.env` file has `GROQ_API_KEY` or `OPENAI_API_KEY`

**"Module not found"**
→ Run `pip install -r requirements.txt`

**Slow responses**
→ Normal! The 5-agent pipeline takes time for quality

## 🎉 That's It!

Just run:
```bash
python main_simple.py
```

And start creating professional prompts!
