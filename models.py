from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Literal


class Repository(BaseModel):
    github_id: int = Field(..., alias='id')
    name: str = Field(..., alias='full_name')
    url: str = Field(..., alias='html_url')
    description: str | None = Field(None, alias='description')
    language: str | None = Field(None, alias='language')
    created_at: datetime = Field(..., alias='created_at')


class RepoMetrics(BaseModel):
    stars: int = Field(..., alias='stargazers_count')
    forks: int = Field(..., alias='forks_count')
    open_issues: int = Field(..., alias='open_issues_count')


class HNStory(BaseModel):
    object_id: str = Field(..., alias='objectID')
    title: str | None = Field(None, alias='title')
    url: str | None = Field(None, alias='url')
    points: int = Field(..., alias='points')
    num_comments: int = Field(..., alias='num_comments')


class MetricPoint(BaseModel):
    metric_date: date
    stars: int
    forks: int
    open_issues: int


class SearchPlan(BaseModel):
    github_query: str
    hn_query: str
    explanation: str


class ProjectAnalysis(BaseModel):
    repository_name: str
    momentum_score: float
    sentiment: Literal['positive', 'neutral', 'negative']
    growth_status: Literal["exploding", "growing", "stable", "declining", "dead"]
    verdict: str
    growth_signals: list[str]


class FinalReport(BaseModel):
    projects: list[ProjectAnalysis]
    summary: str
    query: str
