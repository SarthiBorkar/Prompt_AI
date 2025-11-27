"""
Checkpoint System with Git Integration
Provides automatic state preservation and recovery with Git-based versioning
"""

import os
import json
import hashlib
import subprocess
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class Checkpoint:
    """Represents a checkpoint in the prompt engineering process"""
    checkpoint_id: str
    timestamp: str
    state: Dict[str, Any]
    reasoning: str
    changes: List[str]
    parent_id: Optional[str] = None
    git_commit_hash: Optional[str] = None


class CheckpointSystem:
    """
    Manages checkpoints with Git integration for prompt engineering
    """

    def __init__(self, checkpoint_dir: str = ".checkpoints"):
        """
        Initialize checkpoint system

        Args:
            checkpoint_dir: Directory to store checkpoint data
        """
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(exist_ok=True)
        self.checkpoints: Dict[str, Checkpoint] = {}
        self.current_checkpoint: Optional[str] = None
        self.git_enabled = self._check_git_repo()

        # Load existing checkpoints
        self._load_checkpoints()

    def create_checkpoint(
        self,
        state: Dict[str, Any],
        reasoning: str,
        changes: List[str],
        auto_commit: bool = True
    ) -> Checkpoint:
        """
        Creates a new checkpoint

        Args:
            state: Current state to checkpoint
            reasoning: Explanation of why this checkpoint was created
            changes: List of changes since last checkpoint
            auto_commit: Whether to automatically create a Git commit

        Returns:
            Created Checkpoint object
        """
        # Generate checkpoint ID
        checkpoint_id = self._generate_checkpoint_id(state)

        # Create checkpoint
        checkpoint = Checkpoint(
            checkpoint_id=checkpoint_id,
            timestamp=datetime.now().isoformat(),
            state=state,
            reasoning=reasoning,
            changes=changes,
            parent_id=self.current_checkpoint
        )

        # Save checkpoint data
        self._save_checkpoint_data(checkpoint)

        # Create Git commit if enabled
        if self.git_enabled and auto_commit:
            commit_hash = self._create_git_commit(checkpoint)
            checkpoint.git_commit_hash = commit_hash

        # Store in memory
        self.checkpoints[checkpoint_id] = checkpoint
        self.current_checkpoint = checkpoint_id

        return checkpoint

    def restore_checkpoint(self, checkpoint_id: str) -> Dict[str, Any]:
        """
        Restores state from a checkpoint

        Args:
            checkpoint_id: ID of checkpoint to restore

        Returns:
            Restored state dictionary
        """
        if checkpoint_id not in self.checkpoints:
            raise ValueError(f"Checkpoint {checkpoint_id} not found")

        checkpoint = self.checkpoints[checkpoint_id]
        self.current_checkpoint = checkpoint_id

        return checkpoint.state

    def get_checkpoint_history(self) -> List[Checkpoint]:
        """
        Gets checkpoint history in chronological order

        Returns:
            List of checkpoints ordered by timestamp
        """
        return sorted(
            self.checkpoints.values(),
            key=lambda c: c.timestamp
        )

    def verify_integrity(self, checkpoint_id: str) -> bool:
        """
        Verifies checkpoint integrity using hash verification

        Args:
            checkpoint_id: ID of checkpoint to verify

        Returns:
            True if checkpoint is valid, False otherwise
        """
        if checkpoint_id not in self.checkpoints:
            return False

        checkpoint = self.checkpoints[checkpoint_id]
        checkpoint_file = self.checkpoint_dir / f"{checkpoint_id}.json"

        if not checkpoint_file.exists():
            return False

        # Verify hash
        expected_hash = checkpoint_id
        actual_hash = self._generate_checkpoint_id(checkpoint.state)

        return expected_hash == actual_hash

    def get_changes_since(self, checkpoint_id: str) -> List[str]:
        """
        Gets list of changes since a specific checkpoint

        Args:
            checkpoint_id: Starting checkpoint ID

        Returns:
            List of changes
        """
        if checkpoint_id not in self.checkpoints:
            return []

        changes = []
        current = self.current_checkpoint

        while current and current != checkpoint_id:
            checkpoint = self.checkpoints.get(current)
            if not checkpoint:
                break
            changes.extend(checkpoint.changes)
            current = checkpoint.parent_id

        return list(reversed(changes))

    def rollback_to(self, checkpoint_id: str) -> Dict[str, Any]:
        """
        Rolls back to a specific checkpoint

        Args:
            checkpoint_id: Checkpoint to roll back to

        Returns:
            Restored state
        """
        state = self.restore_checkpoint(checkpoint_id)

        # Create a rollback checkpoint
        self.create_checkpoint(
            state=state,
            reasoning=f"Rolled back to checkpoint {checkpoint_id}",
            changes=[f"Rollback to {checkpoint_id}"],
            auto_commit=True
        )

        return state

    def _check_git_repo(self) -> bool:
        """Checks if current directory is a Git repository"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def _create_git_commit(self, checkpoint: Checkpoint) -> Optional[str]:
        """Creates a Git commit for the checkpoint"""
        try:
            # Add checkpoint file
            checkpoint_file = self.checkpoint_dir / f"{checkpoint.checkpoint_id}.json"
            subprocess.run(
                ["git", "add", str(checkpoint_file)],
                check=True,
                capture_output=True
            )

            # Create commit message
            commit_message = f"Checkpoint: {checkpoint.reasoning}\n\nChanges:\n"
            commit_message += "\n".join([f"- {change}" for change in checkpoint.changes])

            # Commit
            result = subprocess.run(
                ["git", "commit", "-m", commit_message],
                capture_output=True,
                text=True,
                check=False
            )

            if result.returncode == 0:
                # Get commit hash
                hash_result = subprocess.run(
                    ["git", "rev-parse", "HEAD"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                return hash_result.stdout.strip()
            else:
                # Nothing to commit or error
                return None

        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    def _generate_checkpoint_id(self, state: Dict[str, Any]) -> str:
        """Generates a unique checkpoint ID from state"""
        state_str = json.dumps(state, sort_keys=True)
        timestamp = datetime.now().isoformat()
        combined = f"{state_str}{timestamp}"
        return hashlib.sha256(combined.encode()).hexdigest()[:16]

    def _save_checkpoint_data(self, checkpoint: Checkpoint):
        """Saves checkpoint data to file"""
        checkpoint_file = self.checkpoint_dir / f"{checkpoint.checkpoint_id}.json"

        data = {
            "checkpoint_id": checkpoint.checkpoint_id,
            "timestamp": checkpoint.timestamp,
            "state": checkpoint.state,
            "reasoning": checkpoint.reasoning,
            "changes": checkpoint.changes,
            "parent_id": checkpoint.parent_id,
            "git_commit_hash": checkpoint.git_commit_hash
        }

        with open(checkpoint_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _load_checkpoints(self):
        """Loads existing checkpoints from disk"""
        if not self.checkpoint_dir.exists():
            return

        for checkpoint_file in self.checkpoint_dir.glob("*.json"):
            try:
                with open(checkpoint_file, 'r') as f:
                    data = json.load(f)

                checkpoint = Checkpoint(
                    checkpoint_id=data["checkpoint_id"],
                    timestamp=data["timestamp"],
                    state=data["state"],
                    reasoning=data["reasoning"],
                    changes=data["changes"],
                    parent_id=data.get("parent_id"),
                    git_commit_hash=data.get("git_commit_hash")
                )

                self.checkpoints[checkpoint.checkpoint_id] = checkpoint

                # Update current checkpoint to the most recent
                if (not self.current_checkpoint or
                        checkpoint.timestamp > self.checkpoints[self.current_checkpoint].timestamp):
                    self.current_checkpoint = checkpoint.checkpoint_id

            except (json.JSONDecodeError, KeyError):
                # Skip corrupted checkpoint files
                continue

    def get_checkpoint(self, checkpoint_id: str) -> Optional[Checkpoint]:
        """Gets a specific checkpoint by ID"""
        return self.checkpoints.get(checkpoint_id)

    def list_checkpoints(self) -> List[Dict[str, Any]]:
        """Lists all checkpoints with summary information"""
        return [
            {
                "id": cp.checkpoint_id,
                "timestamp": cp.timestamp,
                "reasoning": cp.reasoning,
                "num_changes": len(cp.changes),
                "has_git_commit": cp.git_commit_hash is not None
            }
            for cp in self.get_checkpoint_history()
        ]

    def export_checkpoint(self, checkpoint_id: str, output_path: str):
        """Exports a checkpoint to a file"""
        checkpoint = self.get_checkpoint(checkpoint_id)
        if not checkpoint:
            raise ValueError(f"Checkpoint {checkpoint_id} not found")

        with open(output_path, 'w') as f:
            json.dump({
                "checkpoint_id": checkpoint.checkpoint_id,
                "timestamp": checkpoint.timestamp,
                "state": checkpoint.state,
                "reasoning": checkpoint.reasoning,
                "changes": checkpoint.changes
            }, f, indent=2)

    def import_checkpoint(self, input_path: str) -> Checkpoint:
        """Imports a checkpoint from a file"""
        with open(input_path, 'r') as f:
            data = json.load(f)

        checkpoint = Checkpoint(
            checkpoint_id=data["checkpoint_id"],
            timestamp=data["timestamp"],
            state=data["state"],
            reasoning=data["reasoning"],
            changes=data["changes"],
            parent_id=None  # Imported checkpoints start new lineage
        )

        self._save_checkpoint_data(checkpoint)
        self.checkpoints[checkpoint.checkpoint_id] = checkpoint

        return checkpoint
