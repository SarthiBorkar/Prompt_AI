"""
Prompt Engineering Crew
Implements the complete prompt engineering pipeline with specialized agents
"""

import os
import logging
from crewai import Agent, Crew, Task, LLM
from logging_config import get_logger
from thinking_framework import MultiDimensionalThinking
from dxtag_manager import DxTagManager, PromptComponent
from refinement_engine import RefinementEngine
from checkpoint_system import CheckpointSystem
from context_manager import ContextManager
from rate_limiter import RateLimiter, RateLimitConfig
from typing import Dict, Any, Optional, List
import json

# Suppress CrewAI and LiteLLM verbose logging
logging.getLogger('crewai').setLevel(logging.ERROR)
logging.getLogger('litellm').setLevel(logging.ERROR)
logging.getLogger('httpx').setLevel(logging.ERROR)
logging.getLogger('openai').setLevel(logging.ERROR)


class PromptEngineeringCrew:
    """
    Main crew for prompt engineering using the five-step thinking framework
    """

    # Production configuration constants
    MIN_INPUT_LENGTH = 10
    MAX_INPUT_LENGTH = 5000
    SUPPORTED_STYLES = ["structured", "minimal", "conversational"]

    def __init__(self, verbose=True, logger=None, user_id: Optional[str] = None):
        """
        Initialize production-grade prompt engineering crew

        Args:
            verbose: Whether to enable verbose logging
            logger: Optional logger instance
            user_id: Optional user identifier for context management
        """
        self.verbose = verbose
        self.logger = logger or get_logger(__name__)
        self.user_id = user_id

        # Configure LLM based on provider
        try:
            self.llm = self._configure_llm()
        except ValueError as e:
            self.logger.error(f"LLM configuration failed: {e}")
            raise

        # Initialize core systems
        self.thinking_framework = MultiDimensionalThinking()
        self.dxtag_manager = DxTagManager()
        self.refinement_engine = RefinementEngine()
        self.checkpoint_system = CheckpointSystem()
        self.context_manager = ContextManager()
        self.rate_limiter = RateLimiter(RateLimitConfig())

        # Create crew
        self.crew = self.create_crew()
        self.logger.info("Production PromptEngineeringCrew initialized successfully")

    def _validate_input(self, text: str, style: str) -> tuple[bool, Optional[str]]:
        """
        Validate input parameters for production use

        Args:
            text: Input text to validate
            style: Output style to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check text length
        if not text or len(text.strip()) < self.MIN_INPUT_LENGTH:
            return False, f"Input too short. Minimum {self.MIN_INPUT_LENGTH} characters required."

        if len(text) > self.MAX_INPUT_LENGTH:
            return False, f"Input too long. Maximum {self.MAX_INPUT_LENGTH} characters allowed."

        # Check for valid style
        if style not in self.SUPPORTED_STYLES:
            return False, f"Invalid style '{style}'. Supported: {', '.join(self.SUPPORTED_STYLES)}"

        # Check for malicious content (basic)
        suspicious_patterns = ['<script', 'javascript:', 'eval(', 'exec(']
        text_lower = text.lower()
        for pattern in suspicious_patterns:
            if pattern in text_lower:
                return False, "Input contains potentially malicious content."

        return True, None

    def _configure_llm(self) -> LLM:
        """
        Configure LLM based on environment variables

        Returns:
            Configured LLM instance
        """
        provider = os.getenv("LLM_PROVIDER", "openai").lower()

        if provider == "groq":
            groq_api_key = os.getenv("GROQ_API_KEY")
            groq_model = os.getenv("GROQ_MODEL", "llama-3.1-70b-versatile")

            if not groq_api_key or groq_api_key == "your_groq_api_key_here":
                raise ValueError("GROQ_API_KEY not set in .env file")

            self.logger.info(f"Using Groq LLM with model: {groq_model}")
            return LLM(
                model=f"groq/{groq_model}",
                api_key=groq_api_key
            )
        else:  # Default to OpenAI
            openai_api_key = os.getenv("OPENAI_API_KEY")

            if not openai_api_key or openai_api_key == "your_openai_api_key":
                raise ValueError("OPENAI_API_KEY not set in .env file")

            self.logger.info("Using OpenAI LLM with model: gpt-4")
            return LLM(
                model="gpt-4",
                api_key=openai_api_key
            )

    def create_crew(self) -> Crew:
        """
        Creates production-grade prompt engineering crew with optimized agents

        Returns:
            Configured Crew instance
        """
        self.logger.info("Creating prompt engineering crew with specialized agents")

        # Single PRD Generator Agent (simplified)
        prd_generator = Agent(
            role='Senior Product Manager',
            goal='Generate complete, professional PRD in one pass',
            backstory='''You are a senior PM at a top tech company. You create comprehensive,
            production-ready PRDs with 8 sections: Product Overview, Problem Statement,
            Goals & Objectives, User Stories, Functional Requirements, Non-Functional Requirements,
            Success Metrics, and Out of Scope. Be concise, specific, and measurable.''',
            verbose=False,
            llm=self.llm,
            max_iter=1,
            allow_delegation=False
        )

        # Single streamlined task for clean output
        tasks = [
            Task(
                description='''Generate a professional Product Requirements Document (PRD) for: {text}

                Create a complete PRD with these 8 sections:

                # [Product/Feature Name]

                ## Product Overview
                2-3 sentences describing what this product/feature is and its core value.

                ## Problem Statement
                What problem does this solve? What pain points does it address?

                ## Goals & Objectives
                3-5 specific, measurable goals in bullet points.

                ## User Stories
                2-3 user stories in format: "As a [user], I want [goal], so that [benefit]"

                ## Functional Requirements
                Numbered list of specific features and capabilities.

                ## Non-Functional Requirements
                Performance, security, scalability, usability requirements.

                ## Success Metrics
                Measurable KPIs to track success (e.g., "90% accuracy", "< 1s response time").

                ## Out of Scope
                What is explicitly NOT included in this release.

                **CRITICAL RULES:**
                - Output ONLY the PRD in markdown format
                - NO meta-commentary or explanations
                - NO phrases like "this demonstrates" or "the final answer"
                - Professional, concise tone
                - Maximum 700 words
                - STOP immediately after "Out of Scope" section''',
                expected_output='''A complete, professional PRD in markdown format with exactly 8 sections.
                Maximum 700 words. No additional commentary. Just the PRD itself.''',
                agent=prd_generator
            )
        ]

        crew = Crew(
            agents=[prd_generator],
            tasks=tasks,
            verbose=False,
            output_log_file=False
        )

        self.logger.info("Prompt engineering crew created successfully")
        return crew

    async def process_input(
        self,
        text: str,
        style: str = "structured",
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Production-grade input processing with validation and error handling

        Args:
            text: Raw input text (10-5000 chars)
            style: Output style (structured, minimal, conversational)
            conversation_id: Optional conversation ID for context

        Returns:
            Dictionary with PRD output and metadata

        Raises:
            ValueError: If input validation fails
        """
        # Input validation (production safety)
        is_valid, error_msg = self._validate_input(text, style)
        if not is_valid:
            self.logger.warning(f"Input validation failed: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "error_type": "validation_error"
            }

        self.logger.info(f"Processing validated input ({len(text)} chars, style={style})")

        # Check rate limit
        allowed, reason = self.rate_limiter.check_rate_limit(self.user_id)
        if not allowed:
            self.logger.warning(f"Rate limit exceeded: {reason}")
            return {
                "success": False,
                "error": reason,
                "error_type": "rate_limit_error",
                "rate_limit_info": self.rate_limiter.get_stats()
            }

        # Create checkpoint at start
        initial_state = {
            "text": text,
            "style": style,
            "timestamp": self.checkpoint_system.checkpoints.get(
                self.checkpoint_system.current_checkpoint
            ).timestamp if self.checkpoint_system.current_checkpoint else None
        }
        self.checkpoint_system.create_checkpoint(
            state=initial_state,
            reasoning="Starting prompt engineering process",
            changes=["Initial input received"]
        )

        # Create or get conversation context
        if not conversation_id and self.user_id:
            conversation_id = self.context_manager.create_conversation(
                user_id=self.user_id,
                metadata={"style": style}
            )

        # Add input message to context
        if conversation_id:
            self.context_manager.add_message(
                conversation_id=conversation_id,
                role="user",
                content=text
            )

        try:
            # Run streamlined PRD generation (single pass)
            self.logger.info("Generating PRD...")
            crew_result = self.crew.kickoff(inputs={"text": text})

            # Extract PRD output
            prd_output = crew_result.raw if hasattr(crew_result, "raw") else str(crew_result)

            # Validate output
            word_count = len(prd_output.split())

            # Record successful request
            self.rate_limiter.record_request(self.user_id)

            self.logger.info(f"✅ PRD generated ({word_count} words)")

            return {
                "success": True,
                "prd": prd_output,
                "metadata": {
                    "word_count": word_count,
                    "style": style,
                    "input_length": len(text)
                },
                "conversation_id": conversation_id
            }

        except Exception as e:
            self.logger.error(f"Production pipeline error: {str(e)}", exc_info=True)
            self.rate_limiter.record_failure(self.user_id)

            # Return structured error
            error_type = type(e).__name__
            return {
                "success": False,
                "error": str(e),
                "error_type": error_type,
                "rate_limit_info": self.rate_limiter.get_stats(),
                "retry_recommended": error_type in ["TimeoutError", "ConnectionError"]
            }

    def get_conversation_context(self, conversation_id: str) -> List[Dict[str, Any]]:
        """Gets conversation history"""
        return self.context_manager.get_conversation_history(conversation_id)

    def rollback_to_checkpoint(self, checkpoint_id: str) -> Dict[str, Any]:
        """Rolls back to a specific checkpoint"""
        return self.checkpoint_system.rollback_to(checkpoint_id)

    def get_statistics(self) -> Dict[str, Any]:
        """Gets comprehensive statistics"""
        return {
            "context": self.context_manager.get_statistics(),
            "rate_limiter": self.rate_limiter.get_stats(),
            "refinement": self.refinement_engine.get_refinement_stats(),
            "checkpoints": len(self.checkpoint_system.checkpoints)
        }
