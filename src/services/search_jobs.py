"""
This module uses CrewAI library to create a job search crew in
the JobSearchCrew class.

The JobSearchCrew class takes a keywords as input and runs
a job search crew to find relevant jobs based on the keywords.
The crew consists of four agents: job_search_expert_agent,
job_rating_expert_agent, company_rating_expert_agent,
and summarization_expert_agent.

The crew performs the following tasks:
1. Job search: Find relevant jobs based on the keywords.
2. Job rating: Rate the jobs based on the user's resume.
3. Evaluate company: Evaluate the companies that offer the jobs.
4. Structure results: Summarize the results and structure them into
    a JSON format.

The crew uses the AzureChatOpenAI language model for generating responses.
The crew is created using the Crew class from the CrewAI library,
and the agents and tasks are created using the AgentsFactory and
TasksFactory classes.
The crew is then kicked off, and the result is validated using the
JobResults model schema.

If the result is valid, it is printed; otherwise, an error message is displayed.
"""

import logging
import json
import os

from crewai import Crew, Process
from crewai_tools import FileReadTool, SerperDevTool
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

from src.agent import AgentsFactory
from src.models.models import JobResults
from src.tasks import TasksFactory
from src.services.jooble import JoobleSearchTool

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

logger = logging.getLogger(__name__)


class SearchJobs:
    """
    SearchJobs class is responsible for running a job search crew
    based on the keywords provided. The keywords is used to find relevant jobs
    using the job_search_expert_agent, rate the jobs based on the user's
    resume using the job_rating_expert_agent, evaluate the companies that
    offer the jobs using the company_rating_expert_agent, and summarize
    the results using the summarization_expert_agent. The crew is created
    using the Crew class from the CrewAI library, and the agents and tasks
    are created using the AgentsFactory and TasksFactory classes.
    Attributes:
        keywords (str): The keywords for finding relevant jobs.
    Methods:
        search: search jobs and return the result
    """

    def __init__(self, keywords: str, location: str, resume: str):
        self.keywords = keywords
        self.location = location
        self.resume = resume

    def search(self) -> str:
        """
        Run the job search crew and return the result.
        Search Steps:
            1. Job search: Find relevant jobs based on the keywords.
            2. Job rating: Rate the jobs based on the user's resume.
            3. Evaluate company: Evaluate the companies that offer the jobs.
            4. Structure results: Summarize the results and structure them into
                a JSON format.
            5. Return the result.
        Returns:
            result (str): The result of the job search crew.
        """

        logger.info('Running Job Search Crew...')
        verbose = False

        try:
            # 1. Define the LLM the AI Agents will use

            # Load environment variables
            az_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
            az_key = os.environ.get("AZURE_OPENAI_KEY")
            deployment_name = "gpt-4"

            azure_llm = AzureChatOpenAI(
                deployment_name=deployment_name,
                azure_endpoint=az_endpoint,
                api_key=az_key,
                api_version="2023-12-01-preview",
                streaming=True,
                temperature=0,
                verbose=verbose
            )

            # 2. Create the data sources

            # Resume reader tool
            resume_file_read_tool = FileReadTool(
                file_path=self.resume)
            # file_path="data/sample_resume.txt")

            # Jobs search and reader tool
            jooble_search_tool = JoobleSearchTool(
                host=os.environ.get("JOOBLE_HOST"),
                key=os.environ.get("JOOBLE_API_KEY"),
                keywords=self.keywords,
                location=self.location,
                verbose=verbose
            )

            # 3. Create serper seeach tool for company rating

            search_tool = SerperDevTool(n_results=5)

            # 4. Setup the Agents pipeline for the Crew

            # Create the agent with the processing steps
            agent_factory = AgentsFactory("configs/agents.yml")

            # Agent Step 1: Search Jobs based on the keywords
            job_search_expert_agent = agent_factory.create_agent(
                "job_search_expert", tools=[jooble_search_tool], llm=azure_llm, verbose=verbose
            )
            # Agent Step 2: Rate the jobs based on the user's resume
            job_rating_expert_agent = agent_factory.create_agent(
                "job_rating_expert", tools=[resume_file_read_tool], llm=azure_llm, verbose=verbose
            )
            # Agent Step 3: Evaluate the companies that offer the jobs
            company_rating_expert_agent = agent_factory.create_agent(
                "company_rating_expert", tools=[search_tool], llm=azure_llm, verbose=verbose
            )
            # Agent Step 4: Summarize the results
            summarization_expert_agent = agent_factory.create_agent(
                "summarization_expert", tools=None, llm=azure_llm, verbose=verbose
            )

            # Response model schema
            response_schema = json.dumps(
                JobResults.model_json_schema(), indent=2)

            # 5. Setup the Tasks for the Crew

            # Create the tasks pipeline with the processing steps
            tasks_factory = TasksFactory("configs/tasks.yml")
            # Task Step 1: Search Jobs based on the keywords
            job_search_task = tasks_factory.create_task(
                "job_search", job_search_expert_agent, keywords=self.keywords
            )
            # Task Step 2: Rate the jobs based on the user's resume
            job_rating_task = tasks_factory.create_task(
                "job_rating", job_rating_expert_agent
            )
            # Task Step 3: Evaluate the companies that offer the jobs
            evaluate_company_task = tasks_factory.create_task(
                "evaluate_company",
                company_rating_expert_agent,
                output_schema=response_schema,
            )
            # Task Step 4: Summarize the results
            structure_results_task = tasks_factory.create_task(
                "structure_results",
                summarization_expert_agent,
                output_schema=response_schema,
            )

            # 6 Build a Crew

            crew = Crew(
                agents=[
                    job_search_expert_agent,
                    job_rating_expert_agent,
                    company_rating_expert_agent,
                    summarization_expert_agent,
                ],
                tasks=[
                    job_search_task,
                    job_rating_task,
                    evaluate_company_task,
                    structure_results_task,
                ],
                verbose=verbose,
                process=Process.sequential,
            )

            # 7. Launch the Crew

            result = crew.kickoff()
            return result

        except Exception as e:
            logger.error(f"JobSearchCrew::run() Error: {e}")
            return None
