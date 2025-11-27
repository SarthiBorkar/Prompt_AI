"""
Refinement Engine Module
Implements the two-iteration internal refinement process for quality assurance
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from dxtag_manager import PromptComponent, VersionType


@dataclass
class RefinementCriteria:
    """Criteria for evaluating prompt quality"""
    clear_intent: bool = False
    specific_constraints: bool = False
    easy_parsing: bool = False
    no_ambiguities: bool = False
    proper_structure: bool = False
    score: float = 0.0


@dataclass
class RefinementIteration:
    """Results from a single refinement iteration"""
    iteration_number: int
    original_prompt: PromptComponent
    refined_prompt: PromptComponent
    criteria: RefinementCriteria
    improvements: List[str]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class RefinementEngine:
    """
    Manages the two-iteration internal refinement process
    """

    def __init__(self):
        self.refinement_history: List[RefinementIteration] = []
        self.improvement_patterns: Dict[str, int] = {}  # Track common improvements

    def refine(
        self,
        initial_prompt: PromptComponent,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[PromptComponent, List[RefinementIteration]]:
        """
        Performs two-iteration refinement on a prompt

        Args:
            initial_prompt: The initial prompt to refine
            context: Optional context for refinement decisions

        Returns:
            Tuple of (final_prompt, iteration_history)
        """
        iterations = []
        current_prompt = initial_prompt

        # First iteration
        first_refined, first_iteration = self._perform_iteration(
            current_prompt,
            iteration_number=1,
            context=context
        )
        iterations.append(first_iteration)
        current_prompt = first_refined

        # Second iteration
        second_refined, second_iteration = self._perform_iteration(
            current_prompt,
            iteration_number=2,
            context=context
        )
        iterations.append(second_iteration)

        # Update refinement history
        self.refinement_history.extend(iterations)

        # Learn from improvements
        self._update_improvement_patterns(iterations)

        return second_refined, iterations

    def _perform_iteration(
        self,
        prompt: PromptComponent,
        iteration_number: int,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[PromptComponent, RefinementIteration]:
        """
        Performs a single refinement iteration

        Args:
            prompt: Current prompt
            iteration_number: Which iteration (1 or 2)
            context: Optional context

        Returns:
            Tuple of (refined_prompt, iteration_record)
        """
        # Evaluate current prompt
        criteria = self._evaluate_prompt(prompt)

        # Identify improvements needed
        improvements = self._identify_improvements(prompt, criteria)

        # Apply improvements if needed
        if improvements and criteria.score < 0.9:
            refined_prompt = self._apply_improvements(prompt, improvements)
        else:
            # Already good enough, minimal changes
            refined_prompt = prompt

        # Create iteration record
        iteration = RefinementIteration(
            iteration_number=iteration_number,
            original_prompt=prompt,
            refined_prompt=refined_prompt,
            criteria=criteria,
            improvements=improvements
        )

        return refined_prompt, iteration

    def _evaluate_prompt(self, prompt: PromptComponent) -> RefinementCriteria:
        """
        Evaluates a prompt against quality criteria

        Args:
            prompt: Prompt to evaluate

        Returns:
            RefinementCriteria with evaluation results
        """
        criteria = RefinementCriteria()

        # Check for clear intent
        role = prompt.data.get('role', '')
        task = prompt.data.get('task', '')

        criteria.clear_intent = bool(role and task and len(task.split()) > 5)

        # Check for specific constraints
        constraints = prompt.execution.get('constraints', [])
        criteria.specific_constraints = len(constraints) >= 2

        # Check for easy parsing (well-defined output format)
        output_format = prompt.execution.get('output_format', {})
        criteria.easy_parsing = bool(output_format and len(output_format) > 0)

        # Check for ambiguities (heuristic)
        ambiguous_words = ['maybe', 'possibly', 'might', 'could', 'perhaps', 'somehow']
        task_lower = task.lower()
        criteria.no_ambiguities = not any(word in task_lower for word in ambiguous_words)

        # Check for proper structure
        has_role = bool(role)
        has_task = bool(task)
        has_context = bool(prompt.data.get('context'))
        has_output = bool(output_format)

        criteria.proper_structure = sum([has_role, has_task, has_context, has_output]) >= 3

        # Calculate overall score
        scores = [
            criteria.clear_intent,
            criteria.specific_constraints,
            criteria.easy_parsing,
            criteria.no_ambiguities,
            criteria.proper_structure
        ]
        criteria.score = sum(scores) / len(scores)

        return criteria

    def _identify_improvements(
        self,
        prompt: PromptComponent,
        criteria: RefinementCriteria
    ) -> List[str]:
        """
        Identifies specific improvements needed

        Args:
            prompt: Prompt to improve
            criteria: Evaluation criteria

        Returns:
            List of improvement descriptions
        """
        improvements = []

        if not criteria.clear_intent:
            improvements.append("clarify_intent")
            improvements.append("Enhance role definition and task description for clarity")

        if not criteria.specific_constraints:
            improvements.append("add_constraints")
            improvements.append("Add specific constraints and requirements")

        if not criteria.easy_parsing:
            improvements.append("define_output_format")
            improvements.append("Define clear output format specification")

        if not criteria.no_ambiguities:
            improvements.append("remove_ambiguities")
            improvements.append("Remove ambiguous language and add specificity")

        if not criteria.proper_structure:
            improvements.append("improve_structure")
            improvements.append("Enhance overall prompt structure")

        return improvements

    def _apply_improvements(
        self,
        prompt: PromptComponent,
        improvements: List[str]
    ) -> PromptComponent:
        """
        Applies improvements to a prompt

        Args:
            prompt: Current prompt
            improvements: List of improvements to apply

        Returns:
            Improved PromptComponent
        """
        refinements = {
            "data": prompt.data.copy(),
            "execution": prompt.execution.copy(),
            "reason": f"Applied {len(improvements)} improvements"
        }

        # Apply specific improvements
        for improvement in improvements:
            if improvement == "clarify_intent":
                # Enhance role if too brief
                if len(refinements["data"].get("role", "")) < 20:
                    current_role = refinements["data"].get("role", "professional assistant")
                    refinements["data"]["role"] = f"an expert {current_role} specializing in prompt engineering"

                # Enhance task if too brief
                if len(refinements["data"].get("task", "")) < 30:
                    current_task = refinements["data"].get("task", "")
                    refinements["data"]["task"] = f"{current_task}. Ensure the output is clear, accurate, and comprehensive."

            elif improvement == "add_constraints":
                current_constraints = refinements["execution"].get("constraints", [])
                if len(current_constraints) < 2:
                    default_constraints = [
                        "Ensure output is well-formatted and easy to read",
                        "Provide complete and accurate information",
                        "Maintain professional tone throughout"
                    ]
                    refinements["execution"]["constraints"] = current_constraints + default_constraints

            elif improvement == "define_output_format":
                if not refinements["execution"].get("output_format"):
                    refinements["execution"]["output_format"] = {
                        "type": "structured",
                        "format": "text",
                        "sections": ["main_content", "summary"]
                    }

            elif improvement == "remove_ambiguities":
                # Replace ambiguous words with definitive language
                task = refinements["data"].get("task", "")
                ambiguous_replacements = {
                    "maybe": "specifically",
                    "possibly": "definitely",
                    "might": "will",
                    "could": "should",
                    "perhaps": "certainly",
                    "somehow": "by using"
                }
                for ambiguous, definite in ambiguous_replacements.items():
                    task = task.replace(ambiguous, definite)
                refinements["data"]["task"] = task

            elif improvement == "improve_structure":
                # Ensure all key components exist
                if not refinements["data"].get("context"):
                    refinements["data"]["context"] = {
                        "purpose": "general prompt engineering",
                        "target": "AI language model"
                    }

        # Create refined component
        from dxtag_manager import DxTagManager
        manager = DxTagManager()

        new_component = PromptComponent(
            data=refinements["data"],
            execution=refinements["execution"],
            tags=prompt.tags.copy(),
            version=prompt.version,
            component_id=prompt.component_id
        )

        # Increment version as minor change
        version_parts = new_component.version.split('.')
        version_parts[1] = str(int(version_parts[1]) + 1)
        new_component.version = '.'.join(version_parts)

        return new_component

    def _update_improvement_patterns(self, iterations: List[RefinementIteration]):
        """
        Updates learning patterns based on refinement iterations

        Args:
            iterations: List of refinement iterations
        """
        for iteration in iterations:
            for improvement in iteration.improvements:
                # Extract improvement type (first word)
                if isinstance(improvement, str):
                    improvement_type = improvement.split()[0] if ' ' in improvement else improvement
                    if improvement_type not in self.improvement_patterns:
                        self.improvement_patterns[improvement_type] = 0
                    self.improvement_patterns[improvement_type] += 1

    def get_common_improvements(self, top_n: int = 5) -> List[Tuple[str, int]]:
        """
        Gets the most common improvement patterns

        Args:
            top_n: Number of top patterns to return

        Returns:
            List of (improvement_type, count) tuples
        """
        sorted_patterns = sorted(
            self.improvement_patterns.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_patterns[:top_n]

    def should_iterate_again(
        self,
        iteration: RefinementIteration,
        max_iterations: int = 2
    ) -> bool:
        """
        Determines if another iteration is needed

        Args:
            iteration: Current iteration
            max_iterations: Maximum allowed iterations

        Returns:
            True if another iteration is recommended
        """
        # Always do at least 2 iterations as per design
        if iteration.iteration_number < 2:
            return True

        # Don't exceed max iterations
        if iteration.iteration_number >= max_iterations:
            return False

        # Check if quality threshold is met
        if iteration.criteria.score >= 0.95:
            return False

        # Check if significant improvements were made
        if len(iteration.improvements) > 0:
            return True

        return False

    def get_refinement_stats(self) -> Dict[str, Any]:
        """
        Gets statistics about refinement history

        Returns:
            Dictionary with statistics
        """
        if not self.refinement_history:
            return {
                "total_refinements": 0,
                "average_score_improvement": 0.0,
                "common_improvements": []
            }

        # Calculate average score improvement
        improvements = []
        for i in range(0, len(self.refinement_history), 2):
            if i + 1 < len(self.refinement_history):
                first = self.refinement_history[i]
                second = self.refinement_history[i + 1]
                # Compare original from first to final from second
                original_score = self._evaluate_prompt(first.original_prompt).score
                final_score = self._evaluate_prompt(second.refined_prompt).score
                improvements.append(final_score - original_score)

        avg_improvement = sum(improvements) / len(improvements) if improvements else 0.0

        return {
            "total_refinements": len(self.refinement_history) // 2,
            "total_iterations": len(self.refinement_history),
            "average_score_improvement": avg_improvement,
            "common_improvements": self.get_common_improvements()
        }

    def reset_history(self):
        """Resets refinement history"""
        self.refinement_history.clear()
        self.improvement_patterns.clear()
