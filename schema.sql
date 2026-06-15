CREATE TABLE repositories (
    id SERIAL PRIMARY KEY,
    github_id BIGINT UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    url TEXT NOT NULL,
    description TEXT NULL,
    language TEXT NULL,
    created_at DATE
);

CREATE TABLE scan_runs (
    id SERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE repository_metrics(
    id SERIAL PRIMARY KEY,
    repository_id INT NOT NULL,
    scan_run_id INT NOT NULL,
    metric_date DATE NOT NULL,
    stars INT NOT NULL DEFAULT 0,
    forks INT NOT NULL DEFAULT 0,
    contributors INT NOT NULL DEFAULT 0,
    open_issues INT NOT NULL  DEFAULT 0,
    CONSTRAINT uq_repository_metric
        UNIQUE (repository_id, metric_date),
    CONSTRAINT fk_repository_metrics
        FOREIGN KEY (repository_id) REFERENCES repositories(id),
    CONSTRAINT fk_scan_metrics
        FOREIGN KEY (scan_run_id) REFERENCES scan_runs(id)
);