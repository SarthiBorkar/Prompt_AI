"""
Advanced Prompting Techniques Module
Implements cutting-edge prompt engineering patterns from latest AI research
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json


@dataclass
class PromptTechnique:
    """Represents a prompt engineering technique"""
    name: str
    description: str
    pattern: str
    use_cases: List[str]
    example: str


class AdvancedPromptingTechniques:
    """
    Library of advanced prompting techniques from latest AI research
    Includes: CoT, ToT, ReAct, Self-Consistency, Few-Shot, Meta-Prompting, etc.
    """

    def __init__(self):
        self.techniques = self._load_techniques()

    def _load_techniques(self) -> Dict[str, PromptTechnique]:
        """Load all available prompting techniques"""
        return {
            "chain_of_thought": self._chain_of_thought(),
            "tree_of_thought": self._tree_of_thought(),
            "react": self._react_framework(),
            "self_consistency": self._self_consistency(),
            "few_shot": self._few_shot_learning(),
            "meta_prompting": self._meta_prompting(),
            "constitutional_ai": self._constitutional_ai(),
            "prompt_chaining": self._prompt_chaining(),
            "zero_shot_cot": self._zero_shot_cot(),
            "agent_to_agent": self._agent_to_agent(),
        }

    def _chain_of_thought(self) -> PromptTechnique:
        """Chain-of-Thought (CoT) prompting"""
        return PromptTechnique(
            name="Chain-of-Thought (CoT)",
            description="Encourages step-by-step reasoning before final answer",
            pattern="""Let's approach this step by step:

1. First, [analyze the input]
2. Then, [break down the problem]
3. Next, [reason through each step]
4. Finally, [provide the answer]

Think through your reasoning before answering.""",
            use_cases=[
                "Complex reasoning tasks",
                "Mathematical problems",
                "Multi-step analysis",
                "Decision making"
            ],
            example="""Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls. How many tennis balls does he have now?

A: Let's think step by step:
1. Roger starts with 5 tennis balls
2. He buys 2 cans, each with 3 balls = 2 × 3 = 6 balls
3. Total = 5 + 6 = 11 tennis balls

Answer: 11 tennis balls"""
        )

    def _tree_of_thought(self) -> PromptTechnique:
        """Tree-of-Thought (ToT) prompting"""
        return PromptTechnique(
            name="Tree-of-Thought (ToT)",
            description="Explores multiple reasoning paths and selects best",
            pattern="""Consider multiple approaches to this problem:

Approach 1: [Method A]
- Reasoning: [...]
- Outcome: [...]

Approach 2: [Method B]
- Reasoning: [...]
- Outcome: [...]

Approach 3: [Method C]
- Reasoning: [...]
- Outcome: [...]

Evaluate and select the best approach based on [criteria].""",
            use_cases=[
                "Complex problems with multiple solutions",
                "Strategic planning",
                "Creative problem solving",
                "Optimization tasks"
            ],
            example="""Problem: Design a system architecture

Approach 1: Microservices
- Pro: Scalable, independent deployment
- Con: Complex, network overhead

Approach 2: Monolithic
- Pro: Simple, fast development
- Con: Hard to scale

Approach 3: Serverless
- Pro: Auto-scaling, low maintenance
- Con: Vendor lock-in

Best choice: Microservices (based on long-term scalability needs)"""
        )

    def _react_framework(self) -> PromptTechnique:
        """ReAct (Reasoning + Acting) framework"""
        return PromptTechnique(
            name="ReAct Framework",
            description="Combines reasoning with actions, ideal for agents",
            pattern="""Use this pattern for agent tasks:

Thought: [Analyze what needs to be done]
Action: [Specific action to take]
Observation: [Result of the action]

Thought: [Analyze the observation]
Action: [Next action based on analysis]
Observation: [Result]

[Repeat until task complete]

Final Answer: [Conclusion based on all observations]""",
            use_cases=[
                "Agent-based systems",
                "Tool-using AI",
                "Multi-step tasks",
                "Interactive problem solving"
            ],
            example="""Task: Find the current weather in Tokyo

Thought: I need to search for Tokyo weather
Action: search("Tokyo weather today")
Observation: Tokyo is 18°C, partly cloudy

Thought: I have the weather info
Action: format_response()
Observation: Response ready

Answer: Tokyo weather is 18°C and partly cloudy today."""
        )

    def _self_consistency(self) -> PromptTechnique:
        """Self-Consistency prompting"""
        return PromptTechnique(
            name="Self-Consistency",
            description="Generate multiple reasoning paths, select most consistent answer",
            pattern="""Generate 3 different reasoning approaches:

Reasoning Path 1:
[Approach from angle 1]
Answer: [X]

Reasoning Path 2:
[Approach from angle 2]
Answer: [Y]

Reasoning Path 3:
[Approach from angle 3]
Answer: [Z]

Most consistent answer: [Select the answer that appears most often or is most robust]""",
            use_cases=[
                "Reducing hallucinations",
                "Improving accuracy",
                "Complex reasoning",
                "Verification tasks"
            ],
            example="""Q: Is Python faster than JavaScript?

Path 1 (Execution): Python slower (interpreted)
Path 2 (Development): Python faster (less code)
Path 3 (Libraries): Depends on use case

Consistent Answer: "Depends on context - Python for development speed, JS for runtime"""
        )

    def _few_shot_learning(self) -> PromptTechnique:
        """Few-Shot Learning prompting"""
        return PromptTechnique(
            name="Few-Shot Learning",
            description="Provide examples to guide the model",
            pattern="""Here are some examples:

Example 1:
Input: [Example input 1]
Output: [Example output 1]

Example 2:
Input: [Example input 2]
Output: [Example output 2]

Example 3:
Input: [Example input 3]
Output: [Example output 3]

Now apply the same pattern:
Input: [Your actual input]
Output:""",
            use_cases=[
                "Format consistency",
                "Style matching",
                "Pattern recognition",
                "Custom output formats"
            ],
            example="""Classify sentiment:

Example 1: "I love this!" → Positive
Example 2: "This is terrible." → Negative
Example 3: "It's okay." → Neutral

Classify: "This is amazing!"
Output: Positive"""
        )

    def _meta_prompting(self) -> PromptTechnique:
        """Meta-Prompting - prompts about prompts"""
        return PromptTechnique(
            name="Meta-Prompting",
            description="Use AI to generate or improve prompts",
            pattern="""You are a prompt engineering expert. Create/improve a prompt for: [task]

Requirements:
- Clear role definition
- Specific instructions
- Output format
- Examples if needed
- Error handling

Generate an optimal prompt that achieves: [goal]""",
            use_cases=[
                "Prompt generation",
                "Prompt optimization",
                "Automated prompt engineering",
                "A/B testing prompts"
            ],
            example="""Create a prompt for: "Extracting email addresses from text"

Generated Prompt:
"You are a data extraction specialist. Extract all email addresses from the given text.

Rules:
- Must be valid email format (user@domain.com)
- Return as JSON array
- Exclude duplicates
- Handle multiple domains

Input: [text]
Output: {"emails": ["email1@example.com", "email2@example.com"]}"""
        )

    def _constitutional_ai(self) -> PromptTechnique:
        """Constitutional AI - value-aligned prompting"""
        return PromptTechnique(
            name="Constitutional AI",
            description="Add ethical guidelines and constraints",
            pattern="""Core Principles:
1. Be helpful, harmless, and honest
2. Respect privacy and confidentiality
3. Avoid bias and discrimination
4. Provide accurate information
5. Decline harmful requests politely

Task: [Your task]

Ensure your response aligns with all principles above.""",
            use_cases=[
                "Production AI systems",
                "User-facing applications",
                "Sensitive domains",
                "Ethical AI deployment"
            ],
            example="""Constitutional Guidelines:
- No personal data sharing
- No harmful content
- Factual accuracy required
- Respect all users

Task: Provide health advice
Response: "I can provide general wellness information, but please consult a healthcare professional for medical advice." """
        )

    def _prompt_chaining(self) -> PromptTechnique:
        """Prompt Chaining for complex workflows"""
        return PromptTechnique(
            name="Prompt Chaining",
            description="Break complex tasks into sequential prompts",
            pattern="""Step 1: [Subtask 1]
Input: [Initial input]
Output: [Result 1]

Step 2: [Subtask 2]
Input: [Result 1]
Output: [Result 2]

Step 3: [Subtask 3]
Input: [Result 2]
Final Output: [Final result]""",
            use_cases=[
                "Complex workflows",
                "Multi-stage processing",
                "Agent pipelines",
                "Data transformation"
            ],
            example="""Task: Analyze and summarize research paper

Chain:
1. Extract: Get title, authors, abstract
2. Analyze: Identify key findings
3. Summarize: Create 3-sentence summary
4. Format: Output as markdown"""
        )

    def _zero_shot_cot(self) -> PromptTechnique:
        """Zero-Shot Chain-of-Thought"""
        return PromptTechnique(
            name="Zero-Shot CoT",
            description="Trigger reasoning without examples",
            pattern="""[Your question or task]

Let's think step by step.""",
            use_cases=[
                "Quick reasoning",
                "No example available",
                "General problem solving",
                "Exploratory analysis"
            ],
            example="""Q: What are the implications of quantum computing for cryptography?

Let's think step by step:
1. Current encryption relies on hard math problems
2. Quantum computers can solve these faster
3. Need new quantum-resistant algorithms
4. Transition period will be critical

Answer: Quantum computing threatens current encryption, requiring new cryptographic methods."""
        )

    def _agent_to_agent(self) -> PromptTechnique:
        """Agent-to-Agent Communication Patterns"""
        return PromptTechnique(
            name="Agent-to-Agent Communication",
            description="Structured patterns for multi-agent systems",
            pattern="""AGENT COMMUNICATION PROTOCOL:

From: [Agent Name/Role]
To: [Recipient Agent]
Context: [Shared context ID]

Message:
{
  "type": "[request|response|notification]",
  "action": "[specific action]",
  "data": {
    [structured data]
  },
  "constraints": [constraints],
  "expected_format": {
    [output format specification]
  }
}

Validation Rules:
- All JSON must be valid
- Required fields: type, action, data
- Error handling: [specify]""",
            use_cases=[
                "Multi-agent systems",
                "Agent orchestration",
                "Workflow automation",
                "Distributed AI systems"
            ],
            example="""From: AnalysisAgent
To: SummaryAgent
Context: task_123

Message:
{
  "type": "request",
  "action": "summarize_findings",
  "data": {
    "analysis_results": [...],
    "word_limit": 100
  },
  "expected_format": {
    "summary": "string",
    "key_points": ["array"]
  }
}"""
        )

    def get_technique(self, technique_name: str) -> Optional[PromptTechnique]:
        """Get a specific technique by name"""
        return self.techniques.get(technique_name)

    def get_all_techniques(self) -> Dict[str, PromptTechnique]:
        """Get all available techniques"""
        return self.techniques

    def suggest_technique(self, task_description: str) -> List[str]:
        """Suggest appropriate techniques based on task"""
        suggestions = []

        task_lower = task_description.lower()

        # Rule-based suggestions
        if any(word in task_lower for word in ["reason", "analyze", "think", "complex"]):
            suggestions.append("chain_of_thought")

        if any(word in task_lower for word in ["agent", "tool", "action", "multi-step"]):
            suggestions.append("react")

        if any(word in task_lower for word in ["multiple", "compare", "various", "different"]):
            suggestions.append("tree_of_thought")

        if any(word in task_lower for word in ["accurate", "verify", "check", "validate"]):
            suggestions.append("self_consistency")

        if any(word in task_lower for word in ["example", "format", "style", "pattern"]):
            suggestions.append("few_shot")

        if any(word in task_lower for word in ["agent-to-agent", "communication", "protocol", "workflow"]):
            suggestions.append("agent_to_agent")

        if any(word in task_lower for word in ["ethical", "safe", "responsible", "privacy"]):
            suggestions.append("constitutional_ai")

        if any(word in task_lower for word in ["workflow", "pipeline", "sequence", "stages"]):
            suggestions.append("prompt_chaining")

        # Default to zero-shot CoT if no specific match
        if not suggestions:
            suggestions.append("zero_shot_cot")

        return suggestions

    def apply_technique(self, base_prompt: str, technique_name: str, **kwargs) -> str:
        """Apply a technique to enhance a base prompt"""
        technique = self.get_technique(technique_name)
        if not technique:
            return base_prompt

        # Apply the technique pattern to the base prompt
        enhanced_prompt = f"""# Using {technique.name}

{technique.description}

## Pattern Applied:
{technique.pattern}

## Your Task:
{base_prompt}

## Remember:
{', '.join(technique.use_cases)}
"""
        return enhanced_prompt

    def get_technique_summary(self) -> str:
        """Get a summary of all available techniques"""
        summary = "# Available Advanced Prompting Techniques\n\n"

        for name, technique in self.techniques.items():
            summary += f"## {technique.name}\n"
            summary += f"**Description:** {technique.description}\n"
            summary += f"**Use Cases:** {', '.join(technique.use_cases)}\n\n"

        return summary
