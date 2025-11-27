"""
Context Manager Module
Manages context across interactions with JSON-based persistence
"""

import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class UserProfile:
    """User profile with preferences and history"""
    user_id: str
    created_at: str
    last_active: str
    preferred_style: str = "structured"  # structured, minimal, conversational
    common_use_cases: List[str] = field(default_factory=list)
    refinement_patterns: Dict[str, int] = field(default_factory=dict)
    total_prompts: int = 0
    average_iterations: float = 0.0


@dataclass
class ConversationContext:
    """Context for a conversation or session"""
    conversation_id: str
    user_id: Optional[str]
    started_at: str
    last_updated: str
    messages: List[Dict[str, Any]] = field(default_factory=list)
    current_prompt: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentContext:
    """Context for agent-to-agent interactions on Masumi"""
    agent_id: str
    relationship_started: str
    last_interaction: str
    total_transactions: int = 0
    service_agreements: List[Dict[str, Any]] = field(default_factory=list)
    conversation_history: List[str] = field(default_factory=list)
    payment_history: List[Dict[str, Any]] = field(default_factory=list)


class ContextManager:
    """
    Manages context across user and agent interactions with JSON persistence
    """

    def __init__(self, storage_dir: str = ".context"):
        """
        Initialize context manager

        Args:
            storage_dir: Directory for storing context data
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)

        # Create subdirectories
        (self.storage_dir / "users").mkdir(exist_ok=True)
        (self.storage_dir / "conversations").mkdir(exist_ok=True)
        (self.storage_dir / "agents").mkdir(exist_ok=True)

        # In-memory caches
        self.user_profiles: Dict[str, UserProfile] = {}
        self.conversations: Dict[str, ConversationContext] = {}
        self.agent_contexts: Dict[str, AgentContext] = {}

    # ─────────────────────────────────────────────────────────────────────
    # User Profile Management
    # ─────────────────────────────────────────────────────────────────────

    def get_user_profile(self, user_id: str) -> UserProfile:
        """
        Gets or creates a user profile

        Args:
            user_id: User identifier

        Returns:
            UserProfile instance
        """
        if user_id in self.user_profiles:
            return self.user_profiles[user_id]

        # Try to load from disk
        profile_path = self.storage_dir / "users" / f"{user_id}.json"
        if profile_path.exists():
            with open(profile_path, 'r') as f:
                data = json.load(f)
                profile = UserProfile(**data)
                self.user_profiles[user_id] = profile
                return profile

        # Create new profile
        profile = UserProfile(
            user_id=user_id,
            created_at=datetime.now().isoformat(),
            last_active=datetime.now().isoformat()
        )
        self.user_profiles[user_id] = profile
        self._save_user_profile(profile)
        return profile

    def update_user_profile(self, user_id: str, **kwargs):
        """
        Updates user profile with new information

        Args:
            user_id: User identifier
            **kwargs: Fields to update
        """
        profile = self.get_user_profile(user_id)

        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)

        profile.last_active = datetime.now().isoformat()
        self._save_user_profile(profile)

    def record_prompt_creation(self, user_id: str, style: str, iterations: int):
        """
        Records prompt creation for learning user preferences

        Args:
            user_id: User identifier
            style: Prompt style used
            iterations: Number of iterations needed
        """
        profile = self.get_user_profile(user_id)

        # Update statistics
        profile.total_prompts += 1

        # Update average iterations
        current_avg = profile.average_iterations
        n = profile.total_prompts
        profile.average_iterations = ((current_avg * (n - 1)) + iterations) / n

        # Track preferred style
        if style not in profile.refinement_patterns:
            profile.refinement_patterns[style] = 0
        profile.refinement_patterns[style] += 1

        # Update preferred style to the most common
        if profile.refinement_patterns:
            profile.preferred_style = max(
                profile.refinement_patterns,
                key=profile.refinement_patterns.get
            )

        self._save_user_profile(profile)

    def _save_user_profile(self, profile: UserProfile):
        """Saves user profile to disk"""
        profile_path = self.storage_dir / "users" / f"{profile.user_id}.json"
        with open(profile_path, 'w') as f:
            json.dump(profile.__dict__, f, indent=2)

    # ─────────────────────────────────────────────────────────────────────
    # Conversation Context Management
    # ─────────────────────────────────────────────────────────────────────

    def create_conversation(
        self,
        user_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Creates a new conversation context

        Args:
            user_id: Optional user identifier
            metadata: Optional metadata

        Returns:
            Conversation ID
        """
        conversation_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.conversations)}"

        conversation = ConversationContext(
            conversation_id=conversation_id,
            user_id=user_id,
            started_at=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat(),
            metadata=metadata or {}
        )

        self.conversations[conversation_id] = conversation
        self._save_conversation(conversation)

        return conversation_id

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: Any,
        metadata: Optional[Dict] = None
    ):
        """
        Adds a message to a conversation

        Args:
            conversation_id: Conversation identifier
            role: Message role (user, assistant, system)
            content: Message content
            metadata: Optional metadata
        """
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = self._load_conversation(conversation_id)

        conversation = self.conversations[conversation_id]

        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }

        conversation.messages.append(message)
        conversation.last_updated = datetime.now().isoformat()

        self._save_conversation(conversation)

    def get_conversation_history(
        self,
        conversation_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Gets conversation history

        Args:
            conversation_id: Conversation identifier
            limit: Optional limit on number of messages

        Returns:
            List of messages
        """
        if conversation_id not in self.conversations:
            conversation = self._load_conversation(conversation_id)
            if conversation:
                self.conversations[conversation_id] = conversation

        conversation = self.conversations.get(conversation_id)
        if not conversation:
            return []

        messages = conversation.messages
        if limit:
            messages = messages[-limit:]

        return messages

    def update_current_prompt(self, conversation_id: str, prompt_data: Dict[str, Any]):
        """
        Updates the current prompt being worked on in a conversation

        Args:
            conversation_id: Conversation identifier
            prompt_data: Prompt data to store
        """
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = self._load_conversation(conversation_id)

        conversation = self.conversations[conversation_id]
        conversation.current_prompt = prompt_data
        conversation.last_updated = datetime.now().isoformat()

        self._save_conversation(conversation)

    def _save_conversation(self, conversation: ConversationContext):
        """Saves conversation to disk"""
        conv_path = self.storage_dir / "conversations" / f"{conversation.conversation_id}.json"
        with open(conv_path, 'w') as f:
            json.dump({
                "conversation_id": conversation.conversation_id,
                "user_id": conversation.user_id,
                "started_at": conversation.started_at,
                "last_updated": conversation.last_updated,
                "messages": conversation.messages,
                "current_prompt": conversation.current_prompt,
                "metadata": conversation.metadata
            }, f, indent=2)

    def _load_conversation(self, conversation_id: str) -> Optional[ConversationContext]:
        """Loads conversation from disk"""
        conv_path = self.storage_dir / "conversations" / f"{conversation_id}.json"
        if not conv_path.exists():
            return None

        with open(conv_path, 'r') as f:
            data = json.load(f)
            return ConversationContext(**data)

    # ─────────────────────────────────────────────────────────────────────
    # Agent Context Management (for Masumi Network)
    # ─────────────────────────────────────────────────────────────────────

    def get_agent_context(self, agent_id: str) -> AgentContext:
        """
        Gets or creates agent context for agent-to-agent interactions

        Args:
            agent_id: Agent identifier

        Returns:
            AgentContext instance
        """
        if agent_id in self.agent_contexts:
            return self.agent_contexts[agent_id]

        # Try to load from disk
        agent_path = self.storage_dir / "agents" / f"{agent_id}.json"
        if agent_path.exists():
            with open(agent_path, 'r') as f:
                data = json.load(f)
                context = AgentContext(**data)
                self.agent_contexts[agent_id] = context
                return context

        # Create new context
        context = AgentContext(
            agent_id=agent_id,
            relationship_started=datetime.now().isoformat(),
            last_interaction=datetime.now().isoformat()
        )
        self.agent_contexts[agent_id] = context
        self._save_agent_context(context)
        return context

    def record_agent_transaction(
        self,
        agent_id: str,
        transaction_data: Dict[str, Any]
    ):
        """
        Records a transaction with an agent

        Args:
            agent_id: Agent identifier
            transaction_data: Transaction details
        """
        context = self.get_agent_context(agent_id)

        context.total_transactions += 1
        context.payment_history.append({
            "timestamp": datetime.now().isoformat(),
            **transaction_data
        })
        context.last_interaction = datetime.now().isoformat()

        self._save_agent_context(context)

    def add_service_agreement(
        self,
        agent_id: str,
        agreement: Dict[str, Any]
    ):
        """
        Adds a service agreement with an agent

        Args:
            agent_id: Agent identifier
            agreement: Agreement details
        """
        context = self.get_agent_context(agent_id)
        context.service_agreements.append({
            "created_at": datetime.now().isoformat(),
            **agreement
        })
        self._save_agent_context(context)

    def _save_agent_context(self, context: AgentContext):
        """Saves agent context to disk"""
        agent_path = self.storage_dir / "agents" / f"{context.agent_id}.json"
        with open(agent_path, 'w') as f:
            json.dump({
                "agent_id": context.agent_id,
                "relationship_started": context.relationship_started,
                "last_interaction": context.last_interaction,
                "total_transactions": context.total_transactions,
                "service_agreements": context.service_agreements,
                "conversation_history": context.conversation_history,
                "payment_history": context.payment_history
            }, f, indent=2)

    # ─────────────────────────────────────────────────────────────────────
    # Utility Methods
    # ─────────────────────────────────────────────────────────────────────

    def clear_old_conversations(self, days: int = 30):
        """
        Clears conversations older than specified days

        Args:
            days: Age threshold in days
        """
        cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)

        for conv_file in (self.storage_dir / "conversations").glob("*.json"):
            if conv_file.stat().st_mtime < cutoff:
                conv_file.unlink()

    def get_statistics(self) -> Dict[str, Any]:
        """
        Gets context manager statistics

        Returns:
            Dictionary with statistics
        """
        return {
            "total_users": len(list((self.storage_dir / "users").glob("*.json"))),
            "total_conversations": len(list((self.storage_dir / "conversations").glob("*.json"))),
            "total_agents": len(list((self.storage_dir / "agents").glob("*.json"))),
            "active_conversations": len(self.conversations),
            "cached_profiles": len(self.user_profiles),
            "cached_agents": len(self.agent_contexts)
        }
