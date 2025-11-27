"""
DxTag Pattern Manager
Implements the DxTag architectural pattern for prompt engineering:
- Data structures
- eXecution logic
- Tag/presentation formatting

Includes semantic versioning and dependency management
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import json
import hashlib
from enum import Enum


class VersionType(Enum):
    """Semantic version types"""
    PATCH = "patch"  # Minor wording adjustments
    MINOR = "minor"  # Structural modifications
    MAJOR = "major"  # Fundamental redesigns


@dataclass
class PromptVersion:
    """Represents a version of a prompt"""
    version: str
    prompt_data: Dict[str, Any]
    execution_logic: Dict[str, Any]
    tags: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    change_log: str = ""
    parent_version: Optional[str] = None


@dataclass
class PromptComponent:
    """
    A component of a prompt following DxTag pattern
    """
    # Data: The actual content
    data: Dict[str, Any]

    # eXecution: Logic and instructions
    execution: Dict[str, Any]

    # Tags: Metadata and formatting
    tags: Dict[str, str]

    # Version info
    version: str = "1.0.0"
    component_id: str = field(default_factory=lambda: hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8])


class DxTagManager:
    """
    Manages prompts using the DxTag pattern with version control
    """

    def __init__(self):
        self.versions: Dict[str, PromptVersion] = {}
        self.current_version: Optional[str] = None
        self.dependencies: Dict[str, List[str]] = {}  # prompt_id -> [dependent_ids]

    def create_prompt(
        self,
        role: str,
        task: str,
        context: Dict[str, Any],
        constraints: List[str],
        output_format: Dict[str, Any],
        examples: Optional[List[Dict]] = None
    ) -> PromptComponent:
        """
        Creates a structured prompt using DxTag pattern

        Args:
            role: The role/persona for the AI
            task: The main task description
            context: Background context and information
            constraints: List of constraints and requirements
            output_format: Specification of the desired output format
            examples: Optional few-shot examples

        Returns:
            PromptComponent with structured data
        """
        # Data structure
        data = {
            "role": role,
            "task": task,
            "context": context,
            "examples": examples or []
        }

        # Execution logic
        execution = {
            "constraints": constraints,
            "output_format": output_format,
            "processing_instructions": [
                "Read and understand the role and context",
                "Analyze the task requirements",
                "Apply constraints during processing",
                "Format output according to specifications"
            ]
        }

        # Tags and metadata
        tags = {
            "created": datetime.now().isoformat(),
            "purpose": "prompt_engineering",
            "format_version": "dxtag-1.0",
            "complexity": self._assess_complexity(task, constraints)
        }

        component = PromptComponent(
            data=data,
            execution=execution,
            tags=tags
        )

        # Store as version 1.0.0
        self._store_version(component, "1.0.0", "Initial prompt creation")

        return component

    def refine_prompt(
        self,
        component: PromptComponent,
        refinements: Dict[str, Any],
        version_type: VersionType = VersionType.MINOR
    ) -> PromptComponent:
        """
        Refines an existing prompt and creates a new version

        Args:
            component: The current prompt component
            refinements: Dictionary of refinements to apply
            version_type: Type of version increment (PATCH, MINOR, MAJOR)

        Returns:
            New PromptComponent with refinements applied
        """
        # Create a copy
        new_data = component.data.copy()
        new_execution = component.execution.copy()
        new_tags = component.tags.copy()

        # Apply refinements
        if "data" in refinements:
            new_data.update(refinements["data"])

        if "execution" in refinements:
            new_execution.update(refinements["execution"])

        if "tags" in refinements:
            new_tags.update(refinements["tags"])

        # Create new component
        refined_component = PromptComponent(
            data=new_data,
            execution=new_execution,
            tags=new_tags,
            version=self._increment_version(component.version, version_type),
            component_id=component.component_id
        )

        # Store new version
        change_log = self._generate_change_log(component, refined_component, refinements)
        self._store_version(refined_component, refined_component.version, change_log)

        return refined_component

    def to_prompt_string(self, component: PromptComponent, style: str = "structured") -> str:
        """
        Converts a PromptComponent to a formatted prompt string

        Args:
            component: The prompt component to convert
            style: Output style ('structured', 'minimal', 'conversational')

        Returns:
            Formatted prompt string
        """
        if style == "structured":
            return self._format_structured(component)
        elif style == "minimal":
            return self._format_minimal(component)
        elif style == "conversational":
            return self._format_conversational(component)
        else:
            return self._format_structured(component)

    def _format_structured(self, component: PromptComponent) -> str:
        """Formats prompt in structured style"""
        sections = []

        # Role section
        sections.append(f"# ROLE\n{component.data['role']}\n")

        # Context section
        if component.data.get('context'):
            sections.append("# CONTEXT")
            for key, value in component.data['context'].items():
                sections.append(f"- {key}: {value}")
            sections.append("")

        # Task section
        sections.append(f"# TASK\n{component.data['task']}\n")

        # Constraints section
        if component.execution.get('constraints'):
            sections.append("# CONSTRAINTS")
            for i, constraint in enumerate(component.execution['constraints'], 1):
                sections.append(f"{i}. {constraint}")
            sections.append("")

        # Output format section
        sections.append("# OUTPUT FORMAT")
        sections.append(json.dumps(component.execution['output_format'], indent=2))
        sections.append("")

        # Examples section
        if component.data.get('examples') and component.data['examples']:
            sections.append("# EXAMPLES")
            for i, example in enumerate(component.data['examples'], 1):
                sections.append(f"\n## Example {i}")
                sections.append(f"Input: {example.get('input', 'N/A')}")
                sections.append(f"Output: {example.get('output', 'N/A')}")
            sections.append("")

        return "\n".join(sections)

    def _format_minimal(self, component: PromptComponent) -> str:
        """Formats prompt in minimal style"""
        parts = []

        if component.data.get('role'):
            parts.append(f"You are {component.data['role']}.")

        parts.append(component.data['task'])

        if component.execution.get('constraints'):
            parts.append(f"Requirements: {'; '.join(component.execution['constraints'])}")

        return " ".join(parts)

    def _format_conversational(self, component: PromptComponent) -> str:
        """Formats prompt in conversational style"""
        parts = []

        # Friendly introduction
        if component.data.get('role'):
            parts.append(f"I'd like you to act as {component.data['role']}.")

        # Context as narrative
        if component.data.get('context'):
            context_str = ", ".join([f"{k}: {v}" for k, v in component.data['context'].items()])
            parts.append(f"Here's some background information: {context_str}.")

        # Task description
        parts.append(f"Your task is to {component.data['task']}.")

        # Constraints as requests
        if component.execution.get('constraints'):
            parts.append("Please make sure to:")
            for constraint in component.execution['constraints']:
                parts.append(f"- {constraint}")

        # Output format
        parts.append(f"\nPlease provide your response in the following format: {json.dumps(component.execution['output_format'])}")

        return "\n".join(parts)

    def _assess_complexity(self, task: str, constraints: List[str]) -> str:
        """Assesses prompt complexity"""
        score = 0

        # Task length
        score += len(task.split()) // 20

        # Number of constraints
        score += len(constraints)

        # Complexity keywords
        complex_keywords = ['analyze', 'compare', 'evaluate', 'synthesize', 'optimize']
        score += sum(1 for keyword in complex_keywords if keyword in task.lower())

        if score <= 3:
            return "low"
        elif score <= 7:
            return "medium"
        else:
            return "high"

    def _increment_version(self, current: str, version_type: VersionType) -> str:
        """Increments version number based on type"""
        major, minor, patch = map(int, current.split('.'))

        if version_type == VersionType.MAJOR:
            return f"{major + 1}.0.0"
        elif version_type == VersionType.MINOR:
            return f"{major}.{minor + 1}.0"
        else:  # PATCH
            return f"{major}.{minor}.{patch + 1}"

    def _store_version(self, component: PromptComponent, version: str, change_log: str):
        """Stores a version in the version history"""
        prompt_version = PromptVersion(
            version=version,
            prompt_data=component.data,
            execution_logic=component.execution,
            tags=component.tags,
            change_log=change_log,
            parent_version=self.current_version
        )

        version_key = f"{component.component_id}_{version}"
        self.versions[version_key] = prompt_version
        self.current_version = version_key

    def _generate_change_log(
        self,
        old: PromptComponent,
        new: PromptComponent,
        refinements: Dict[str, Any]
    ) -> str:
        """Generates a change log describing the differences"""
        changes = []

        if old.data != new.data:
            changes.append("Data modifications")

        if old.execution != new.execution:
            changes.append("Execution logic updated")

        if refinements.get("reason"):
            changes.append(f"Reason: {refinements['reason']}")

        return "; ".join(changes) if changes else "Minor refinements"

    def get_version_history(self, component_id: str) -> List[PromptVersion]:
        """Gets version history for a component"""
        return [
            version for key, version in self.versions.items()
            if key.startswith(component_id)
        ]

    def add_dependency(self, prompt_id: str, depends_on: str):
        """Adds a dependency relationship between prompts"""
        if prompt_id not in self.dependencies:
            self.dependencies[prompt_id] = []
        self.dependencies[prompt_id].append(depends_on)

    def check_compatibility(self, prompt1_id: str, prompt2_id: str) -> bool:
        """Checks if two prompts are compatible for chaining"""
        # Simple version compatibility check
        # In production, this would check output/input format compatibility
        return True

    def to_dict(self, component: PromptComponent) -> Dict[str, Any]:
        """Converts component to dictionary"""
        return {
            "data": component.data,
            "execution": component.execution,
            "tags": component.tags,
            "version": component.version,
            "component_id": component.component_id
        }

    def from_dict(self, data: Dict[str, Any]) -> PromptComponent:
        """Creates component from dictionary"""
        return PromptComponent(
            data=data["data"],
            execution=data["execution"],
            tags=data["tags"],
            version=data.get("version", "1.0.0"),
            component_id=data.get("component_id", "")
        )
