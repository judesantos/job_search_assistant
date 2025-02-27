"""
This module provides a class to query jobs from Jooble API.
Classes:
    Jooble: A class to query jobs from Jooble API.
    JoobleSearchTool: A crewai custom tool to be uses in the crewai framework
        to search jobs. Encapsulates the Jooble class.
"""
import json
import requests
import logging

from crewai_tools import BaseTool

logger = logging.getLogger(__name__)


class Jooble:
    """
    Jooble class to query jobs by using external API.
    Attributes:
        query (str): The job query to search for.
    Methods:
        query_jobs: Query jobs from Jooble API.
    """

    def __init__(self, host, key):
        self.host = host
        self.key = key

    def search(self, keywords, location) -> str | None:
        """
        Query jobs from Jooble API.
        Args:
            query (str): The job query to search for.
        Returns:
            response (dict): The response from Jooble API.
        """

        # Create connection
        # connection = http.client.HTTPConnection(self.host)

        # Setup request
        # 1. headers
        headers = {"Content-type": "application/json"}
        # 2. json formatted query body
        body = {'keywords': f'{keywords}', 'location': f'{location}'}

        # 3. send request
        try:
            # Send request
            response = requests.post(
                f'http://{self.host}/api/{self.key}',
                json=body,
                headers=headers
            )

        except Exception as e:
            logger.error(f"Error: {e}")
            return None

        # 4. Check response status send response

        if response.status_code != 200:
            logger.error(f"Error: {response.reason}")
            return None
        else:
            # Process response
            json_response = response.json()
            return json.dumps(json_response, indent=2)


class JoobleSearchTool(BaseTool):
    """
    Implementation of a tool to fetch json data from an external source (jooble)
    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
        query (str): The query to search for.
        location (str): The location to search for.
        host (str): The host of the external source.
        key (str): The API key to access the external source.
    Methods:
        _run: Fetch json data from the external source.
    """

    name: str = "json_tool"
    description: str = "Tool to read json data"

    query: str = ''
    location: str = ''
    host: str = ''
    key: str = ''

    def __init__(self, host, key, query, location, **kwargs):
        super().__init__(**kwargs)

        self.query = query
        self.location = location
        self.host = host
        self.key = key

    def _run(self):
        """
        Run the tool to fetch jobs and return json data
        Returns:
            str: The json data response
        Exceptions:
            Exception: If the response is not valid
        """
        # Fetch jobs from external sources
        jooble = Jooble(self.host, self.key)
        jobs = jooble.search(self.query, self.location)
        if jobs is None:
            logger.error("Failed to fetch jobs from Jooble")
            raise Exception("Failed to fetch jobs from Jooble")
        else:
            return jobs
