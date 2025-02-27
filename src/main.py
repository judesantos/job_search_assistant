import logging

from textwrap import dedent
from dotenv import load_dotenv

from src.services.search_jobs import SearchJobs

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


logging.basicConfig(
    filename="logs/crewai.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

if __name__ == "__main__":

    logger.info('Welcome to Career Search!')

    query = input(
        dedent("""Enter a list of keywords relevant to the target job:
               e.g. 'Software Engineer, Python, Azure, Remote'
        """))

    crew = SearchJobs(query, 'US', 'data/sample_resume.txt')
    result = crew.search()

    if result is None:
        logger.error("Job search crew failed to run, please try again.")
        exit()

    print("\n\n########################")
    print("## RESULT")
    print("########################")
    print(result)
