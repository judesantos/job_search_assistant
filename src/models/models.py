"""
The models module contains the data models used in the project.
Classes:
    Job: A data model representing a job.
    JobResults: A data model representing a list of jobs.
"""

from typing import List, Optional
from pydantic import BaseModel


class Job(BaseModel):
    id: Optional[str]
    location: Optional[str]
    title: Optional[str]
    company: Optional[str]
    description: Optional[str]
    provider: Optional[str]
    url: Optional[str]
    rating: Optional[int]
    rating_notes: Optional[str]
    company_rating: Optional[int]
    company_notes: Optional[str]


class JobResults(BaseModel):
    jobs: Optional[List[Job]]
