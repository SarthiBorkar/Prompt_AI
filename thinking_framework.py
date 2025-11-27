"""
Thinking Framework Module
Implements the five-step cognitive framework for prompt engineering:
1. Multi-dimensional thinking (logical, analytical, computational, producer)
2. Fundamental framework analysis
3. Checkpoint identification
4. Debugging and transparency
5. Context management
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class ThinkingResult:
    """Result from a thinking operation"""
    thinking_type: str
    analysis: str
    insights: List[str]
    recommendations: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class LogicalThinking:
    """
    Establishes cause-and-effect relationships and identifies contradictions
    """

    @staticmethod
    def analyze(input_text: str, context: Optional[Dict] = None) -> ThinkingResult:
        """
        Analyzes input using logical reasoning

        Args:
            input_text: The raw input to analyze
            context: Optional context from previous interactions

        Returns:
            ThinkingResult with logical analysis
        """
        insights = []
        recommendations = []

        # Analyze for logical structure
        analysis = f"Logical Analysis of: '{input_text[:100]}...'\n\n"

        # Check for clear intent
        if "?" in input_text:
            insights.append("Input contains questions - requires clarification structure")
            recommendations.append("Structure prompt to address each question systematically")
        elif any(word in input_text.lower() for word in ["create", "generate", "write", "make"]):
            insights.append("Input is a creation request - requires clear output specifications")
            recommendations.append("Define explicit success criteria and output format")

        # Check for contradictions
        contradiction_keywords = [("not", "but"), ("however", "although"), ("except", "only")]
        for pair in contradiction_keywords:
            if pair[0] in input_text.lower() and pair[1] in input_text.lower():
                insights.append(f"Potential contradiction detected: '{pair[0]}' and '{pair[1]}'")
                recommendations.append("Clarify relationship between conflicting requirements")

        # Check for completeness
        if len(input_text.split()) < 5:
            insights.append("Input is very brief - likely missing context")
            recommendations.append("Request additional context: target audience, constraints, format")

        analysis += f"Identified {len(insights)} logical patterns\n"
        analysis += f"Generated {len(recommendations)} recommendations"

        return ThinkingResult(
            thinking_type="logical",
            analysis=analysis,
            insights=insights,
            recommendations=recommendations,
            metadata={"word_count": len(input_text.split())}
        )


class AnalyticalThinking:
    """
    Breaks down complex requests into constituent components
    """

    @staticmethod
    def analyze(input_text: str, context: Optional[Dict] = None) -> ThinkingResult:
        """
        Analyzes input by breaking it into components

        Args:
            input_text: The raw input to analyze
            context: Optional context from previous interactions

        Returns:
            ThinkingResult with analytical breakdown
        """
        insights = []
        recommendations = []

        analysis = f"Analytical Breakdown of: '{input_text[:100]}...'\n\n"

        # Identify components
        components = {
            "action": None,
            "subject": None,
            "constraints": [],
            "context": [],
            "output_format": None
        }

        # Extract action verbs
        action_verbs = ["create", "generate", "write", "analyze", "summarize", "explain", "build"]
        for verb in action_verbs:
            if verb in input_text.lower():
                components["action"] = verb
                insights.append(f"Primary action identified: {verb}")
                break

        if not components["action"]:
            insights.append("No clear action verb detected")
            recommendations.append("Add explicit action verb (e.g., 'create', 'analyze', 'generate')")

        # Check for constraints
        constraint_indicators = ["must", "should", "cannot", "within", "limit", "maximum", "minimum"]
        for indicator in constraint_indicators:
            if indicator in input_text.lower():
                components["constraints"].append(indicator)
                insights.append(f"Constraint indicator found: '{indicator}'")

        if not components["constraints"]:
            recommendations.append("Consider adding explicit constraints or requirements")

        # Check for context clues
        context_indicators = ["for", "about", "regarding", "concerning", "in the context of"]
        for indicator in context_indicators:
            if indicator in input_text.lower():
                components["context"].append(indicator)

        # Check for output format specifications
        format_indicators = ["format", "style", "structure", "template", "json", "markdown"]
        for indicator in format_indicators:
            if indicator in input_text.lower():
                components["output_format"] = indicator
                insights.append(f"Output format specified: {indicator}")

        if not components["output_format"]:
            recommendations.append("Specify desired output format (e.g., JSON, markdown, plain text)")

        analysis += f"Components identified: {len([v for v in components.values() if v])}/5\n"
        analysis += f"Completeness score: {(len([v for v in components.values() if v]) / 5) * 100:.0f}%"

        return ThinkingResult(
            thinking_type="analytical",
            analysis=analysis,
            insights=insights,
            recommendations=recommendations,
            metadata={"components": components}
        )


class ComputationalThinking:
    """
    Translates abstract concepts into structured, executable patterns
    """

    @staticmethod
    def analyze(input_text: str, context: Optional[Dict] = None) -> ThinkingResult:
        """
        Analyzes input for computational structure

        Args:
            input_text: The raw input to analyze
            context: Optional context from previous interactions

        Returns:
            ThinkingResult with computational analysis
        """
        insights = []
        recommendations = []

        analysis = f"Computational Analysis of: '{input_text[:100]}...'\n\n"

        # Identify computational patterns
        patterns = {
            "sequential": False,
            "conditional": False,
            "iterative": False,
            "parallel": False
        }

        # Check for sequential processing
        sequential_indicators = ["first", "then", "next", "finally", "step"]
        if any(ind in input_text.lower() for ind in sequential_indicators):
            patterns["sequential"] = True
            insights.append("Sequential processing pattern detected")
            recommendations.append("Structure prompt with clear step-by-step instructions")

        # Check for conditional logic
        conditional_indicators = ["if", "when", "unless", "in case", "depending on"]
        if any(ind in input_text.lower() for ind in conditional_indicators):
            patterns["conditional"] = True
            insights.append("Conditional logic detected")
            recommendations.append("Clearly define all conditional branches and edge cases")

        # Check for iteration
        iterative_indicators = ["each", "every", "all", "multiple", "repeat", "loop"]
        if any(ind in input_text.lower() for ind in iterative_indicators):
            patterns["iterative"] = True
            insights.append("Iterative processing pattern detected")
            recommendations.append("Specify iteration criteria and termination conditions")

        # Check for parallel processing
        parallel_indicators = ["simultaneously", "at the same time", "parallel", "concurrent"]
        if any(ind in input_text.lower() for ind in parallel_indicators):
            patterns["parallel"] = True
            insights.append("Parallel processing pattern detected")
            recommendations.append("Define dependencies and synchronization points")

        # Assess algorithmic complexity
        complexity = "low"
        active_patterns = sum(patterns.values())
        if active_patterns >= 3:
            complexity = "high"
            recommendations.append("Consider breaking into multiple sub-prompts for clarity")
        elif active_patterns >= 2:
            complexity = "medium"

        analysis += f"Computational patterns: {active_patterns}/4 active\n"
        analysis += f"Algorithmic complexity: {complexity}"

        return ThinkingResult(
            thinking_type="computational",
            analysis=analysis,
            insights=insights,
            recommendations=recommendations,
            metadata={"patterns": patterns, "complexity": complexity}
        )


class ProducerThinking:
    """
    Focuses on practical end results and consumption patterns
    """

    @staticmethod
    def analyze(input_text: str, context: Optional[Dict] = None) -> ThinkingResult:
        """
        Analyzes input for end-result focus

        Args:
            input_text: The raw input to analyze
            context: Optional context from previous interactions

        Returns:
            ThinkingResult with producer analysis
        """
        insights = []
        recommendations = []

        analysis = f"Producer Analysis of: '{input_text[:100]}...'\n\n"

        # Identify output characteristics
        output_analysis = {
            "target_audience": None,
            "use_case": None,
            "success_metrics": [],
            "consumption_method": None
        }

        # Check for target audience
        audience_indicators = ["for users", "for developers", "for customers", "for agents", "audience"]
        for indicator in audience_indicators:
            if indicator in input_text.lower():
                output_analysis["target_audience"] = indicator
                insights.append(f"Target audience identified: {indicator}")
                break

        if not output_analysis["target_audience"]:
            recommendations.append("Specify target audience for the output")

        # Check for use case
        use_case_indicators = ["to help", "to enable", "to solve", "for the purpose of"]
        for indicator in use_case_indicators:
            if indicator in input_text.lower():
                output_analysis["use_case"] = indicator
                insights.append(f"Use case identified: {indicator}")
                break

        # Check for success metrics
        metric_indicators = ["accurate", "fast", "comprehensive", "concise", "clear", "detailed"]
        for indicator in metric_indicators:
            if indicator in input_text.lower():
                output_analysis["success_metrics"].append(indicator)

        if output_analysis["success_metrics"]:
            insights.append(f"Success metrics: {', '.join(output_analysis['success_metrics'])}")
        else:
            recommendations.append("Define success criteria (e.g., accuracy, speed, comprehensiveness)")

        # Check for consumption method
        consumption_indicators = ["api", "command line", "web", "mobile", "agent-to-agent"]
        for indicator in consumption_indicators:
            if indicator in input_text.lower():
                output_analysis["consumption_method"] = indicator
                insights.append(f"Consumption method: {indicator}")
                break

        # Assess practical viability
        viability_score = sum([
            1 if output_analysis["target_audience"] else 0,
            1 if output_analysis["use_case"] else 0,
            1 if output_analysis["success_metrics"] else 0,
            1 if output_analysis["consumption_method"] else 0
        ]) / 4

        if viability_score < 0.5:
            recommendations.append("Add more details about intended use and success criteria")

        analysis += f"Output specification completeness: {viability_score*100:.0f}%\n"
        analysis += f"Production readiness: {'High' if viability_score >= 0.75 else 'Medium' if viability_score >= 0.5 else 'Low'}"

        return ThinkingResult(
            thinking_type="producer",
            analysis=analysis,
            insights=insights,
            recommendations=recommendations,
            metadata={"output_analysis": output_analysis, "viability_score": viability_score}
        )


class MultiDimensionalThinking:
    """
    Orchestrates all four thinking modes in parallel
    """

    def __init__(self):
        self.logical = LogicalThinking()
        self.analytical = AnalyticalThinking()
        self.computational = ComputationalThinking()
        self.producer = ProducerThinking()

    def analyze_all(self, input_text: str, context: Optional[Dict] = None) -> Dict[str, ThinkingResult]:
        """
        Runs all four thinking modes in parallel

        Args:
            input_text: The raw input to analyze
            context: Optional context from previous interactions

        Returns:
            Dictionary mapping thinking type to results
        """
        results = {
            "logical": self.logical.analyze(input_text, context),
            "analytical": self.analytical.analyze(input_text, context),
            "computational": self.computational.analyze(input_text, context),
            "producer": self.producer.analyze(input_text, context)
        }

        return results

    def synthesize(self, results: Dict[str, ThinkingResult]) -> Dict[str, Any]:
        """
        Synthesizes insights from all thinking modes

        Args:
            results: Dictionary of thinking results

        Returns:
            Synthesized analysis with combined insights
        """
        all_insights = []
        all_recommendations = []

        for thinking_type, result in results.items():
            all_insights.extend([f"[{thinking_type.upper()}] {i}" for i in result.insights])
            all_recommendations.extend([f"[{thinking_type.upper()}] {r}" for r in result.recommendations])

        return {
            "total_insights": len(all_insights),
            "total_recommendations": len(all_recommendations),
            "insights": all_insights,
            "recommendations": all_recommendations,
            "timestamp": datetime.now().isoformat()
        }
