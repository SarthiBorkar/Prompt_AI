"""
Continuous Learning System
Makes the agent learn from each interaction and improve over time
Uses checkpoints + feedback to evolve techniques
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import statistics


@dataclass
class LearningRecord:
    """Record of a single learning event"""
    timestamp: str
    input_description: str
    techniques_used: List[str]
    quality_score: float
    user_feedback: Optional[float]  # 1-5 rating
    success: bool
    time_taken: float
    token_count: int
    checkpoint_id: Optional[str]


class ContinuousLearningSystem:
    """
    Learns from every interaction to improve future performance
    Tracks what works, what doesn't, and adapts accordingly
    """

    def __init__(self, storage_path: str = ".learning"):
        """
        Initialize learning system

        Args:
            storage_path: Directory to store learning data
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)

        self.records_file = self.storage_path / "learning_records.jsonl"
        self.insights_file = self.storage_path / "insights.json"
        self.technique_performance_file = self.storage_path / "technique_performance.json"

        # Load existing data
        self.records = self._load_records()
        self.insights = self._load_insights()
        self.technique_performance = self._load_technique_performance()

    def record_interaction(
        self,
        input_description: str,
        techniques_used: List[str],
        quality_score: float,
        success: bool,
        time_taken: float,
        token_count: int,
        checkpoint_id: Optional[str] = None,
        user_feedback: Optional[float] = None
    ):
        """
        Record a learning event

        Args:
            input_description: What the user asked for
            techniques_used: Which techniques were applied
            quality_score: Evaluation score (0-100)
            success: Whether task succeeded
            time_taken: Processing time in seconds
            token_count: Estimated tokens used
            checkpoint_id: Associated checkpoint
            user_feedback: Optional user rating (1-5)
        """
        record = LearningRecord(
            timestamp=datetime.now().isoformat(),
            input_description=input_description,
            techniques_used=techniques_used,
            quality_score=quality_score,
            user_feedback=user_feedback,
            success=success,
            time_taken=time_taken,
            token_count=token_count,
            checkpoint_id=checkpoint_id
        )

        # Append to records
        with open(self.records_file, 'a') as f:
            f.write(json.dumps(asdict(record)) + '\n')

        # Update in-memory
        self.records.append(record)

        # Update technique performance
        self._update_technique_performance(record)

        # Generate insights periodically
        if len(self.records) % 10 == 0:  # Every 10 interactions
            self._generate_insights()

    def get_recommended_techniques(self, task_description: str) -> List[str]:
        """
        Recommend techniques based on learning history

        Args:
            task_description: Description of current task

        Returns:
            List of recommended technique names
        """
        # Simple keyword-based recommendation enhanced by performance data
        recommendations = []

        task_lower = task_description.lower()

        # Check technique performance history
        for technique, stats in self.technique_performance.items():
            if stats["success_rate"] > 0.7 and stats["avg_quality_score"] > 75:
                # This technique has proven effective

                # Match to task type
                if technique == "chain_of_thought" and any(
                    word in task_lower for word in ["analyze", "reason", "think", "complex"]
                ):
                    recommendations.append(technique)

                elif technique == "react" and any(
                    word in task_lower for word in ["agent", "action", "tool", "step"]
                ):
                    recommendations.append(technique)

                elif technique == "few_shot" and any(
                    word in task_lower for word in ["example", "format", "pattern"]
                ):
                    recommendations.append(technique)

                elif technique == "agent_to_agent" and any(
                    word in task_lower for word in ["agent", "communication", "protocol"]
                ):
                    recommendations.append(technique)

        # If no recommendations yet, use most successful techniques overall
        if not recommendations:
            sorted_techniques = sorted(
                self.technique_performance.items(),
                key=lambda x: (x[1]["success_rate"], x[1]["avg_quality_score"]),
                reverse=True
            )
            recommendations = [t[0] for t in sorted_techniques[:3]]

        return recommendations

    def get_performance_trend(self) -> Dict[str, Any]:
        """Get performance trends over time"""
        if len(self.records) < 5:
            return {"status": "insufficient_data", "interactions": len(self.records)}

        # Recent records (last 20)
        recent = self.records[-20:]

        # Calculate trends
        quality_scores = [r.quality_score for r in recent if r.quality_score]
        success_rate = sum(1 for r in recent if r.success) / len(recent)
        avg_quality = statistics.mean(quality_scores) if quality_scores else 0
        avg_time = statistics.mean([r.time_taken for r in recent])

        # Compare to earlier data
        if len(self.records) > 40:
            earlier = self.records[-40:-20]
            earlier_quality = statistics.mean([r.quality_score for r in earlier if r.quality_score]) or 0
            earlier_success = sum(1 for r in earlier if r.success) / len(earlier)

            quality_trend = ((avg_quality - earlier_quality) / earlier_quality * 100) if earlier_quality else 0
            success_trend = ((success_rate - earlier_success) / earlier_success * 100) if earlier_success else 0
        else:
            quality_trend = 0
            success_trend = 0

        return {
            "status": "active",
            "total_interactions": len(self.records),
            "recent_success_rate": round(success_rate * 100, 1),
            "recent_avg_quality": round(avg_quality, 1),
            "recent_avg_time": round(avg_time, 2),
            "quality_trend": round(quality_trend, 1),  # % change
            "success_trend": round(success_trend, 1),  # % change
            "improvement": "improving" if quality_trend > 5 else "stable" if quality_trend > -5 else "declining"
        }

    def get_insights(self) -> Dict[str, Any]:
        """Get current insights from learning"""
        return self.insights

    def _load_records(self) -> List[LearningRecord]:
        """Load historical records"""
        if not self.records_file.exists():
            return []

        records = []
        with open(self.records_file, 'r') as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    records.append(LearningRecord(**data))

        return records

    def _load_insights(self) -> Dict:
        """Load generated insights"""
        if not self.insights_file.exists():
            return {}

        with open(self.insights_file, 'r') as f:
            return json.load(f)

    def _load_technique_performance(self) -> Dict:
        """Load technique performance data"""
        if not self.technique_performance_file.exists():
            return {}

        with open(self.technique_performance_file, 'r') as f:
            return json.load(f)

    def _update_technique_performance(self, record: LearningRecord):
        """Update performance stats for techniques used"""
        for technique in record.techniques_used:
            if technique not in self.technique_performance:
                self.technique_performance[technique] = {
                    "uses": 0,
                    "successes": 0,
                    "total_quality_score": 0,
                    "success_rate": 0.0,
                    "avg_quality_score": 0.0
                }

            stats = self.technique_performance[technique]
            stats["uses"] += 1
            stats["successes"] += 1 if record.success else 0
            stats["total_quality_score"] += record.quality_score

            # Update averages
            stats["success_rate"] = stats["successes"] / stats["uses"]
            stats["avg_quality_score"] = stats["total_quality_score"] / stats["uses"]

        # Save updated stats
        with open(self.technique_performance_file, 'w') as f:
            json.dump(self.technique_performance, f, indent=2)

    def _generate_insights(self):
        """Generate insights from accumulated data"""
        if len(self.records) < 10:
            return

        insights = {
            "generated_at": datetime.now().isoformat(),
            "total_interactions": len(self.records),
            "top_techniques": self._get_top_techniques(),
            "improvement_areas": self._identify_improvement_areas(),
            "success_patterns": self._identify_success_patterns(),
            "recommendations": self._generate_recommendations()
        }

        self.insights = insights

        # Save insights
        with open(self.insights_file, 'w') as f:
            json.dump(insights, f, indent=2)

    def _get_top_techniques(self) -> List[Dict]:
        """Get best performing techniques"""
        sorted_techniques = sorted(
            self.technique_performance.items(),
            key=lambda x: (x[1]["avg_quality_score"], x[1]["success_rate"]),
            reverse=True
        )

        return [
            {
                "technique": name,
                "avg_quality": round(stats["avg_quality_score"], 1),
                "success_rate": round(stats["success_rate"] * 100, 1),
                "uses": stats["uses"]
            }
            for name, stats in sorted_techniques[:5]
        ]

    def _identify_improvement_areas(self) -> List[str]:
        """Identify areas needing improvement"""
        areas = []

        # Check recent success rate
        recent = self.records[-20:] if len(self.records) >= 20 else self.records
        success_rate = sum(1 for r in recent if r.success) / len(recent) if recent else 0

        if success_rate < 0.8:
            areas.append("Overall success rate could be improved")

        # Check quality scores
        quality_scores = [r.quality_score for r in recent if r.quality_score]
        avg_quality = statistics.mean(quality_scores) if quality_scores else 0

        if avg_quality < 75:
            areas.append("Prompt quality scores below target (75)")

        # Check time efficiency
        avg_time = statistics.mean([r.time_taken for r in recent])
        if avg_time > 90:
            areas.append("Processing time could be optimized")

        return areas if areas else ["All metrics performing well"]

    def _identify_success_patterns(self) -> List[str]:
        """Identify what makes successful prompts"""
        patterns = []

        successful = [r for r in self.records if r.success and r.quality_score >= 80]
        if len(successful) >= 5:
            # Find common techniques
            technique_counts = {}
            for record in successful:
                for technique in record.techniques_used:
                    technique_counts[technique] = technique_counts.get(technique, 0) + 1

            top_techniques = sorted(technique_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            for technique, count in top_techniques:
                patterns.append(f"{technique} used in {count}/{len(successful)} high-quality prompts")

        return patterns if patterns else ["Collecting more data to identify patterns"]

    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        # Based on performance data
        trend = self.get_performance_trend()
        if trend.get("status") == "active":
            if trend["improvement"] == "declining":
                recommendations.append("Consider revisiting successful earlier techniques")
                recommendations.append("Review and refine current approach")
            elif trend["improvement"] == "improving":
                recommendations.append("Current strategy is working well - continue")

        # Based on technique performance
        underperforming = [
            name for name, stats in self.technique_performance.items()
            if stats["uses"] > 3 and stats["avg_quality_score"] < 65
        ]

        if underperforming:
            recommendations.append(f"Consider alternatives to: {', '.join(underperforming)}")

        return recommendations if recommendations else ["Keep learning - more data needed for specific recommendations"]

    def export_learning_summary(self) -> str:
        """Export a human-readable learning summary"""
        trend = self.get_performance_trend()

        summary = f"""
# CONTINUOUS LEARNING SUMMARY

## Performance Metrics
- Total Interactions: {len(self.records)}
- Recent Success Rate: {trend.get('recent_success_rate', 'N/A')}%
- Recent Avg Quality: {trend.get('recent_avg_quality', 'N/A')}/100
- Trend: {trend.get('improvement', 'collecting data').upper()}

## Top Performing Techniques
{chr(10).join(f"- {t['technique']}: {t['avg_quality']}/100 quality, {t['success_rate']}% success ({t['uses']} uses)" for t in self._get_top_techniques())}

## Insights
{chr(10).join(f"- {pattern}" for pattern in self._identify_success_patterns())}

## Improvement Areas
{chr(10).join(f"- {area}" for area in self._identify_improvement_areas())}

## Recommendations
{chr(10).join(f"- {rec}" for rec in self._generate_recommendations())}

---
Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return summary
