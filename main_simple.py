#!/usr/bin/env python3
"""
Enhanced Prompt Engineering AI Agent
Features: Advanced Techniques, Expert Knowledge, Quality Scoring, Continuous Learning
"""

import os
import sys
import asyncio
from dotenv import load_dotenv
from prompt_engineering_crew import PromptEngineeringCrew
from logging_config import setup_logging

# Load environment variables
load_dotenv(override=True)

# Configure logging
logger = setup_logging()

# Disable CrewAI telemetry
os.environ['CREWAI_DISABLE_TELEMETRY'] = 'true'


async def test_prompt_engineering(text: str, style: str = "structured"):
    """
    Test the prompt engineering crew with a given input

    Args:
        text: Input text describing what prompt you need
        style: Output style (structured, minimal, conversational)

    Returns:
        Engineered prompt result
    """
    logger.info(f"Testing prompt engineering with input: {text[:100]}...")

    # Initialize crew
    crew = PromptEngineeringCrew(verbose=True, logger=logger)

    # Process input
    result = await crew.process_input(text=text, style=style)

    return result


def print_section(title: str, char: str = "="):
    """Print a formatted section header"""
    width = 70
    print("\n" + char * width)
    print(f"  {title}")
    print(char * width + "\n")


async def interactive_mode():
    """Run in interactive mode - keep asking for prompts"""
    print_section("🤖 Enhanced Prompt Engineering AI Agent - Interactive Mode", "=")

    print("✨ Features: Advanced Techniques • Expert Knowledge • Quality Scoring • Continuous Learning")
    print("\nThis agent will help you create professional, expert-level prompts.")
    print("Type your prompt description and press Enter.")
    print("Type 'quit' or 'exit' to stop.\n")

    while True:
        try:
            # Get user input
            print("-" * 70)
            user_input = input("\n💭 What prompt do you need? > ").strip()

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!\n")
                break

            if not user_input:
                print("⚠️  Please enter a description")
                continue

            # Process the prompt
            web_enabled = os.getenv("ENABLE_WEB_RESEARCH", "false").lower() == "true"
            agent_count = "6 AI agents (with web research)" if web_enabled else "5 AI agents"
            print(f"\n⏳ Processing with {agent_count}...\n")
            result = await test_prompt_engineering(user_input)

            # Display result
            if result.get("success"):
                print_section("✅ Engineered Prompt", "-")
                print(result.get("prompt", "No prompt generated"))
                print("\n" + "-" * 70)

                # Show quality evaluation
                quality = result.get("quality_evaluation", {})
                if quality:
                    print(f"\n📊 Quality Score: {quality.get('overall_score', 'N/A')}/100 (Grade: {quality.get('grade', 'N/A')})")
                    print(f"   - Clarity: {quality.get('clarity_score', 'N/A')}/100")
                    print(f"   - Specificity: {quality.get('specificity_score', 'N/A')}/100")
                    print(f"   - Completeness: {quality.get('completeness_score', 'N/A')}/100")
                    print(f"   - Agent-Ready: {quality.get('agent_ready_score', 'N/A')}/100")

                    strengths = quality.get('strengths', [])
                    if strengths:
                        print(f"\n💪 Strengths:")
                        for strength in strengths[:3]:  # Top 3
                            print(f"   ✓ {strength}")

                # Show techniques used
                techniques = result.get("techniques_used", [])
                if techniques:
                    print(f"\n🔬 Techniques Applied: {', '.join(techniques)}")

                # Show learning insights
                learning = result.get("learning_insights", {})
                if learning:
                    trend = learning.get("performance_trend", {})
                    if trend.get("status") == "active":
                        print(f"\n📈 Learning Stats:")
                        print(f"   - Recent Success Rate: {trend.get('recent_success_rate', 'N/A')}%")
                        print(f"   - Recent Avg Quality: {trend.get('recent_avg_quality', 'N/A')}/100")
                        print(f"   - Trend: {trend.get('improvement', 'collecting data').upper()}")
                        print(f"   - Processing Time: {learning.get('processing_time', 'N/A')}s")

                # Show analysis summary
                analysis = result.get("analysis", {})
                if analysis:
                    print(f"\n🧠 Multi-Dimensional Analysis: {analysis.get('total_insights', 0)} insights")

                # Show rate limit info
                rate_info = result.get("rate_limit_stats", {})
                if rate_info:
                    print(f"\n⚡ Rate Limit: {rate_info.get('requests_remaining', 'N/A')} requests remaining")
            else:
                print_section("❌ Error", "-")
                print(f"Error: {result.get('error', 'Unknown error')}")

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            logger.error(f"Error in interactive mode: {str(e)}", exc_info=True)


async def single_test_mode(test_input: str):
    """Run a single test and exit"""
    print_section("🚀 Running Enhanced Prompt Engineering Agent", "=")

    web_enabled = os.getenv("ENABLE_WEB_RESEARCH", "false").lower() == "true"
    features = "Advanced Techniques • Expert Knowledge • Quality Scoring • Continuous Learning"
    if web_enabled:
        features += " • Web Research"
    print(f"✨ Features: {features}\n")
    print(f"Input: {test_input}\n")

    agent_count = "6 AI agents (with web research)" if web_enabled else "5 AI agents"
    print(f"Processing with {agent_count}...\n")

    # Run the crew
    result = await test_prompt_engineering(test_input)

    # Display result
    print_section("✅ Engineered Prompt", "=")

    if result.get("success"):
        print(result.get("prompt", "No prompt generated"))

        # Show quality evaluation
        print("\n" + "=" * 70)
        quality = result.get("quality_evaluation", {})
        if quality:
            print(f"\n📊 QUALITY EVALUATION")
            print("━" * 70)
            print(f"Overall Score: {quality.get('overall_score', 'N/A')}/100 (Grade: {quality.get('grade', 'N/A')})")
            print(f"\nDetailed Scores:")
            print(f"  • Clarity:       {quality.get('clarity_score', 'N/A')}/100")
            print(f"  • Specificity:   {quality.get('specificity_score', 'N/A')}/100")
            print(f"  • Completeness:  {quality.get('completeness_score', 'N/A')}/100")
            print(f"  • Structure:     {quality.get('structure_score', 'N/A')}/100")
            print(f"  • Efficiency:    {quality.get('efficiency_score', 'N/A')}/100")
            print(f"  • Agent-Ready:   {quality.get('agent_ready_score', 'N/A')}/100")

            strengths = quality.get('strengths', [])
            if strengths:
                print(f"\n💪 Strengths:")
                for strength in strengths:
                    print(f"   ✓ {strength}")

            improvements = quality.get('improvements', [])
            if improvements and len(improvements) > 0 and improvements[0] != "Prompt is excellent - no major improvements needed":
                print(f"\n💡 Suggested Improvements:")
                for improvement in improvements[:3]:  # Top 3
                    print(f"   • {improvement}")

            print(f"\n📏 Metrics:")
            print(f"   - Token Count: {quality.get('token_count', 'N/A')}")
            print(f"   - Estimated Cost: ${quality.get('estimated_cost', 0):.4f}")

        # Show techniques used
        techniques = result.get("techniques_used", [])
        if techniques:
            print(f"\n🔬 TECHNIQUES APPLIED")
            print("━" * 70)
            print(f"{', '.join(techniques)}")

        # Show learning insights
        learning = result.get("learning_insights", {})
        if learning:
            print(f"\n📈 CONTINUOUS LEARNING INSIGHTS")
            print("━" * 70)
            trend = learning.get("performance_trend", {})
            if trend.get("status") == "active":
                print(f"Total Interactions: {trend.get('total_interactions', 'N/A')}")
                print(f"Recent Success Rate: {trend.get('recent_success_rate', 'N/A')}%")
                print(f"Recent Avg Quality: {trend.get('recent_avg_quality', 'N/A')}/100")
                print(f"Performance Trend: {trend.get('improvement', 'collecting data').upper()}")
                if trend.get('quality_trend'):
                    print(f"Quality Change: {trend.get('quality_trend', 0):+.1f}%")
            print(f"Processing Time: {learning.get('processing_time', 'N/A')}s")

        # Show analysis summary
        analysis = result.get("analysis", {})
        if analysis:
            print(f"\n🧠 MULTI-DIMENSIONAL ANALYSIS")
            print("━" * 70)
            print(f"Total Insights: {analysis.get('total_insights', 0)}")
            print(f"Thinking Dimensions: {len(analysis.get('dimensions', []))}")

        # Show expert recommendations count
        expert_count = result.get("expert_recommendations_count", 0)
        if expert_count:
            print(f"\n📚 EXPERT KNOWLEDGE")
            print("━" * 70)
            print(f"Applied {expert_count} expert best practices from Anthropic, OpenAI, and research")

        # Show checkpoints
        checkpoints = result.get("checkpoints", [])
        if checkpoints:
            print(f"\n💾 CHECKPOINTS")
            print("━" * 70)
            print(f"Created {len(checkpoints)} checkpoints for rollback/learning")

        print("\n" + "=" * 70 + "\n")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}\n")


def main():
    """Main entry point"""
    # Check for API key
    llm_provider = os.getenv("LLM_PROVIDER", "openai").lower()

    if llm_provider == "groq":
        if not os.getenv("GROQ_API_KEY"):
            print("❌ Error: GROQ_API_KEY not set in .env file")
            print("Please add your Groq API key to the .env file")
            sys.exit(1)
    else:
        if not os.getenv("OPENAI_API_KEY"):
            print("❌ Error: OPENAI_API_KEY not set in .env file")
            print("Please add your OpenAI API key to the .env file")
            sys.exit(1)

    # Check if test input provided as argument
    if len(sys.argv) > 1:
        # Single test mode
        test_input = " ".join(sys.argv[1:])
        asyncio.run(single_test_mode(test_input))
    else:
        # Interactive mode
        asyncio.run(interactive_mode())


if __name__ == "__main__":
    main()
