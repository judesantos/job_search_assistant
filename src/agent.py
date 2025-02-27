import logging

from typing import Any, List, Optional
from crewai import Agent

from src.utils.utils import load_config  # Load YAML

logger = logging.getLogger(__name__)


class AgentsFactory:

    def __init__(self, config_path):
        self.config = load_config(config_path)

    def create_agent(
        self,
        agent_type: str,
        llm: Any,
        tools: Optional[List] = None,
        verbose: bool = True,
        allow_delegation: bool = False,
    ) -> Agent:

        agent_config = self.config.get(agent_type)

        if not agent_config:
            raise ValueError(f"No configuration found for {agent_type}")

        if tools is None:
            tools = []

        try:
            return Agent(
                role=agent_config["role"],
                goal=agent_config["goal"],
                backstory=agent_config["backstory"],
                verbose=verbose,
                tools=tools,
                llm=llm,
                allow_delegation=allow_delegation,
            )
        except Exception as e:
            logger.exception(f"Error creating agent: {e}")
            return None
