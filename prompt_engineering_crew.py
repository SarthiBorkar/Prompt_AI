"""
Prompt Engineering Crew
Implements the complete prompt engineering pipeline with specialized agents
"""

import os
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


class PromptEngineeringCrew:
    """
    Main crew for prompt engineering using the five-step thinking framework
    """

    def __init__(self, verbose=True, logger=None, user_id: Optional[str] = None):
        """
        Initialize the prompt engineering crew

        Args:
            verbose: Whether to enable verbose logging
            logger: Optional logger instance
            user_id: Optional user identifier for context management
        """
        self.verbose = verbose
        self.logger = logger or get_logger(__name__)
        self.user_id = user_id

        # Configure LLM based on provider
        self.llm = self._configure_llm()

        # Initialize core systems
        self.thinking_framework = MultiDimensionalThinking()
        self.dxtag_manager = DxTagManager()
        self.refinement_engine = RefinementEngine()
        self.checkpoint_system = CheckpointSystem()
        self.context_manager = ContextManager()
        self.rate_limiter = RateLimiter(RateLimitConfig())

        # Create crew
        self.crew = self.create_crew()
        self.logger.info("PromptEngineeringCrew initialized")

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
        Creates the prompt engineering crew with specialized agents

        Returns:
            Configured Crew instance
        """
        self.logger.info("Creating prompt engineering crew with specialized agents")

        # Agent 1: Input Analyzer
        # Analyzes raw input using multi-dimensional thinking
        input_analyzer = Agent(
            role='Input Analysis Specialist',
            goal='Analyze user input using logical, analytical, computational, and producer thinking',
            backstory='''You are an expert at understanding user intent and breaking down
            complex requests into structured components. You apply four types of thinking:
            - Logical: cause-effect, contradictions
            - Analytical: breaking into components
            - Computational: structured patterns
            - Producer: end-result focus''',
            verbose=self.verbose,
            llm=self.llm
        )

        # Agent 2: Requirements Clarifier
        # Asks clarifying questions to fill gaps
        requirements_clarifier = Agent(
            role='Requirements Clarification Expert',
            goal='Identify missing information and ask precise clarifying questions',
            backstory='''You are skilled at identifying gaps in requirements and asking
            the right questions to elicit complete information. You ensure prompts have
            clear role definitions, specific constraints, and well-defined output formats.''',
            verbose=self.verbose,
            llm=self.llm
        )

        # Agent 3: Prompt Architect
        # Designs the prompt structure using DxTag pattern
        prompt_architect = Agent(
            role='Prompt Architecture Designer',
            goal='Design well-structured prompts using the DxTag pattern',
            backstory='''You are a master of prompt architecture. You structure prompts
            with clear separation between data, execution logic, and tags. You ensure
            prompts are modular, maintainable, and version-controlled.''',
            verbose=self.verbose,
            llm=self.llm
        )

        # Agent 4: Quality Assurance Specialist
        # Performs the two-iteration refinement
        quality_specialist = Agent(
            role='Prompt Quality Assurance Specialist',
            goal='Refine prompts through iterative quality checks',
            backstory='''You are meticulous about prompt quality. You evaluate prompts
            against professional standards: clarity, specificity, structure, and
            effectiveness. You perform multiple refinement iterations before approval.''',
            verbose=self.verbose,
            llm=self.llm
        )

        # Agent 5: Output Formatter
        # Formats the final prompt in the requested style
        output_formatter = Agent(
            role='Output Formatting Expert',
            goal='Format prompts in the appropriate style for the target audience',
            backstory='''You excel at adapting prompt presentation to different audiences
            and use cases. You can format prompts as structured (detailed sections),
            minimal (concise), or conversational (natural language).''',
            verbose=self.verbose,
            llm=self.llm
        )

        # Create tasks
        tasks = [
            Task(
                description='''Analyze the input: {text}

                Apply multi-dimensional thinking:
                1. Logical analysis - identify cause-effect and contradictions
                2. Analytical breakdown - decompose into components
                3. Computational patterns - identify structured patterns
                4. Producer focus - understand the end goal

                Output a comprehensive analysis covering all four dimensions.''',
                expected_output='''A detailed analysis report with insights from all four thinking modes:
                - Logical insights and recommendations
                - Analytical component breakdown
                - Computational patterns identified
                - Producer/end-result assessment''',
                agent=input_analyzer
            ),
            Task(
                description='''Based on the analysis, identify any missing information and generate
                clarifying questions if needed.

                Consider:
                - Is the role/persona clear?
                - Are constraints specific?
                - Is the output format defined?
                - Is the target audience identified?

                If information is sufficient, state "No clarification needed" and summarize requirements.''',
                expected_output='''Either:
                1. A list of specific clarifying questions, OR
                2. "No clarification needed" with a requirements summary''',
                agent=requirements_clarifier
            ),
            Task(
                description='''Design the prompt structure using the DxTag pattern.

                Create:
                - Data section: role, task, context, examples
                - Execution section: constraints, processing instructions, output format
                - Tags section: metadata, versioning, complexity assessment

                Ensure the prompt is modular and maintainable.''',
                expected_output='''A well-structured prompt design with:
                - Clear role definition
                - Detailed task description
                - Relevant context
                - Specific constraints
                - Defined output format
                - Appropriate metadata''',
                agent=prompt_architect
            ),
            Task(
                description='''Perform quality assurance on the prompt through two refinement iterations.

                For each iteration:
                1. Evaluate against quality criteria (clarity, specificity, structure, etc.)
                2. Identify improvements needed
                3. Apply refinements

                Iteration 1: Focus on major structural improvements
                Iteration 2: Focus on fine-tuning and polish

                Provide the final refined prompt.''',
                expected_output='''The refined prompt after two quality iterations, with:
                - Evaluation scores from both iterations
                - List of improvements applied
                - Final quality assessment''',
                agent=quality_specialist
            ),
            Task(
                description='''Format the final prompt in the appropriate style.

                Choose format based on context:
                - Structured: For technical/professional use (default)
                - Minimal: For quick/simple tasks
                - Conversational: For natural agent interactions

                Ensure the output is polished and ready for immediate use.''',
                expected_output='''The final formatted prompt ready for deployment, presented in
                the appropriate style with clear sections and professional formatting.''',
                agent=output_formatter
            )
        ]

        crew = Crew(
            agents=[
                input_analyzer,
                requirements_clarifier,
                prompt_architect,
                quality_specialist,
                output_formatter
            ],
            tasks=tasks,
            verbose=self.verbose
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
        Processes input through the complete prompt engineering pipeline

        Args:
            text: Raw input text
            style: Output style (structured, minimal, conversational)
            conversation_id: Optional conversation ID for context

        Returns:
            Dictionary with engineered prompt and metadata
        """
        self.logger.info(f"Processing input: {text[:100]}...")

        # Check rate limit
        allowed, reason = self.rate_limiter.check_rate_limit(self.user_id)
        if not allowed:
            self.logger.warning(f"Rate limit exceeded: {reason}")
            return {
                "success": False,
                "error": reason,
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
            # Step 1: Multi-dimensional thinking analysis
            self.logger.info("Step 1: Analyzing input with multi-dimensional thinking")
            thinking_results = self.thinking_framework.analyze_all(text)
            synthesis = self.thinking_framework.synthesize(thinking_results)

            # Create checkpoint after analysis
            self.checkpoint_system.create_checkpoint(
                state={"analysis": synthesis},
                reasoning="Completed multi-dimensional analysis",
                changes=["Applied 4 thinking modes", f"Generated {synthesis['total_insights']} insights"]
            )

            # Step 2: Run CrewAI pipeline
            self.logger.info("Step 2: Running CrewAI agent pipeline")
            crew_result = self.crew.kickoff(inputs={"text": text})

            # Record successful request
            self.rate_limiter.record_request(self.user_id)

            # Extract the final output from crew_result
            final_output = crew_result.raw if hasattr(crew_result, "raw") else str(crew_result)

            # Step 3: Create final checkpoint
            final_state = {
                "original_input": text,
                "analysis": synthesis,
                "final_output": final_output,
                "style": style
            }
            self.checkpoint_system.create_checkpoint(
                state=final_state,
                reasoning="Completed prompt engineering pipeline",
                changes=["Generated final prompt", "Applied quality assurance"]
            )

            # Update context
            if conversation_id:
                self.context_manager.add_message(
                    conversation_id=conversation_id,
                    role="assistant",
                    content=final_output
                )
                self.context_manager.update_current_prompt(
                    conversation_id=conversation_id,
                    prompt_data=final_state
                )

            # Update user profile if user_id is provided
            if self.user_id:
                self.context_manager.record_prompt_creation(
                    user_id=self.user_id,
                    style=style,
                    iterations=2  # Two-iteration refinement
                )

            self.logger.info("Prompt engineering completed successfully")

            return {
                "success": True,
                "prompt": final_output,
                "analysis": synthesis,
                "conversation_id": conversation_id,
                "checkpoints": self.checkpoint_system.list_checkpoints(),
                "rate_limit_stats": self.rate_limiter.get_stats()
            }

        except Exception as e:
            self.logger.error(f"Error in prompt engineering pipeline: {str(e)}", exc_info=True)
            self.rate_limiter.record_failure(self.user_id)

            return {
                "success": False,
                "error": str(e),
                "rate_limit_info": self.rate_limiter.get_stats()
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
