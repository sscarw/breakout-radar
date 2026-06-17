from PyQt5.QtWidgets.QMainWindow import metric

from models import Repository, RepoMetrics, MetricPoint
import psycopg
import os
from datetime import date
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    conn = psycopg.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('POSTGRES_HOST'),
        port=os.getenv('POSTGRES_PORT'),
    )
    return conn


def save_scan_run(query: str) -> int:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            row = cur.execute("INSERT INTO scan_runs (query) VALUES (%s) RETURNING id",
                              (query,)).fetchone()
            conn.commit()
        return row[0]
    finally:
        conn.close()


def save_repository(repo: Repository) -> int:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            row = cur.execute(
                "INSERT INTO repositories (github_id, name, url, description, language, created_at) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (github_id) DO UPDATE SET name = EXCLUDED.name RETURNING id",
                (repo.github_id, repo.name, repo.url, repo.description, repo.language, repo.created_at,)).fetchone()
            conn.commit()
        return row[0]
    finally:
        conn.close()


def save_metrics(repository_id: int, scan_run_id: int, metrics: RepoMetrics) -> int:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            row = cur.execute(
                "INSERT INTO repository_metrics (repository_id, scan_run_id, metric_date, stars, forks, open_issues) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
                (
                    repository_id, scan_run_id, date.today(), metrics.stars, metrics.forks,
                    metrics.open_issues)).fetchone()
            conn.commit()
        return row[0]
    finally:
        conn.close()


def get_metrics_history(repository_id: int) -> list[MetricPoint]:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            rows = cur.execute(
                "SELECT metric_date, stars, forks, open_issues FROM repository_metrics WHERE repository_id = %s ORDER BY metric_date",
                (repository_id,)
            ).fetchall()
        return [
            MetricPoint(metric_date=r[0], stars=r[1], forks=r[2], open_issues=r[3])
            for r in rows
        ]
    finally:
        conn.close()
