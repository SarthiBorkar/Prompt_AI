# Production PRD Generator AI Agent v2.0

MIP-003 compliant AI agent that generates professional Product Requirements Documents (PRDs).

## What Is This?

Input: `"Build a mobile banking app"`

Output: **Complete 8-section PRD** with Product Overview, Problem Statement, Goals, User Stories, Requirements, Success Metrics, and more.

## Quick Start

### 1. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
```

### 2. Add Groq API Key

Edit `.env`:
```env
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
LLM_PROVIDER=groq
```

Get free key: https://console.groq.com

### 3. Run (CLI Mode)

```bash
python main.py "Build a task management app for remote teams"
```

**Output:**
```
======================================================================
🚀 PRD Generator AI Agent
======================================================================

Input: Build a task management app for remote teams

⏳ Generating PRD...

======================================================================
✅ Generated PRD:
======================================================================

# Task Management App for Remote Teams

## Product Overview
A collaborative task management platform designed for remote teams...

## Problem Statement
...

[Complete 8-section PRD]
...

----------------------------------------------------------------------
📊 Word Count: 652
----------------------------------------------------------------------
```

### 4. Run (API Mode - Optional)

```bash
python main.py api
```

Server runs at: **http://localhost:8000**
Docs: **http://localhost:8000/docs**

## MIP-003 Endpoints (API Mode)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/availability` | GET | Check if agent is operational |
| `/input_schema` | GET | Get input requirements |
| `/start_job` | POST | Generate PRD (optionally with payment) |
| `/status?job_id=X` | GET | Check job status |
| `/provide_input` | POST | Provide additional input |
| `/health` | GET | Health check |

## Architecture

**v2.0 Streamlined:**
```
User Input → Single PRD Generator → Professional 8-Section PRD
```

**Performance:**
- ⚡ 1 agent (was 4 in v1.0)
- ⚡ 2,500 tokens/request (was 8,000 - **69% reduction**)
- ⚡ ~15 seconds (was ~45 seconds - **67% faster**)
- ✅ Clean output (no verbose logs)

## Payment Integration (Optional)

The agent supports Masumi payment integration for monetization. **This is optional** - the agent works without payment.

### Setup Payment (Advanced)

1. Register your agent at [Masumi Registry](https://registry.masumi.ai)
2. Get your `AGENT_IDENTIFIER`
3. Set up a Masumi Payment Service
4. Add to `.env`:

```env
# Optional - Masumi Payment Integration
AGENT_IDENTIFIER=your_agent_identifier_here
PAYMENT_SERVICE_URL=http://localhost:3001/api/v1
PAYMENT_API_KEY=your_payment_api_key
PAYMENT_AMOUNT=10000000
PAYMENT_UNIT=lovelace
NETWORK=Preprod
```

### Payment Error: "Application not found" (404)

If you see:
```
masumi.payment - ERROR - Payment request failed with status 404:
{"status":"error","code":404,"message":"Application not found"}
```

**Cause:** Your `AGENT_IDENTIFIER` is not registered in the Masumi Registry.

**Solutions:**
1. **Free Mode:** Remove payment variables from `.env` - agent will work without payment
2. **Register Agent:** Go to Masumi Registry and register your agent
3. **Use Valid ID:** If you have an agent ID, ensure it's correctly configured

**Without payment configured**, the agent runs in **FREE mode** and works perfectly for local/testing use.

## Usage Examples

### Test API Endpoints

```bash
# Check availability
curl http://localhost:8000/availability

# Start PRD generation (no payment needed if not configured)
curl -X POST http://localhost:8000/start_job \
  -H "Content-Type: application/json" \
  -d '{
    "identifier_from_purchaser": "user_123",
    "input_data": {"text": "Build an e-commerce platform"}
  }'

# Check status
curl "http://localhost:8000/status?job_id=YOUR_JOB_ID"
```

### Interactive API Docs

Visit: **http://localhost:8000/docs**

## Output Format

Every PRD has 8 sections:

1. **Product Overview** - 2-3 sentence summary
2. **Problem Statement** - What problem does this solve?
3. **Goals & Objectives** - 3-5 measurable goals
4. **User Stories** - "As a [user], I want [goal], so that [benefit]"
5. **Functional Requirements** - Numbered list of features
6. **Non-Functional Requirements** - Performance, security, scalability
7. **Success Metrics** - Measurable KPIs
8. **Out of Scope** - What's NOT included

## Configuration

### Required
```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
GROQ_MODEL=llama-3.3-70b-versatile
LLM_PROVIDER=groq
```

### Optional (Payment)
```env
AGENT_IDENTIFIER=your_registered_agent_id
PAYMENT_SERVICE_URL=http://localhost:3001/api/v1
PAYMENT_API_KEY=your_payment_key
NETWORK=Preprod
PAYMENT_AMOUNT=10000000
PAYMENT_UNIT=lovelace
```

### Optional (Server)
```env
API_PORT=8000
API_HOST=0.0.0.0
```

## Troubleshooting

### Rate Limit Error

```
Error: Rate limit reached. Please try again later or upgrade your Groq tier.
```

**Solution:** Groq free tier has 100k tokens/day. Wait 33 minutes or upgrade at https://console.groq.com/settings/billing

### Payment 404 Error

**Problem:** Agent not registered
**Solution:** Remove payment variables or register at Masumi Registry

### No Output / Verbose Logs

**Problem:** Logging not suppressed
**Solution:** Already fixed in v2.0 - update your code

## Documentation

- **USAGE.md** - Detailed usage guide
- **PRODUCTION_IMPROVEMENTS.md** - Technical architecture details
- **/docs** - Interactive API documentation (when server running)

## Version History

- **v2.0** (Current) - Single agent, clean output, 69% token reduction
- **v1.0** - Multi-agent pipeline with verbose logging (deprecated)

## License

MIT

## Support

- GitHub Issues: [Report bugs](https://github.com/yourrepo/issues)
- Documentation: See USAGE.md
- API Docs: http://localhost:8000/docs (when running)
