# PRD Generator AI Agent - Usage Guide

## Quick Start

### CLI Usage

```bash
# Activate virtual environment
source .venv/bin/activate

# Run with custom input
python main.py "Build a mobile banking app with biometric authentication"

# Run with default example
python main.py
```

### Expected Output

```
======================================================================
🚀 PRD Generator AI Agent
======================================================================

Input: Build a mobile banking app with biometric authentication

⏳ Generating PRD...

======================================================================
✅ Generated PRD:
======================================================================

# Mobile Banking App with Biometric Authentication

## Product Overview
[Clean PRD output here - 8 sections]
...

----------------------------------------------------------------------
📊 Word Count: 652
----------------------------------------------------------------------

======================================================================
```

## Features

✅ **Clean Output** - Only shows the final PRD, no verbose logs
✅ **Single Agent** - Streamlined architecture, faster processing
✅ **Rate Limit Handling** - Graceful error messages for API limits
✅ **Production Ready** - Professional markdown PRD format
✅ **Token Optimized** - ~70% less tokens than v1.0

## Architecture

```
User Input
    ↓
[Single PRD Generator Agent]
    ↓
Professional 8-Section PRD
```

**Simplified from 4 agents to 1 agent** for:
- Faster processing
- Cleaner output
- Better stability
- Lower token usage

## PRD Format

Every PRD contains exactly 8 sections:

1. **Product Overview** - 2-3 sentences
2. **Problem Statement** - Pain points being addressed
3. **Goals & Objectives** - 3-5 measurable goals
4. **User Stories** - 2-3 stories in standard format
5. **Functional Requirements** - Numbered features
6. **Non-Functional Requirements** - Performance, security, etc.
7. **Success Metrics** - Measurable KPIs
8. **Out of Scope** - What's NOT included

## API Usage

### Start Server

```bash
python main.py api
```

Server will run on `http://0.0.0.0:7860`

### Endpoints

**POST** `/start_job` - Generate PRD
```json
{
  "identifier_from_purchaser": "user_123",
  "input_data": {
    "text": "Your product description here"
  }
}
```

**GET** `/availability` - Check if server is running
**GET** `/input_schema` - Get input requirements
**GET** `/health` - Health check

## Error Handling

### Rate Limit Error

```
❌ Error:
======================================================================

Type: RateLimitError
Message: Rate limit reached. Please try again later or upgrade your Groq tier.
```

**Solution**: Wait 33 minutes or upgrade Groq plan

### Input Validation Error

```
error_type: validation_error
error: Input too short. Minimum 10 characters required.
```

**Solution**: Provide at least 10 characters of input

## Environment Setup

Required in `.env`:

```bash
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
LLM_PROVIDER=groq
```

Optional:
```bash
NETWORK=Preprod
PAYMENT_SERVICE_URL=http://localhost:3001
PAYMENT_API_KEY=your_payment_key
AGENT_IDENTIFIER=your_agent_id
```

## Token Usage

| Version | Tokens/Request | Time |
|---------|----------------|------|
| v1.0 (4 agents) | ~8,000 | ~45s |
| **v2.0 (1 agent)** | **~2,500** | **~15s** |

**Savings: 69% fewer tokens, 67% faster**

## Troubleshooting

### No output shown

Check that logging is set correctly:
```python
logging.getLogger('crewai').setLevel(logging.ERROR)
```

### Verbose CrewAI logs appearing

Ensure `verbose=False` in:
- Agent initialization
- Crew initialization
- `process_input()` call

### Rate limit hit immediately

Your daily Groq quota (100k tokens) is exhausted. Wait or upgrade.

## Best Practices

1. **Keep input focused** - 50-200 words works best
2. **Be specific** - Include target users, key features
3. **Use examples** - Reference similar products if helpful
4. **Check rate limits** - Monitor your Groq usage

## Examples

### Good Input
```
Build a project management tool for remote teams with
real-time collaboration, Kanban boards, time tracking,
and Slack integration. Target small teams (5-20 people).
```

### Bad Input
```
App
```
(Too short - will fail validation)

## Support

- Check logs in `logs/` directory
- Review `.env` configuration
- Verify Groq API key is valid
- Ensure you haven't hit rate limits
