"""
Expert Knowledge Base Module
Built-in best practices from Anthropic, OpenAI, and AI research community
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import json


@dataclass
class BestPractice:
    """Represents a prompt engineering best practice"""
    source: str  # "Anthropic", "OpenAI", "Research", etc.
    category: str
    title: str
    description: str
    do_this: List[str]
    avoid_this: List[str]
    example_good: str
    example_bad: str


class ExpertKnowledgeBase:
    """
    Curated knowledge base of prompt engineering best practices
    Sources: Anthropic, OpenAI, Google, Academic Research
    """

    def __init__(self):
        self.knowledge = self._load_knowledge_base()

    def _load_knowledge_base(self) -> Dict[str, List[BestPractice]]:
        """Load all best practices organized by category"""
        return {
            "clarity": self._clarity_practices(),
            "specificity": self._specificity_practices(),
            "structure": self._structure_practices(),
            "context": self._context_practices(),
            "examples": self._example_practices(),
            "output_format": self._output_format_practices(),
            "agent_communication": self._agent_communication_practices(),
            "error_handling": self._error_handling_practices(),
            "performance": self._performance_practices(),
            "safety": self._safety_practices(),
        }

    def _clarity_practices(self) -> List[BestPractice]:
        """Best practices for prompt clarity"""
        return [
            BestPractice(
                source="Anthropic",
                category="clarity",
                title="Use Clear, Direct Language",
                description="Be explicit and specific rather than vague or implicit",
                do_this=[
                    "Use simple, direct sentences",
                    "Define technical terms",
                    "Be explicit about what you want",
                    "Avoid ambiguous pronouns"
                ],
                avoid_this=[
                    "Vague instructions",
                    "Implicit assumptions",
                    "Complex nested clauses",
                    "Unclear pronouns (it, that, this)"
                ],
                example_good="Extract the customer's email address from the text and return it in lowercase.",
                example_bad="Get the email and make it look right."
            ),
            BestPractice(
                source="OpenAI",
                category="clarity",
                title="Put Instructions at the Beginning",
                description="Place the most important instructions at the start",
                do_this=[
                    "Start with the main task",
                    "Front-load critical instructions",
                    "Use clear headers/sections"
                ],
                avoid_this=[
                    "Burying key info in middle",
                    "Instructions at the end",
                    "Scattered requirements"
                ],
                example_good="Summarize this article in 3 sentences. Focus on the main arguments. [article text]",
                example_bad="[Long article text] ...and by the way, summarize this in 3 sentences focusing on main arguments."
            )
        ]

    def _specificity_practices(self) -> List[BestPractice]:
        """Best practices for specificity"""
        return [
            BestPractice(
                source="Anthropic",
                category="specificity",
                title="Specify Output Format Precisely",
                description="Define exact structure, length, and format of output",
                do_this=[
                    "Provide output template/schema",
                    "Specify length constraints",
                    "Define required fields",
                    "Include format examples"
                ],
                avoid_this=[
                    "Vague 'provide summary'",
                    "No length constraints",
                    "Unclear structure",
                    "Missing field definitions"
                ],
                example_good='''Return JSON with exactly these fields:
{
  "summary": "string (max 100 words)",
  "sentiment": "positive|negative|neutral",
  "confidence": number (0-1)
}''',
                example_bad="Give me a summary with the sentiment."
            ),
            BestPractice(
                source="OpenAI",
                category="specificity",
                title="Use Delimiters for Distinct Sections",
                description="Clearly separate different parts of the prompt",
                do_this=[
                    "Use triple quotes \"\"\" for text",
                    "Use XML tags <input></input>",
                    "Use markdown sections",
                    "Clear visual separation"
                ],
                avoid_this=[
                    "Run-on text without breaks",
                    "Unclear boundaries",
                    "Mixed instructions and data"
                ],
                example_good='''Analyze this review:
"""
This product is amazing! Highly recommend.
"""

Return: sentiment, rating (1-5), key phrases''',
                example_bad="Analyze this review: This product is amazing! Highly recommend. Return sentiment, rating and key phrases"
            )
        ]

    def _structure_practices(self) -> List[BestPractice]:
        """Best practices for prompt structure"""
        return [
            BestPractice(
                source="Research",
                category="structure",
                title="Use Hierarchical Organization",
                description="Organize complex prompts with clear hierarchy",
                do_this=[
                    "Use sections: ROLE, TASK, CONTEXT, FORMAT",
                    "Number steps clearly",
                    "Group related instructions",
                    "Use visual hierarchy"
                ],
                avoid_this=[
                    "Flat wall of text",
                    "No organization",
                    "Random order",
                    "Missing context"
                ],
                example_good='''# ROLE
You are a code review expert.

# TASK
Review this Python code for:
1. Security issues
2. Performance problems
3. Best practices

# OUTPUT
For each issue found:
- Line number
- Issue type
- Severity (high/medium/low)
- Recommendation''',
                example_bad="Review this code and find problems with security, performance, and best practices then tell me about them."
            )
        ]

    def _context_practices(self) -> List[BestPractice]:
        """Best practices for providing context"""
        return [
            BestPractice(
                source="Anthropic",
                category="context",
                title="Provide Relevant Background",
                description="Give context needed for informed responses",
                do_this=[
                    "Explain the use case",
                    "Define the audience",
                    "Set constraints/requirements",
                    "Mention relevant assumptions"
                ],
                avoid_this=[
                    "Assuming AI knows your context",
                    "Missing key constraints",
                    "Undefined audience",
                    "Implicit requirements"
                ],
                example_good='''Context: Creating API documentation for junior developers.
Target audience: Developers with 0-2 years experience.
Constraint: Must include code examples in Python.
Requirement: Explain technical terms when first used.

Task: Document this API endpoint...''',
                example_bad="Document this API endpoint."
            )
        ]

    def _example_practices(self) -> List[BestPractice]:
        """Best practices for using examples"""
        return [
            BestPractice(
                source="OpenAI",
                category="examples",
                title="Provide Diverse, Quality Examples",
                description="Use 3-5 high-quality examples covering edge cases",
                do_this=[
                    "Show ideal outputs",
                    "Cover edge cases",
                    "Use realistic examples",
                    "Show counter-examples if helpful"
                ],
                avoid_this=[
                    "Only one example",
                    "Trivial examples only",
                    "Unrealistic scenarios",
                    "Inconsistent patterns"
                ],
                example_good='''Examples:

Input: "Call me at 555-1234"
Output: {"phone": "555-1234"}

Input: "Email: user@example.com, Phone: (555) 123-4567"
Output: {"email": "user@example.com", "phone": "(555) 123-4567"}

Input: "No contact info provided"
Output: {"email": null, "phone": null}''',
                example_bad='''Example: "555-1234" → {"phone": "555-1234"}'''
            )
        ]

    def _output_format_practices(self) -> List[BestPractice]:
        """Best practices for output formatting"""
        return [
            BestPractice(
                source="Anthropic",
                category="output_format",
                title="Request Structured Output (JSON/XML)",
                description="Use structured formats for consistent parsing",
                do_this=[
                    "Specify JSON schema",
                    "Define all field types",
                    "Include validation rules",
                    "Provide complete example"
                ],
                avoid_this=[
                    "Free-form text output",
                    "Ambiguous format",
                    "Missing type info",
                    "No example provided"
                ],
                example_good='''Output JSON matching this schema:
{
  "title": "string (required)",
  "summary": "string (100-200 words)",
  "tags": ["array", "of", "strings"],
  "priority": "high|medium|low",
  "metadata": {
    "author": "string",
    "date": "ISO 8601 format"
  }
}''',
                example_bad="Return the title, summary, some tags, and priority."
            )
        ]

    def _agent_communication_practices(self) -> List[BestPractice]:
        """Best practices for agent-to-agent communication"""
        return [
            BestPractice(
                source="Research",
                category="agent_communication",
                title="Use Structured Message Protocols",
                description="Define clear communication protocols between agents",
                do_this=[
                    "Use typed messages (request/response/notify)",
                    "Include sender/receiver metadata",
                    "Define error handling protocol",
                    "Version your message schemas",
                    "Include correlation IDs for tracking"
                ],
                avoid_this=[
                    "Unstructured text messages",
                    "Missing metadata",
                    "No error handling",
                    "Ambiguous message types"
                ],
                example_good='''{
  "message_type": "request",
  "message_id": "req_123",
  "from": "AnalysisAgent",
  "to": "StorageAgent",
  "timestamp": "2024-01-15T10:30:00Z",
  "action": "store_result",
  "payload": {...},
  "expected_response": "acknowledgment",
  "timeout_ms": 5000
}''',
                example_bad="Hey, can you store this data? Thanks!"
            ),
            BestPractice(
                source="Research",
                category="agent_communication",
                title="Define Clear Agent Roles and Responsibilities",
                description="Each agent should have well-defined scope",
                do_this=[
                    "Explicit role definition",
                    "Clear input/output contracts",
                    "Defined capabilities",
                    "Documented limitations"
                ],
                avoid_this=[
                    "Overlapping responsibilities",
                    "Unclear boundaries",
                    "Implicit contracts",
                    "Undefined capabilities"
                ],
                example_good='''Agent: DataValidator
Role: Validate incoming data against schema
Input: Raw data + schema definition
Output: Validated data OR error list
Capabilities: Schema validation, type checking, range validation
Limitations: Does NOT transform data, Does NOT store data''',
                example_bad="This agent does data stuff."
            )
        ]

    def _error_handling_practices(self) -> List[BestPractice]:
        """Best practices for error handling"""
        return [
            BestPractice(
                source="Anthropic",
                category="error_handling",
                title="Specify Error Handling Behavior",
                description="Tell the AI how to handle errors and edge cases",
                do_this=[
                    "Define what constitutes an error",
                    "Specify fallback behavior",
                    "Request error messages",
                    "Handle null/missing data"
                ],
                avoid_this=[
                    "No error handling instructions",
                    "Assuming perfect input",
                    "Silent failures",
                    "Undefined edge cases"
                ],
                example_good='''If the email is invalid:
1. Return error: {"error": "invalid_email", "message": "..."}
2. Do NOT attempt to guess or fix
3. Include the invalid value for reference

If field is missing:
- Use null (not empty string)
- Note in "warnings" array''',
                example_bad="Extract the email address."
            )
        ]

    def _performance_practices(self) -> List[BestPractice]:
        """Best practices for performance"""
        return [
            BestPractice(
                source="OpenAI",
                category="performance",
                title="Optimize Token Usage",
                description="Reduce unnecessary tokens for cost and speed",
                do_this=[
                    "Be concise but clear",
                    "Remove redundant examples",
                    "Use abbreviations in data",
                    "Reference external docs when possible"
                ],
                avoid_this=[
                    "Excessive repetition",
                    "Overly verbose explanations",
                    "Too many examples",
                    "Duplicated information"
                ],
                example_good='''Task: Extract entities
Format: {"person": [], "org": [], "loc": []}
Example: "John works at Google in NYC" → {"person": ["John"], "org": ["Google"], "loc": ["NYC"]}''',
                example_bad='''Task: You need to extract entities from text. Entities include people, organizations, and locations. For example, if someone says...
[500 words of explanation]'''
            )
        ]

    def _safety_practices(self) -> List[BestPractice]:
        """Best practices for safety and ethics"""
        return [
            BestPractice(
                source="Anthropic",
                category="safety",
                title="Include Safety Guidelines",
                description="Add appropriate safety constraints",
                do_this=[
                    "Specify what NOT to do",
                    "Include privacy protections",
                    "Add content filters if needed",
                    "Request harmful content refusal"
                ],
                avoid_this=[
                    "No safety constraints",
                    "Assuming safe outputs",
                    "Missing privacy rules",
                    "No content filtering"
                ],
                example_good='''Guidelines:
- Do NOT include personally identifiable information
- Decline requests for harmful content
- If uncertain, ask for clarification
- Respect copyright and attribution''',
                example_bad="Do whatever the user asks."
            )
        ]

    def query(self, category: Optional[str] = None, source: Optional[str] = None) -> List[BestPractice]:
        """Query the knowledge base"""
        results = []

        for cat_name, practices in self.knowledge.items():
            if category and cat_name != category:
                continue

            for practice in practices:
                if source and practice.source != source:
                    continue

                results.append(practice)

        return results

    def get_all_categories(self) -> List[str]:
        """Get all available categories"""
        return list(self.knowledge.keys())

    def get_all_sources(self) -> List[str]:
        """Get all knowledge sources"""
        sources = set()
        for practices in self.knowledge.values():
            for practice in practices:
                sources.add(practice.source)
        return list(sources)

    def get_recommendations_for_task(self, task_description: str) -> List[BestPractice]:
        """Get relevant best practices for a specific task"""
        recommendations = []

        task_lower = task_description.lower()

        # Simple keyword matching for recommendations
        if "agent" in task_lower or "communication" in task_lower:
            recommendations.extend(self.query(category="agent_communication"))

        if "output" in task_lower or "format" in task_lower or "json" in task_lower:
            recommendations.extend(self.query(category="output_format"))

        if "example" in task_lower:
            recommendations.extend(self.query(category="examples"))

        if "error" in task_lower or "validation" in task_lower:
            recommendations.extend(self.query(category="error_handling"))

        # Always include clarity and specificity
        recommendations.extend(self.query(category="clarity")[:1])
        recommendations.extend(self.query(category="specificity")[:1])

        return recommendations

    def get_knowledge_summary(self) -> str:
        """Get a summary of the knowledge base"""
        summary = "# Expert Prompt Engineering Knowledge Base\n\n"

        summary += f"**Total Categories:** {len(self.knowledge)}\n"
        summary += f"**Sources:** {', '.join(self.get_all_sources())}\n\n"

        for category, practices in self.knowledge.items():
            summary += f"## {category.upper().replace('_', ' ')}\n"
            summary += f"**{len(practices)} best practices**\n\n"

        return summary
