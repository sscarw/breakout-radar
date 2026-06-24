from pydantic import BaseModel, Field
from datetime import datetime, date


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
