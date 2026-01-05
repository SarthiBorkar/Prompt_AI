"""
Prompt Engineering AI Agent - MIP-003 Compliant
"""

import os
import sys
import asyncio
import uvicorn
import uuid
from typing import Dict
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from masumi.config import Config
from masumi.payment import Payment, Amount
from prompt_engineering_crew import PromptEngineeringCrew
from logging_config import setup_logging

# Configure logging
logger = setup_logging()

# Load environment variables
load_dotenv(override=True)

# Configuration
AGENT_IDENTIFIER = os.getenv("AGENT_IDENTIFIER")
PAYMENT_SERVICE_URL = os.getenv("PAYMENT_SERVICE_URL")
PAYMENT_API_KEY = os.getenv("PAYMENT_API_KEY")
NETWORK = os.getenv("NETWORK", "Preprod")
PAYMENT_AMOUNT = os.getenv("PAYMENT_AMOUNT", "10000000")
PAYMENT_UNIT = os.getenv("PAYMENT_UNIT", "lovelace")

# Initialize FastAPI with production metadata
app = FastAPI(
    title="Production PRD Generator AI Agent",
    description="""
    MIP-003 compliant AI agent that generates production-ready Product Requirements Documents (PRDs).

    **Features:**
    - Analyzes user input and extracts requirements
    - Generates professional PRD with 8 standard sections
    - Quality validation with iterative refinement
    - Token-optimized for cost efficiency
    - Rate limiting and input validation

    **Output Format:**
    - Product Overview
    - Problem Statement
    - Goals & Objectives
    - User Stories
    - Functional Requirements
    - Non-Functional Requirements
    - Success Metrics
    - Out of Scope
    """,
    version="2.0.0",
    contact={
        "name": "Prompt Engineering Team",
        "email": "support@promptai.dev"
    }
)

# Job storage
jobs = {}
payment_instances = {}

# Masumi config
config = Config(
    payment_service_url=PAYMENT_SERVICE_URL,
    payment_api_key=PAYMENT_API_KEY
) if PAYMENT_SERVICE_URL and PAYMENT_API_KEY else None

# ─────────────────────────────────────────────────────────────────────────────
# Models
# ─────────────────────────────────────────────────────────────────────────────
class StartJobRequest(BaseModel):
    """Request model for starting a new PRD generation job"""
    identifier_from_purchaser: str
    input_data: Dict[str, str]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "identifier_from_purchaser": "user_123",
                    "input_data": {
                        "text": "Build a mobile app for restaurant order management with real-time kitchen updates",
                        "style": "structured"
                    }
                }
            ]
        }
    }

class ProvideInputRequest(BaseModel):
    job_id: str
    input_data: Dict[str, str]

# ─────────────────────────────────────────────────────────────────────────────
# Core Function
# ─────────────────────────────────────────────────────────────────────────────
async def execute_prompt_engineering(text: str, style: str = "structured") -> Dict:
    """
    Execute PRD generation with clean output

    Args:
        text: User input describing the product/feature
        style: Output style (default: structured)

    Returns:
        Dict with PRD or error info
    """
    try:
        crew = PromptEngineeringCrew(logger=logger, verbose=False)
        result = await crew.process_input(text=text, style=style)

        if isinstance(result, dict) and result.get("success"):
            return {
                "success": True,
                "prd": result.get("prd", ""),
                "metadata": result.get("metadata", {})
            }
        else:
            return result

    except Exception as e:
        error_msg = str(e)

        # Handle rate limit errors with helpful message
        if "rate_limit" in error_msg.lower():
            return {
                "success": False,
                "error": "Rate limit reached. Please try again later or upgrade your Groq tier.",
                "error_type": "RateLimitError",
                "details": error_msg
            }

        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }

# ─────────────────────────────────────────────────────────────────────────────
# MIP-003 Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/availability")
async def check_availability():
    """Checks if the server is operational"""
    return {
        "status": "available",
        "agentIdentifier": AGENT_IDENTIFIER,
        "message": "Server operational"
    }

@app.get("/input_schema")
async def get_input_schema():
    """Returns input requirements"""
    return {
        "input_data": [
            {
                "id": "text",
                "type": "string",
                "name": "Prompt Description",
                "data": {
                    "description": "Brief description of the prompt you need engineered",
                    "placeholder": "e.g., 'Create a prompt for analyzing customer feedback sentiment'",
                    "validation": {
                        "required": True,
                        "min_length": 10,
                        "max_length": 5000
                    }
                }
            }
        ]
    }

@app.post("/start_job")
async def start_job(request: StartJobRequest):
    """Initiates a new job with payment"""
    job_id = str(uuid.uuid4())
    text = request.input_data.get("text", "")

    if not text:
        raise HTTPException(status_code=400, detail="Text field required in input_data")

    logger.info(f"Starting job {job_id}")

    # Try payment service if configured
    if config and AGENT_IDENTIFIER:
        try:
            amounts = [Amount(amount=PAYMENT_AMOUNT, unit=PAYMENT_UNIT)]

            payment = Payment(
                agent_identifier=AGENT_IDENTIFIER,
                amounts=amounts,
                config=config,
                identifier_from_purchaser=request.identifier_from_purchaser,
                input_data=request.input_data,
                network=NETWORK
            )

            payment_request = await payment.create_payment_request()
            blockchain_identifier = payment_request["data"]["blockchainIdentifier"]
            payment.payment_ids.add(blockchain_identifier)

            # Store job
            jobs[job_id] = {
                "status": "awaiting_payment",
                "payment_status": "pending",
                "blockchain_identifier": blockchain_identifier,
                "input_data": request.input_data,
                "result": None
            }

            # Payment callback
            async def payment_callback(bid: str):
                await handle_payment_confirmed(job_id, bid)

            payment_instances[job_id] = payment
            await payment.start_status_monitoring(payment_callback)

            return {
                "status": "success",
                "job_id": job_id,
                "blockchainIdentifier": blockchain_identifier,
                "submitResultTime": payment_request["data"]["submitResultTime"],
                "unlockTime": payment_request["data"]["unlockTime"],
                "agentIdentifier": AGENT_IDENTIFIER,
                "amounts": [{"amount": amt.amount, "unit": amt.unit} for amt in amounts],
                "payByTime": payment_request["data"]["payByTime"]
            }

        except Exception as e:
            logger.warning(f"Payment service unavailable: {str(e)}")
            # Fall through to execute without payment

    # Execute without payment
    logger.info("Executing job without payment")

    jobs[job_id] = {
        "status": "running",
        "input_data": request.input_data,
        "result": None
    }

    try:
        result = await execute_prompt_engineering(text)
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = result

        return {
            "status": "completed",
            "job_id": job_id,
            "result": result
        }
    except Exception as e:
        logger.error(f"Error executing job: {str(e)}", exc_info=True)
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        raise HTTPException(status_code=500, detail=str(e))

async def handle_payment_confirmed(job_id: str, payment_id: str):
    """Execute job after payment confirmation"""
    try:
        logger.info(f"Payment confirmed for job {job_id}, executing...")

        jobs[job_id]["status"] = "running"
        text = jobs[job_id]["input_data"].get("text", "")

        result = await execute_prompt_engineering(text)

        # Complete payment
        await payment_instances[job_id].complete_payment(payment_id, result)

        jobs[job_id]["status"] = "completed"
        jobs[job_id]["payment_status"] = "completed"
        jobs[job_id]["result"] = result

        # Cleanup
        if job_id in payment_instances:
            payment_instances[job_id].stop_status_monitoring()
            del payment_instances[job_id]

    except Exception as e:
        logger.error(f"Error processing job {job_id}: {str(e)}", exc_info=True)
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

@app.get("/status")
async def get_status(job_id: str = Query(..., description="Job ID to check")):
    """Check job status"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_id]

    # Update payment status if available
    if job_id in payment_instances:
        try:
            status = await payment_instances[job_id].check_payment_status()
            job["payment_status"] = status.get("data", {}).get("status")
        except:
            pass

    return {
        "job_id": job_id,
        "status": job["status"],
        "payment_status": job.get("payment_status"),
        "result": job.get("result")
    }

@app.post("/provide_input")
async def provide_input(request: ProvideInputRequest):
    """Provide additional input to a job"""
    if request.job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    # Update job input data
    jobs[request.job_id]["input_data"].update(request.input_data)

    return {"status": "success", "message": "Input updated"}

# ─────────────────────────────────────────────────────────────────────────────
# Additional Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy"}

# ─────────────────────────────────────────────────────────────────────────────
# Standalone Mode
# ─────────────────────────────────────────────────────────────────────────────
def main_standalone():
    """Run without API - Clean CLI interface"""
    import sys
    os.environ['CREWAI_DISABLE_TELEMETRY'] = 'true'

    print("\n" + "=" * 70)
    print("🚀 PRD Generator AI Agent")
    print("=" * 70 + "\n")

    # Get input from command line or use default
    if len(sys.argv) > 2:
        user_input = " ".join(sys.argv[2:])
    else:
        user_input = "Create a prompt for analyzing customer feedback sentiment"

    print(f"Input: {user_input}\n")
    print("⏳ Generating PRD...\n")

    try:
        result = asyncio.run(execute_prompt_engineering(user_input, style="structured"))

        print("=" * 70)
        if result.get("success"):
            print("✅ Generated PRD:")
            print("=" * 70 + "\n")
            print(result.get("prd", ""))

            # Show metadata
            metadata = result.get("metadata", {})
            if metadata:
                print("\n" + "-" * 70)
                print(f"📊 Word Count: {metadata.get('word_count', 'N/A')}")
                print("-" * 70)
        else:
            print("❌ Error:")
            print("=" * 70 + "\n")
            print(f"Type: {result.get('error_type', 'Unknown')}")
            print(f"Message: {result.get('error', 'Unknown error')}")

            if result.get("details"):
                print(f"\nDetails: {result['details']}")

        print("\n" + "=" * 70 + "\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal Error: {str(e)}\n")
        sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        port = int(os.getenv("API_PORT", 8000))
        host = os.getenv("API_HOST", "0.0.0.0")

        print("\n" + "=" * 70)
        print("🚀 Prompt Engineering AI Agent - MIP-003")
        print("=" * 70)
        print(f"\nServer: http://{host}:{port}")
        print(f"Docs:   http://{host}:{port}/docs")
        print(f"\nMIP-003 Endpoints:")
        print(f"  GET  /availability")
        print(f"  GET  /input_schema")
        print(f"  POST /start_job")
        print(f"  GET  /status")
        print(f"  POST /provide_input")

        if config and AGENT_IDENTIFIER:
            print(f"\n✅ Payment service configured")
        else:
            print(f"\n⚠️  Payment service not configured (will run without payments)")

        print("\n" + "=" * 70 + "\n")

        uvicorn.run(app, host=host, port=port, log_level="info")
    else:
        main_standalone()
