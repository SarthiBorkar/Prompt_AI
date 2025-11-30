"""
Prompt Engineering Crew WITH WEB RESEARCH
Enhanced version with web search capability for research and learning
"""

import os
from crewai import Agent, Crew, Task, LLM
from crewai_tools import SerperDevTool, WebsiteSearchTool
from logging_config import get_logger
from thinking_framework import MultiDimensionalThinking
from dxtag_manager import DxTagManager, PromptComponent
from refinement_engine import RefinementEngine
from checkpoint_system import CheckpointSystem
from context_manager import ContextManager
from rate_limiter import RateLimiter, RateLimitConfig
from typing import Dict, Any, Optional, List
import json


# Try to import DuckDuckGo search (free alternative)
try:
    from duckduckgo_search import DDGS
    DUCKDUCKGO_AVAILABLE = True
except ImportError:
    DUCKDUCKGO_AVAILABLE = False


class PromptEngineeringCrewWithWeb:
    """
    Enhanced prompt engineering crew with web research capability
    """

    def __init__(self, verbose=True, logger=None, user_id: Optional[str] = None, enable_web_research=True):
        """
        Initialize the prompt engineering crew with web research

        Args:
            verbose: Whether to enable verbose logging
            logger: Optional logger instance
            user_id: Optional user identifier for context management
            enable_web_research: Enable web search tools (default: True)
        """
        self.verbose = verbose
        self.logger = logger or get_logger(__name__)
        self.user_id = user_id
        self.enable_web_research = enable_web_research

        # Configure LLM based on provider
        self.llm = self._configure_llm()

        # Initialize core systems
        self.thinking_framework = MultiDimensionalThinking()
        self.dxtag_manager = DxTagManager()
        self.refinement_engine = RefinementEngine()
        self.checkpoint_system = CheckpointSystem()
        self.context_manager = ContextManager()
        self.rate_limiter = RateLimiter(RateLimitConfig())

        # Initialize web tools if enabled
        self.web_tools = self._setup_web_tools() if enable_web_research else []

        # Create crew
        self.crew = self.create_crew()
        self.logger.info(f"PromptEngineeringCrew initialized (Web Research: {enable_web_research})")

    def _configure_llm(self) -> LLM:
        """Configure LLM based on environment variables"""
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

    def _setup_web_tools(self) -> List:
        """Setup web research tools based on available APIs"""
        tools = []

        # Try SerperDev (Google Search) - Most powerful
        serper_api_key = os.getenv("SERPER_API_KEY")
        if serper_api_key and serper_api_key != "your_serper_api_key_here":
            try:
                search_tool = SerperDevTool()
                tools.append(search_tool)
                self.logger.info("✅ SerperDev search tool enabled (Google Search)")
            except Exception as e:
                self.logger.warning(f"Could not initialize SerperDev: {e}")

        # Try DuckDuckGo (Free alternative)
        if DUCKDUCKGO_AVAILABLE and not tools:
            self.logger.info("✅ DuckDuckGo search available (Free)")
            # Note: DuckDuckGo is used directly in agent logic, not as a tool

        # Try WebsiteSearchTool for specific sites
        try:
            # Can search specific domains for best practices, docs, etc.
            website_tool = WebsiteSearchTool()
            tools.append(website_tool)
            self.logger.info("✅ Website search tool enabled")
        except Exception as e:
            self.logger.warning(f"Website search tool not available: {e}")

        if not tools and not DUCKDUCKGO_AVAILABLE:
            self.logger.warning("⚠️  No web search tools available. Install: pip install duckduckgo-search")

        return tools

    def create_crew(self) -> Crew:
        """Creates the prompt engineering crew with specialized agents"""
        self.logger.info("Creating prompt engineering crew with specialized agents")

        # Agent 1: Research Analyst (NEW - with web access)
        research_analyst = Agent(
            role='Research & Context Analyst',
            goal='Research relevant information and gather context using web search when beneficial',
            backstory='''You are a skilled researcher who knows when and how to use web search
            effectively. For current events, technical documentation, and domain-specific knowledge,
            you search the web to gather accurate, up-to-date information. You combine web research
            with analytical thinking to provide comprehensive context.''',
            verbose=self.verbose,
            llm=self.llm,
            tools=self.web_tools  # Web search tools
        )

        # Agent 2: Input Analyzer
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

        # Agent 3: Requirements Clarifier
        requirements_clarifier = Agent(
            role='Requirements Clarification Expert',
            goal='Identify missing information and ask precise clarifying questions',
            backstory='''You are skilled at identifying gaps in requirements and asking
            the right questions to elicit complete information. You ensure prompts have
            clear role definitions, specific constraints, and well-defined output formats.''',
            verbose=self.verbose,
            llm=self.llm
        )

        # Agent 4: Prompt Architect
        prompt_architect = Agent(
            role='Prompt Architecture Designer',
            goal='Design well-structured prompts using the DxTag pattern and research findings',
            backstory='''You are a master of prompt architecture. You structure prompts
            with clear separation between data, execution logic, and tags. You incorporate
            research findings and ensure prompts are modular, maintainable, and version-controlled.''',
            verbose=self.verbose,
            llm=self.llm
        )

        # Agent 5: Quality Assurance Specialist
        quality_specialist = Agent(
            role='Prompt Quality Assurance Specialist',
            goal='Refine prompts through iterative quality checks',
            backstory='''You are meticulous about prompt quality. You evaluate prompts
            against professional standards: clarity, specificity, structure, and
            effectiveness. You perform multiple refinement iterations before approval.''',
            verbose=self.verbose,
            llm=self.llm
        )

        # Agent 6: Output Formatter
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
                description='''Research and gather context for: {text}

                If relevant, use web search to find:
                - Current information and trends
                - Best practices and standards
                - Technical documentation
                - Real-world examples
                - Domain-specific knowledge

                Determine if web research would be beneficial. For general topics, skip web search.
                For current events, technical topics, or domain-specific requests, search the web.

                Provide a research summary with key findings and sources.''',
                expected_output='''Research summary with:
                - Key findings from analysis and/or web research
                - Relevant current information (if searched)
                - Sources and references (if web research was used)
                - Context assessment''',
                agent=research_analyst
            ),
            Task(
                description='''Analyze the input: {text}

                Apply multi-dimensional thinking:
                1. Logical analysis - identify cause-effect and contradictions
                2. Analytical breakdown - decompose into components
                3. Computational patterns - identify structured patterns
                4. Producer focus - understand the end goal

                Consider the research findings provided.

                Output a comprehensive analysis covering all four dimensions.''',
                expected_output='''A detailed analysis report with insights from all four thinking modes:
                - Logical insights and recommendations
                - Analytical component breakdown
                - Computational patterns identified
                - Producer/end-result assessment''',
                agent=input_analyzer
            ),
            Task(
                description='''Based on the analysis and research, identify any missing information
                and generate clarifying questions if needed.

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

                Incorporate research findings and best practices discovered.

                Create:
                - Data section: role, task, context, examples (include research findings)
                - Execution section: constraints, processing instructions, output format
                - Tags section: metadata, versioning, complexity assessment

                Ensure the prompt is modular and maintainable.''',
                expected_output='''A well-structured prompt design with:
                - Clear role definition
                - Detailed task description
                - Relevant context (including research)
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
                research_analyst,
                input_analyzer,
                requirements_clarifier,
                prompt_architect,
                quality_specialist,
                output_formatter
            ],
            tasks=tasks,
            verbose=self.verbose
        )

        self.logger.info("Prompt engineering crew created successfully (6 agents with web research)")
        return crew

    async def process_input(
        self,
        text: str,
        style: str = "structured",
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Processes input through the complete prompt engineering pipeline with web research

        Args:
            text: Raw input text
            style: Output style (structured, minimal, conversational)
            conversation_id: Optional conversation ID for context

        Returns:
            Dictionary with engineered prompt and metadata
        """
        self.logger.info(f"Processing input with web research: {text[:100]}...")

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
            "web_research_enabled": self.enable_web_research,
            "timestamp": self.checkpoint_system.checkpoints.get(
                self.checkpoint_system.current_checkpoint
            ).timestamp if self.checkpoint_system.current_checkpoint else None
        }
        self.checkpoint_system.create_checkpoint(
            state=initial_state,
            reasoning="Starting prompt engineering process with web research",
            changes=["Initial input received"]
        )

        # Create or get conversation context
        if not conversation_id and self.user_id:
            conversation_id = self.context_manager.create_conversation(
                user_id=self.user_id,
                metadata={"style": style, "web_research": self.enable_web_research}
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

            # Step 2: Run CrewAI pipeline with web research
            self.logger.info("Step 2: Running CrewAI agent pipeline with web research")
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
                "style": style,
                "web_research_used": self.enable_web_research
            }
            self.checkpoint_system.create_checkpoint(
                state=final_state,
                reasoning="Completed prompt engineering pipeline with web research",
                changes=["Generated final prompt", "Applied quality assurance", "Incorporated web research"]
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

            self.logger.info("Prompt engineering completed successfully with web research")

            return {
                "success": True,
                "prompt": final_output,
                "analysis": synthesis,
                "conversation_id": conversation_id,
                "checkpoints": self.checkpoint_system.list_checkpoints(),
                "rate_limit_stats": self.rate_limiter.get_stats(),
                "web_research_enabled": self.enable_web_research
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
            "checkpoints": len(self.checkpoint_system.checkpoints),
            "web_research_enabled": self.enable_web_research
        }
