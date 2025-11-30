"""
Prompt Engineering Crew
Implements the complete prompt engineering pipeline with specialized agents
Enhanced with: Advanced Techniques, Expert Knowledge, Quality Scoring, Continuous Learning
"""

import os
import time
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

# Import enhancement modules
from advanced_techniques import AdvancedPromptingTechniques
from expert_knowledge_base import ExpertKnowledgeBase
from prompt_evaluator import PromptEvaluator
from continuous_learning import ContinuousLearningSystem

# Import web search tools (optional)
try:
    from crewai_tools import SerperDevTool, ScrapeWebsiteTool
    WEB_TOOLS_AVAILABLE = True
except ImportError:
    WEB_TOOLS_AVAILABLE = False
    SerperDevTool = None
    ScrapeWebsiteTool = None


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

        # Initialize enhancement systems
        self.advanced_techniques = AdvancedPromptingTechniques()
        self.expert_knowledge = ExpertKnowledgeBase()
        self.prompt_evaluator = PromptEvaluator()
        self.continuous_learning = ContinuousLearningSystem()

        # Check if web research is enabled
        self.web_research_enabled = os.getenv("ENABLE_WEB_RESEARCH", "false").lower() == "true"
        self.web_tools = None

        if self.web_research_enabled:
            if WEB_TOOLS_AVAILABLE:
                try:
                    # Initialize web search tool (SerperDev or fallback)
                    serper_api_key = os.getenv("SERPER_API_KEY")
                    if serper_api_key and serper_api_key != "your_serper_api_key_here":
                        self.web_tools = [SerperDevTool(), ScrapeWebsiteTool()]
                        self.logger.info("Web research enabled with SerperDev (Google Search)")
                    else:
                        # Try DuckDuckGo as fallback
                        try:
                            from crewai_tools import tool
                            from duckduckgo_search import DDGS

                            @tool("DuckDuckGo Search")
                            def search_tool(query: str) -> str:
                                """Search the web using DuckDuckGo"""
                                try:
                                    results = DDGS().text(query, max_results=5)
                                    return str(results)
                                except Exception as e:
                                    return f"Search failed: {str(e)}"

                            self.web_tools = [search_tool]
                            self.logger.info("Web research enabled with DuckDuckGo Search (free)")
                        except ImportError:
                            self.logger.warning("DuckDuckGo search not available. Install with: pip install duckduckgo-search")
                            self.web_research_enabled = False
                except Exception as e:
                    self.logger.warning(f"Failed to initialize web tools: {e}")
                    self.web_research_enabled = False
            else:
                self.logger.warning("Web tools not available. Install with: pip install 'crewai[tools]'")
                self.web_research_enabled = False

        # Create crew
        self.crew = self.create_crew()
        features = "advanced enhancements"
        if self.web_research_enabled:
            features += " + web research"
        self.logger.info(f"PromptEngineeringCrew initialized with {features}")

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

        # Agent 6: Research Analyst (Optional - if web research enabled)
        research_analyst = None
        if self.web_research_enabled and self.web_tools:
            research_analyst = Agent(
                role='Research Analyst',
                goal='Research latest information and trends related to the user request',
                backstory='''You are a research specialist who finds up-to-date information
                from the web. You search for current documentation, trends, best practices,
                and real-world examples. You provide factual, verified information to enhance
                prompt engineering with the latest knowledge.''',
                verbose=self.verbose,
                llm=self.llm,
                tools=self.web_tools
            )

        # Create tasks
        tasks = []

        # Task 0: Web Research (if enabled)
        if research_analyst:
            tasks.append(Task(
                description='''Research the following topic using web search: {text}

                Find:
                1. Latest documentation and official sources
                2. Current trends and developments
                3. Best practices and expert recommendations
                4. Real-world examples and use cases
                5. Technical specifications and requirements (if applicable)

                Provide factual, up-to-date information with sources.
                If the topic is new or specific, verify it exists before making assumptions.''',
                expected_output='''A comprehensive research report with:
                - Summary of findings
                - Key facts and specifications
                - Sources and references
                - Current trends and developments
                - Note if information is not found or topic doesn't exist''',
                agent=research_analyst
            ))

        # Original tasks
        tasks += [
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

        # Build agents list
        agents_list = []
        if research_analyst:
            agents_list.append(research_analyst)
        agents_list.extend([
            input_analyzer,
            requirements_clarifier,
            prompt_architect,
            quality_specialist,
            output_formatter
        ])

        crew = Crew(
            agents=agents_list,
            tasks=tasks,
            verbose=self.verbose
        )

        agent_count = len(agents_list)
        self.logger.info(f"Prompt engineering crew created successfully with {agent_count} agents")
        return crew

    async def process_input(
        self,
        text: str,
        style: str = "structured",
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Processes input through the complete prompt engineering pipeline
        Enhanced with advanced techniques, expert knowledge, quality scoring, and continuous learning

        Args:
            text: Raw input text
            style: Output style (structured, minimal, conversational)
            conversation_id: Optional conversation ID for context

        Returns:
            Dictionary with engineered prompt, quality scores, and learning insights
        """
        self.logger.info(f"Processing input with enhancements: {text[:100]}...")
        start_time = time.time()

        # Check rate limit
        allowed, reason = self.rate_limiter.check_rate_limit(self.user_id)
        if not allowed:
            self.logger.warning(f"Rate limit exceeded: {reason}")
            return {
                "success": False,
                "error": reason,
                "rate_limit_info": self.rate_limiter.get_stats()
            }

        # Step 0: Get technique recommendations from learning system
        self.logger.info("Step 0: Getting technique recommendations from learning history")
        recommended_techniques = self.continuous_learning.get_recommended_techniques(text)
        self.logger.info(f"Recommended techniques: {recommended_techniques}")

        # Get expert knowledge recommendations
        expert_recommendations = self.expert_knowledge.get_recommendations_for_task(text)
        self.logger.info(f"Got {len(expert_recommendations)} expert recommendations")

        # Create checkpoint at start
        initial_state = {
            "text": text,
            "style": style,
            "recommended_techniques": recommended_techniques,
            "expert_recommendations_count": len(expert_recommendations),
            "timestamp": self.checkpoint_system.checkpoints.get(
                self.checkpoint_system.current_checkpoint
            ).timestamp if self.checkpoint_system.current_checkpoint else None
        }
        self.checkpoint_system.create_checkpoint(
            state=initial_state,
            reasoning="Starting enhanced prompt engineering process",
            changes=[
                "Initial input received",
                f"Recommended {len(recommended_techniques)} techniques",
                f"Retrieved {len(expert_recommendations)} expert practices"
            ]
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

            # Step 2: Apply advanced techniques (if recommended)
            enhanced_context = text
            techniques_applied = []

            if recommended_techniques:
                self.logger.info(f"Step 2a: Applying recommended techniques: {recommended_techniques}")
                # Apply first recommended technique
                primary_technique = recommended_techniques[0]
                technique_info = self.advanced_techniques.get_technique_info(primary_technique)
                if technique_info:
                    techniques_applied.append(primary_technique)
                    self.logger.info(f"Applied technique: {technique_info.name}")

            # Build expert guidance summary
            expert_guidance = ""
            if expert_recommendations:
                expert_guidance = "\n\n# EXPERT BEST PRACTICES:\n"
                for rec in expert_recommendations[:3]:  # Top 3 recommendations
                    expert_guidance += f"\n## {rec.title} ({rec.source})\n"
                    expert_guidance += f"{rec.description}\n"
                    expert_guidance += f"DO: {', '.join(rec.do_this[:2])}\n"
                    expert_guidance += f"AVOID: {', '.join(rec.avoid_this[:2])}\n"

            # Step 3: Run CrewAI pipeline with enhanced context
            self.logger.info("Step 3: Running enhanced CrewAI agent pipeline")
            enhanced_input = {
                "text": text,
                "techniques_context": f"Recommended techniques: {', '.join(recommended_techniques)}" if recommended_techniques else "",
                "expert_guidance": expert_guidance
            }
            crew_result = self.crew.kickoff(inputs={"text": f"{text}\n{expert_guidance}"})

            # Record successful request
            self.rate_limiter.record_request(self.user_id)

            # Extract the final output from crew_result
            final_output = crew_result.raw if hasattr(crew_result, "raw") else str(crew_result)

            # Step 4: Evaluate prompt quality
            self.logger.info("Step 4: Evaluating prompt quality")
            quality_score = self.prompt_evaluator.evaluate(final_output, context=text)
            self.logger.info(f"Quality Score: {quality_score.overall_score}/100 (Grade: {quality_score.get_grade()})")
            self.logger.info(f"Agent-Ready Score: {quality_score.agent_ready_score}/100")

            # Step 5: Record in continuous learning system
            processing_time = time.time() - start_time
            self.logger.info("Step 5: Recording interaction for continuous learning")

            # Add techniques that were actually used
            all_techniques_used = techniques_applied + recommended_techniques[:3]  # Track top 3 recommended
            all_techniques_used = list(set(all_techniques_used))  # Remove duplicates

            self.continuous_learning.record_interaction(
                input_description=text[:200],  # First 200 chars
                techniques_used=all_techniques_used,
                quality_score=quality_score.overall_score,
                success=True,
                time_taken=processing_time,
                token_count=quality_score.token_count,
                checkpoint_id=self.checkpoint_system.current_checkpoint
            )

            # Get performance trend
            performance_trend = self.continuous_learning.get_performance_trend()

            # Step 6: Create final checkpoint
            final_state = {
                "original_input": text,
                "analysis": synthesis,
                "final_output": final_output,
                "style": style,
                "techniques_used": all_techniques_used,
                "quality_score": quality_score.overall_score,
                "quality_grade": quality_score.get_grade(),
                "agent_ready_score": quality_score.agent_ready_score,
                "processing_time": processing_time
            }
            self.checkpoint_system.create_checkpoint(
                state=final_state,
                reasoning="Completed enhanced prompt engineering pipeline",
                changes=[
                    "Generated final prompt",
                    "Applied quality assurance",
                    f"Quality score: {quality_score.overall_score}/100",
                    f"Techniques used: {', '.join(all_techniques_used)}",
                    "Recorded in learning system"
                ]
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

            self.logger.info("Enhanced prompt engineering completed successfully")

            return {
                "success": True,
                "prompt": final_output,
                "analysis": synthesis,
                "quality_evaluation": {
                    "overall_score": quality_score.overall_score,
                    "grade": quality_score.get_grade(),
                    "clarity_score": quality_score.clarity_score,
                    "specificity_score": quality_score.specificity_score,
                    "completeness_score": quality_score.completeness_score,
                    "structure_score": quality_score.structure_score,
                    "efficiency_score": quality_score.efficiency_score,
                    "agent_ready_score": quality_score.agent_ready_score,
                    "strengths": quality_score.strengths,
                    "improvements": quality_score.improvements,
                    "token_count": quality_score.token_count,
                    "estimated_cost": quality_score.estimated_cost
                },
                "techniques_used": all_techniques_used,
                "expert_recommendations_count": len(expert_recommendations),
                "learning_insights": {
                    "performance_trend": performance_trend,
                    "recommended_techniques": recommended_techniques,
                    "processing_time": round(processing_time, 2)
                },
                "conversation_id": conversation_id,
                "checkpoints": self.checkpoint_system.list_checkpoints(),
                "rate_limit_stats": self.rate_limiter.get_stats()
            }

        except Exception as e:
            self.logger.error(f"Error in prompt engineering pipeline: {str(e)}", exc_info=True)
            self.rate_limiter.record_failure(self.user_id)

            # Record failure in learning system
            processing_time = time.time() - start_time
            self.continuous_learning.record_interaction(
                input_description=text[:200],
                techniques_used=recommended_techniques[:3] if recommended_techniques else [],
                quality_score=0,
                success=False,
                time_taken=processing_time,
                token_count=0,
                checkpoint_id=self.checkpoint_system.current_checkpoint
            )

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
        """Gets comprehensive statistics including learning insights"""
        return {
            "context": self.context_manager.get_statistics(),
            "rate_limiter": self.rate_limiter.get_stats(),
            "refinement": self.refinement_engine.get_refinement_stats(),
            "checkpoints": len(self.checkpoint_system.checkpoints),
            "learning": {
                "performance_trend": self.continuous_learning.get_performance_trend(),
                "total_interactions": len(self.continuous_learning.records)
            }
        }

    def get_learning_insights(self) -> Dict[str, Any]:
        """Gets insights from continuous learning system"""
        return self.continuous_learning.get_insights()

    def get_performance_trend(self) -> Dict[str, Any]:
        """Gets performance trend from learning system"""
        return self.continuous_learning.get_performance_trend()

    def get_learning_summary(self) -> str:
        """Gets human-readable learning summary"""
        return self.continuous_learning.export_learning_summary()

    def get_available_techniques(self) -> List[Dict[str, Any]]:
        """Gets list of all available prompting techniques"""
        return [
            {
                "name": technique.name,
                "description": technique.description,
                "use_cases": technique.use_cases
            }
            for technique in self.advanced_techniques.get_all_techniques()
        ]

    def get_expert_knowledge(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Gets expert knowledge recommendations"""
        practices = self.expert_knowledge.query(category=category)
        return [
            {
                "source": practice.source,
                "category": practice.category,
                "title": practice.title,
                "description": practice.description,
                "do_this": practice.do_this,
                "avoid_this": practice.avoid_this
            }
            for practice in practices
        ]

    def evaluate_prompt(self, prompt: str, context: Optional[str] = None) -> Dict[str, Any]:
        """Evaluates a prompt and returns quality scores"""
        score = self.prompt_evaluator.evaluate(prompt, context)
        return {
            "overall_score": score.overall_score,
            "grade": score.get_grade(),
            "scores": {
                "clarity": score.clarity_score,
                "specificity": score.specificity_score,
                "completeness": score.completeness_score,
                "structure": score.structure_score,
                "efficiency": score.efficiency_score,
                "agent_ready": score.agent_ready_score
            },
            "strengths": score.strengths,
            "improvements": score.improvements,
            "token_count": score.token_count,
            "estimated_cost": score.estimated_cost
        }
