"""
Prompt Engineering Crew Definition
Wrapper for PromptEngineeringCrew to match Masumi template pattern
"""

from prompt_engineering_crew import PromptEngineeringCrew
from logging_config import get_logger


class PromptCrew:
    """Wrapper for PromptEngineeringCrew following Masumi template pattern"""

    def __init__(self, verbose=False, logger=None):
        self.verbose = verbose
        self.logger = logger or get_logger(__name__)
        self.crew = self.create_crew()
        self.logger.info("PromptCrew initialized")

    def create_crew(self):
        """Initialize the PromptEngineeringCrew"""
        self.logger.info("Creating prompt engineering crew")

        # Initialize the actual PromptEngineeringCrew
        crew_instance = PromptEngineeringCrew(verbose=self.verbose, logger=self.logger)

        self.logger.info("Prompt engineering crew setup completed")
        return crew_instance
