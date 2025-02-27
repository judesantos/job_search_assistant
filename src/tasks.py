"""
This module contains factory classes for creating tasks.
Classes:
    TasksFactory: A class for creating tasks based on a configuration file.
"""

import logging

from textwrap import dedent
from typing import Optional
from crewai import Agent, Task

from src.utils.utils import load_config  # Load YAML

logger = logging.getLogger(__name__)


class TasksFactory:
    """
    TasksFactory class is responsible for creating tasks based on
    the configuration file provided. The create_task method takes
    task_type, agent, query, and output_schema as input and returns
    a Task object. The Task object is created using the description
    and expected_output from the configuration file. If the query and
    output_schema are provided, they are formatted into the description
    and expected_output respectively. If no configuration is found for
    the task_type, a ValueError is raised. The expected_output is dedented
    before creating the Task object.

    Attributes:
        config (dict): The configuration dictionary loaded from the
            configuration file.

    Methods:
        create_task: Create a Task object based on the task_type, agent,
            query, and output_schema.
    """

    def __init__(self, config_path):
        """
        Initialize the TasksFactory with the configuration file path.
        The configuration file is loaded using the load_config function
        from the utils module.
        Args:
            config_path (str): The path to the configuration file.
        """
        self.config = load_config(config_path)

    def create_task(
        self,
        task_type: str,
        agent: Agent,
        query: Optional[str] = None,
        output_schema: Optional[str] = None,
    ):
        """
        Create a Task object based on the task_type, agent, query, and
        output_schema.
        Args:
            task_type (str): The type of task to create.
            agent (Agent): The agent to use for the task.
            query (str, optional): The query to format into the description.
            output_schema (str, optional): The output_schema to format into
                the expected_output.
        Returns:
            Task: The Task object created based on the task_type, agent,
                query, and output_schema.
        """
        task_config = self.config.get(task_type)

        if not task_config:
            raise ValueError(f"No configuration found for {task_type}")

        description = task_config["description"]

        if "{query}" in description and query is not None:
            description = description.format(query=query)

        expected_output = task_config["expected_output"]

        if "{output_schema}" in expected_output and output_schema is not None:
            expected_output = expected_output.format(
                output_schema=output_schema)

        try:
            return Task(
                description=dedent(description),
                expected_output=dedent(expected_output),
                agent=agent,
            )
        except Exception as e:
            logger.exception(f"Error creating task: {e}")
            return None
