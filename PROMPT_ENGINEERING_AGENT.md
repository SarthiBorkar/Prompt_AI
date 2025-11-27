# Prompt Engineering AI Agent for Masumi Network

A sophisticated prompt engineering agent built with CrewAI that transforms brief, unstructured input into optimized, structured prompts. Designed to operate within the Masumi Network ecosystem with full payment integration.

## Overview

This agent serves as a professional prompt engineer that bridges the communication gap in agent-to-agent ecosystems and human-to-agent interactions. When given brief input, it applies a five-step thinking framework to create professionally structured, effective prompts.

## Architecture

### Core Components

#### 1. **Five-Step Thinking Framework** (`thinking_framework.py`)
The agent employs four distinct thinking modalities in parallel:

- **Logical Thinking**: Establishes cause-and-effect relationships, identifies contradictions
- **Analytical Thinking**: Breaks down complex requests into components
- **Computational Thinking**: Translates concepts into structured, executable patterns
- **Producer Thinking**: Focuses on practical end results and consumption patterns

#### 2. **DxTag Pattern Manager** (`dxtag_manager.py`)
Implements the DxTag architectural pattern for prompt structure:

- **D**ata: Role, task, context, examples
- **X**ecution: Constraints, processing instructions, output format
- **Tag**: Metadata, versioning, complexity assessment

Features:
- Semantic versioning (MAJOR.MINOR.PATCH)
- Version history tracking
- Dependency management for multi-agent workflows
- Multiple output formats (structured, minimal, conversational)

#### 3. **Checkpoint System** (`checkpoint_system.py`)
Automatic state preservation with Git integration:

- Checkpoint creation at critical junctures
- Automatic Git commits with descriptive messages
- Corruption detection through hash verification
- Rollback capabilities to any previous state

#### 4. **Two-Iteration Refinement Engine** (`refinement_engine.py`)
Internal quality assurance mechanism:

- **Iteration 1**: Evaluates and improves structure, clarity, specificity
- **Iteration 2**: Fine-tunes and polishes the refined prompt
- Quality scoring against professional standards
- Learning from improvement patterns

Quality criteria evaluated:
- Clear intent
- Specific constraints
- Easy parsing
- No ambiguities
- Proper structure

#### 5. **Rate Limiter** (`rate_limiter.py`)
Conservative rate limiting to prevent API cost overruns:

- **Per second**: 2 requests
- **Per minute**: 10 requests
- **Per hour**: 100 requests
- **Per day**: 1000 requests

Features:
- Exponential backoff with jitter
- Request queuing
- Cache support for frequent patterns (15-minute TTL)

#### 6. **Context Manager** (`context_manager.py`)
Sophisticated context awareness with JSON persistence:

- **User Profiles**: Preferences, history, learning patterns
- **Conversation Context**: Message history, current prompt state
- **Agent Context**: For Masumi agent-to-agent interactions

## Specialized Agents

The prompt engineering crew consists of 5 specialized agents:

1. **Input Analysis Specialist** - Applies multi-dimensional thinking to understand user intent
2. **Requirements Clarification Expert** - Identifies gaps and asks clarifying questions
3. **Prompt Architecture Designer** - Designs prompts using DxTag pattern
4. **Quality Assurance Specialist** - Performs two-iteration refinement
5. **Output Formatting Expert** - Formats prompts for target audience

## Usage

### Standalone Mode (Testing)

```bash
# Make sure to add your OpenAI API key to .env first
python main.py
```

This runs the agent locally without API/payments for development and testing.

### API Mode (Production with Masumi)

```bash
python main.py api
```

This starts the FastAPI server with full Masumi payment integration.

### API Endpoints (MIP-003 Standard)

1. **GET /input_schema** - Returns input requirements
2. **GET /availability** - Checks server operational status
3. **POST /start_job** - Initiates prompt engineering task with payment
4. **GET /status?job_id=X** - Checks job and payment status
5. **POST /provide_input** - Provides additional input (if needed)

### Example Request

```bash
curl -X POST "http://localhost:8000/start_job" \
-H "Content-Type: application/json" \
-d '{
    "identifier_from_purchaser": "unique_hex_identifier",
    "input_data": {
        "text": "Create a prompt for analyzing customer feedback sentiment"
    }
}'
```

Response includes `job_id` and payment details. After payment confirmation, the agent processes the request and returns the engineered prompt.

## Configuration

### Environment Variables (.env)

```ini
# OpenAI
OPENAI_API_KEY=your_openai_api_key

# Masumi Payment Service
PAYMENT_SERVICE_URL=http://localhost:3001/api/v1
PAYMENT_API_KEY=your_payment_api_key

# Agent Configuration
AGENT_IDENTIFIER=your_agent_identifier_from_registration
PAYMENT_AMOUNT=10000000
PAYMENT_UNIT=lovelace
SELLER_VKEY=your_selling_wallet_vkey

# Network
NETWORK=Preprod  # or Mainnet
```

## File Structure

```
promptAI/
├── main.py                          # FastAPI app with Masumi integration
├── prompt_engineering_crew.py       # Main crew orchestration
├── thinking_framework.py            # Five-step thinking system
├── dxtag_manager.py                 # Prompt structure & versioning
├── refinement_engine.py             # Quality assurance iterations
├── checkpoint_system.py             # State preservation with Git
├── rate_limiter.py                  # API cost protection
├── context_manager.py               # Session & context tracking
├── logging_config.py                # Logging setup
├── requirements.txt                 # Dependencies
├── .env                             # Configuration
├── .checkpoints/                    # Checkpoint storage
└── .context/                        # Context storage
    ├── users/                       # User profiles
    ├── conversations/               # Conversation history
    └── agents/                      # Agent relationships
```

## Key Features

### Minimal Code Changes Principle
When implementing features or fixes, the system makes the smallest possible modifications to reduce bugs and maintain readability.

### Efficient Resource Management
- Intelligent caching reduces redundant API calls
- Rate limiting with exponential backoff prevents cost overruns
- Token usage tracking and optimization

### Security & Privacy
- Comprehensive authentication
- Session management with automatic timeout
- Encryption at rest and in transit
- Context isolation between users/agents

### Masumi Network Integration
- First-class citizen in Masumi ecosystem
- Automatic payment processing via blockchain
- Service level agreement tracking
- Agent-to-agent discovery via service registry

## Development Workflow

1. **Local Testing**: Use standalone mode to test prompt engineering logic
2. **API Testing**: Run API mode locally with test payments
3. **Masumi Registration**: Register agent on Masumi Network
4. **Production Deploy**: Deploy with production API keys and monitoring

## Success Metrics

The system tracks:

- **Primary**: Prompt acceptance rate, iteration count, user retention
- **Efficiency**: Processing time, API cost per prompt, cache hit rate
- **Quality**: Clarity scores, specificity metrics, effectiveness ratings

## Future Enhancements

Post-MVP features planned:
- Advanced prompt patterns (chain-of-thought, few-shot, constitutional AI)
- Domain-specific optimization
- Prompt testing and validation
- Analytics and performance tracking
- Community prompt library integration

## Troubleshooting

### "Invalid API Key" Error
Add your real OpenAI API key to `.env`:
```ini
OPENAI_API_KEY=sk-...your-real-key...
```

### Rate Limit Exceeded
The system has conservative limits. Check stats:
```python
crew.get_statistics()
```

### Checkpoint/Context Issues
Check directory permissions for `.checkpoints/` and `.context/`

## Contributing

This agent follows the PRD specifications for the Masumi Network prompt engineering service. All changes should maintain:
- The five-step thinking framework
- Two-iteration refinement process
- Minimal code change principle
- Rate limiting and efficiency constraints

## License

[Add your license here]

## Support

For issues or questions about:
- **Masumi Integration**: https://docs.masumi.network
- **CrewAI**: https://docs.crewai.com
- **This Agent**: [Your support channel]
