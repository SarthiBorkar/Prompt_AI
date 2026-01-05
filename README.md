# Prompt Engineering AI Agent

MIP-003 compliant prompt engineering service with Masumi Network integration.

## Quick Start

```bash
# Activate environment
source .venv/bin/activate

# Run API server
python3 main.py api
```

Server runs at: **http://localhost:8000**

## MIP-003 Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/availability` | GET | Check if server is operational |
| `/input_schema` | GET | Get input requirements |
| `/start_job` | POST | Start new job (with payment) |
| `/status` | GET | Check job status |
| `/provide_input` | POST | Provide additional input |

## Configuration

Add to `.env`:

```env
# Required - LLM
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Optional - Masumi Payment
AGENT_IDENTIFIER=your_agent_id
PAYMENT_SERVICE_URL=http://localhost:3001/api/v1
PAYMENT_API_KEY=your_payment_key
PAYMENT_AMOUNT=10000000
PAYMENT_UNIT=lovelace
NETWORK=Preprod
```


## Usage Examples

### Test Endpoints

```bash
# Check availability
curl http://localhost:8000/availability

# Get input schema
curl http://localhost:8000/input_schema

# Start job (with payment)
curl -X POST http://localhost:8000/start_job \
  -H "Content-Type: application/json" \
  -d '{
    "identifier_from_purchaser": "user_123",
    "input_data": {"text": "Create a prompt for sentiment analysis"}
  }'

# Check status
curl "http://localhost:8000/status?job_id=YOUR_JOB_ID"
```

### Interactive Docs

Visit: **http://localhost:8000/docs**

## What It Does

Transforms brief input into professional, structured prompts using:

1. **Input Analyzer** - Multi-dimensional thinking
2. **Requirements Clarifier** - Gap identification
3. **Prompt Architect** - DxTag pattern
4. **Quality Specialist** - Two-iteration refinement
5. **Output Formatter** - Style formatting

## Features

- ✅ MIP-003 compliant endpoints
- ✅ Masumi payment integration
- ✅ 5 specialized AI agents
- ✅ Multi-dimensional thinking
- ✅ Two-iteration quality assurance

## Get API Key

Free Groq API key: https://console.groq.com
