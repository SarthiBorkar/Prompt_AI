"""
Prompt Evaluation & Scoring System
Objectively measures prompt quality across multiple dimensions
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import re
import json


@dataclass
class PromptScore:
    """Comprehensive prompt quality scores"""
    clarity_score: float  # 0-100
    specificity_score: float  # 0-100
    completeness_score: float  # 0-100
    structure_score: float  # 0-100
    efficiency_score: float  # 0-100
    agent_ready_score: float  # 0-100 (for agent-to-agent)
    overall_score: float  # 0-100

    # Detailed feedback
    strengths: List[str]
    improvements: List[str]
    token_count: int
    estimated_cost: float  # In cents

    def to_dict(self) -> Dict:
        return asdict(self)

    def get_grade(self) -> str:
        """Convert score to letter grade"""
        if self.overall_score >= 90:
            return "A"
        elif self.overall_score >= 80:
            return "B"
        elif self.overall_score >= 70:
            return "C"
        elif self.overall_score >= 60:
            return "D"
        else:
            return "F"


class PromptEvaluator:
    """
    Evaluates prompt quality across multiple dimensions
    Provides objective scoring and improvement suggestions
    """

    def __init__(self, model: str = "gpt-4"):
        """
        Initialize evaluator

        Args:
            model: LLM model for token/cost estimation
        """
        self.model = model
        self.token_costs = {
            "gpt-4": {"input": 0.03, "output": 0.06},  # per 1K tokens
            "gpt-3.5-turbo": {"input": 0.001, "output": 0.002},
            "claude-3-opus": {"input": 0.015, "output": 0.075},
            "claude-3-sonnet": {"input": 0.003, "output": 0.015},
            "llama-3-70b": {"input": 0.001, "output": 0.001},  # via Groq
        }

    def evaluate(self, prompt: str, context: Optional[str] = None) -> PromptScore:
        """
        Comprehensive evaluation of a prompt

        Args:
            prompt: The prompt to evaluate
            context: Optional context about the prompt's purpose

        Returns:
            PromptScore with detailed metrics
        """
        # Calculate individual scores
        clarity_score = self._evaluate_clarity(prompt)
        specificity_score = self._evaluate_specificity(prompt)
        completeness_score = self._evaluate_completeness(prompt)
        structure_score = self._evaluate_structure(prompt)
        efficiency_score = self._evaluate_efficiency(prompt)
        agent_ready_score = self._evaluate_agent_readiness(prompt)

        # Calculate overall score (weighted average)
        weights = {
            "clarity": 0.20,
            "specificity": 0.20,
            "completeness": 0.15,
            "structure": 0.15,
            "efficiency": 0.15,
            "agent_ready": 0.15
        }

        overall_score = (
            clarity_score * weights["clarity"] +
            specificity_score * weights["specificity"] +
            completeness_score * weights["completeness"] +
            structure_score * weights["structure"] +
            efficiency_score * weights["efficiency"] +
            agent_ready_score * weights["agent_ready"]
        )

        # Generate feedback
        strengths = self._identify_strengths(prompt, {
            "clarity": clarity_score,
            "specificity": specificity_score,
            "completeness": completeness_score,
            "structure": structure_score,
            "efficiency": efficiency_score,
            "agent_ready": agent_ready_score
        })

        improvements = self._suggest_improvements(prompt, {
            "clarity": clarity_score,
            "specificity": specificity_score,
            "completeness": completeness_score,
            "structure": structure_score,
            "efficiency": efficiency_score,
            "agent_ready": agent_ready_score
        })

        # Token estimation
        token_count = self._estimate_tokens(prompt)
        estimated_cost = self._estimate_cost(token_count)

        return PromptScore(
            clarity_score=round(clarity_score, 1),
            specificity_score=round(specificity_score, 1),
            completeness_score=round(completeness_score, 1),
            structure_score=round(structure_score, 1),
            efficiency_score=round(efficiency_score, 1),
            agent_ready_score=round(agent_ready_score, 1),
            overall_score=round(overall_score, 1),
            strengths=strengths,
            improvements=improvements,
            token_count=token_count,
            estimated_cost=estimated_cost
        )

    def _evaluate_clarity(self, prompt: str) -> float:
        """Evaluate clarity of instructions (0-100)"""
        score = 100.0

        # Check for clear instruction verbs
        instruction_verbs = ["analyze", "extract", "summarize", "classify", "generate",
                           "identify", "evaluate", "compare", "explain", "create"]
        has_instruction = any(verb in prompt.lower() for verb in instruction_verbs)
        if not has_instruction:
            score -= 20

        # Check for ambiguous words
        ambiguous_words = ["stuff", "things", "it", "that", "this", "something", "maybe", "probably"]
        ambiguity_count = sum(1 for word in ambiguous_words if word in prompt.lower())
        score -= min(ambiguity_count * 5, 25)

        # Check for complex nested sentences
        sentence_count = prompt.count('.') + prompt.count('!') + prompt.count('?')
        avg_sentence_length = len(prompt.split()) / max(sentence_count, 1)
        if avg_sentence_length > 40:
            score -= 15

        # Check for defined terms
        has_definitions = any(marker in prompt.lower() for marker in ["means", "defined as", "refers to"])
        if has_definitions:
            score += 5

        return max(0, min(100, score))

    def _evaluate_specificity(self, prompt: str) -> float:
        """Evaluate specificity of requirements (0-100)"""
        score = 100.0

        # Check for output format specification
        has_format = any(marker in prompt.lower() for marker in
                        ["json", "xml", "format:", "output:", "return:", "structure:"])
        if not has_format:
            score -= 25

        # Check for examples
        has_examples = any(marker in prompt.lower() for marker in
                          ["example:", "e.g.", "for instance", "such as"])
        if not has_examples:
            score -= 15

        # Check for constraints
        has_constraints = any(marker in prompt.lower() for marker in
                             ["must", "required", "should", "do not", "avoid", "limit"])
        if not has_constraints:
            score -= 20

        # Check for vague quantities
        vague_quantities = ["some", "few", "many", "several", "various"]
        vagueness_count = sum(1 for word in vague_quantities if word in prompt.lower())
        score -= vagueness_count * 5

        # Bonus for specific numbers
        has_numbers = bool(re.search(r'\d+', prompt))
        if has_numbers:
            score += 10

        return max(0, min(100, score))

    def _evaluate_completeness(self, prompt: str) -> float:
        """Evaluate completeness of prompt (0-100)"""
        score = 100.0

        components = {
            "role": ["you are", "acting as", "role:", "as a"],
            "task": ["task:", "objective:", "goal:", "do the following"],
            "context": ["context:", "background:", "given that", "considering"],
            "constraints": ["constraint:", "limitation:", "do not", "must not"],
            "output": ["output:", "return:", "provide:", "format:"],
            "examples": ["example:", "e.g.", "for instance"]
        }

        present_components = 0
        for component, markers in components.items():
            if any(marker in prompt.lower() for marker in markers):
                present_components += 1

        # Each component is worth points
        score = (present_components / len(components)) * 100

        # Bonus for comprehensive prompts
        if present_components >= 5:
            score += 10

        return min(100, score)

    def _evaluate_structure(self, prompt: str) -> float:
        """Evaluate prompt structure and organization (0-100)"""
        score = 100.0

        # Check for sections/headers
        has_headers = bool(re.search(r'#{1,3}\s+\w+|[A-Z\s]+:', prompt))
        if not has_headers:
            score -= 20

        # Check for numbered lists
        has_numbered_list = bool(re.search(r'\d+\.\s+\w+', prompt))
        if has_numbered_list:
            score += 10

        # Check for bullet points
        has_bullets = bool(re.search(r'[-*]\s+\w+', prompt))
        if has_bullets:
            score += 5

        # Check for separators/delimiters
        has_separators = any(sep in prompt for sep in ['"""', "'''", "---", "===", "```"])
        if has_separators:
            score += 10

        # Penalize wall-of-text
        lines = prompt.split('\n')
        non_empty_lines = [l for l in lines if l.strip()]
        if non_empty_lines and len(max(non_empty_lines, key=len)) > 150:
            score -= 15

        # Bonus for clear hierarchy
        if has_headers and (has_numbered_list or has_bullets):
            score += 10

        return max(0, min(100, score))

    def _evaluate_efficiency(self, prompt: str) -> float:
        """Evaluate token efficiency (0-100)"""
        score = 100.0

        # Penalize excessive length
        word_count = len(prompt.split())
        if word_count > 500:
            score -= 20
        elif word_count > 300:
            score -= 10

        # Penalize repetition
        words = prompt.lower().split()
        unique_ratio = len(set(words)) / len(words) if words else 1
        if unique_ratio < 0.5:
            score -= 20
        elif unique_ratio < 0.7:
            score -= 10

        # Penalize excessive examples
        example_count = prompt.lower().count("example")
        if example_count > 5:
            score -= 15

        # Bonus for concise but complete
        if 50 < word_count < 200 and self._evaluate_completeness(prompt) > 70:
            score += 15

        return max(0, min(100, score))

    def _evaluate_agent_readiness(self, prompt: str) -> float:
        """Evaluate readiness for agent-to-agent communication (0-100)"""
        score = 100.0

        # Check for structured format (JSON/XML)
        has_json = "json" in prompt.lower() or bool(re.search(r'\{[^}]*\}', prompt))
        if not has_json:
            score -= 25

        # Check for error handling
        has_error_handling = any(marker in prompt.lower() for marker in
                                ["error", "invalid", "failure", "exception", "if.*not"])
        if not has_error_handling:
            score -= 20

        # Check for validation rules
        has_validation = any(marker in prompt.lower() for marker in
                           ["valid", "validate", "check", "verify", "ensure"])
        if has_validation:
            score += 10

        # Check for type definitions
        has_types = any(marker in prompt.lower() for marker in
                       ["string", "number", "boolean", "array", "object", "type:"])
        if has_types:
            score += 15

        # Check for agent communication patterns
        agent_markers = ["agent", "from:", "to:", "message", "protocol", "request", "response"]
        agent_count = sum(1 for marker in agent_markers if marker in prompt.lower())
        if agent_count >= 3:
            score += 15

        return max(0, min(100, score))

    def _identify_strengths(self, prompt: str, scores: Dict[str, float]) -> List[str]:
        """Identify prompt strengths"""
        strengths = []

        if scores["clarity"] >= 80:
            strengths.append("Clear and unambiguous instructions")

        if scores["specificity"] >= 80:
            strengths.append("Well-defined output format and constraints")

        if scores["completeness"] >= 80:
            strengths.append("Comprehensive coverage of all key components")

        if scores["structure"] >= 80:
            strengths.append("Well-organized with clear hierarchy")

        if scores["efficiency"] >= 80:
            strengths.append("Concise and token-efficient")

        if scores["agent_ready"] >= 80:
            strengths.append("Ready for agent-to-agent communication")

        # Specific patterns
        if "json" in prompt.lower():
            strengths.append("Uses structured JSON format")

        if any(marker in prompt.lower() for marker in ["example:", "e.g."]):
            strengths.append("Includes helpful examples")

        return strengths if strengths else ["Prompt is functional"]

    def _suggest_improvements(self, prompt: str, scores: Dict[str, float]) -> List[str]:
        """Suggest specific improvements"""
        improvements = []

        if scores["clarity"] < 70:
            improvements.append("Add clearer instruction verbs (analyze, extract, summarize, etc.)")
            improvements.append("Remove ambiguous words (it, that, stuff, things)")

        if scores["specificity"] < 70:
            improvements.append("Specify exact output format (preferably JSON schema)")
            improvements.append("Add concrete examples of expected output")
            improvements.append("Define precise constraints and requirements")

        if scores["completeness"] < 70:
            improvements.append("Add missing components: role, task, context, constraints, format")

        if scores["structure"] < 70:
            improvements.append("Organize with clear sections/headers")
            improvements.append("Use numbered lists for sequential steps")
            improvements.append("Add visual separators for different sections")

        if scores["efficiency"] < 70:
            improvements.append("Remove redundant or repetitive text")
            improvements.append("Consolidate multiple examples if excessive")

        if scores["agent_ready"] < 70:
            improvements.append("Add JSON schema for structured communication")
            improvements.append("Define error handling behavior")
            improvements.append("Specify validation rules")
            improvements.append("Add type definitions for all fields")

        return improvements if improvements else ["Prompt is excellent - no major improvements needed"]

    def _estimate_tokens(self, prompt: str) -> int:
        """Rough token count estimation"""
        # Rough approximation: 1 token ≈ 4 characters for English
        return int(len(prompt) / 4)

    def _estimate_cost(self, token_count: int) -> float:
        """Estimate cost in cents"""
        if self.model in self.token_costs:
            cost_per_1k = self.token_costs[self.model]["input"]
            return (token_count / 1000) * cost_per_1k
        return 0.0

    def compare_prompts(self, prompt1: str, prompt2: str) -> Dict:
        """Compare two prompts and recommend the better one"""
        score1 = self.evaluate(prompt1)
        score2 = self.evaluate(prompt2)

        return {
            "prompt1": {
                "score": score1.overall_score,
                "grade": score1.get_grade(),
                "strengths": score1.strengths[:3],
                "tokens": score1.token_count
            },
            "prompt2": {
                "score": score2.overall_score,
                "grade": score2.get_grade(),
                "strengths": score2.strengths[:3],
                "tokens": score2.token_count
            },
            "recommendation": "prompt1" if score1.overall_score > score2.overall_score else "prompt2",
            "score_difference": abs(score1.overall_score - score2.overall_score)
        }

    def generate_report(self, prompt: str) -> str:
        """Generate a formatted evaluation report"""
        score = self.evaluate(prompt)

        report = f"""
# PROMPT EVALUATION REPORT

## Overall Score: {score.overall_score}/100 (Grade: {score.get_grade()})

## Detailed Scores:
- Clarity: {score.clarity_score}/100
- Specificity: {score.specificity_score}/100
- Completeness: {score.completeness_score}/100
- Structure: {score.structure_score}/100
- Efficiency: {score.efficiency_score}/100
- Agent-Ready: {score.agent_ready_score}/100

## Strengths:
{chr(10).join(f'✓ {s}' for s in score.strengths)}

## Suggested Improvements:
{chr(10).join(f'• {i}' for i in score.improvements)}

## Resource Estimates:
- Estimated Tokens: {score.token_count}
- Estimated Cost: ${score.estimated_cost:.4f} per call

---
*Evaluation based on industry best practices from Anthropic, OpenAI, and research community*
"""
        return report
