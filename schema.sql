CREATE TABLE repositories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    url TEXT NOT NULL,
    description TEXT,
    language VARCHAR(50),
    created_at DATE
);

CREATE TABLE repository_metrics (
    id SERIAL PRIMARY KEY,
    repository_id INTEGER,
    metric_date DATE,
    stars INTEGER NOT NULL DEFAULT 0,
    forks INTEGER NOT NULL DEFAULT 0,
    contributors INTEGER NOT NULL DEFAULT 0,
    open_issues INTEGER NOT NULL DEFAULT 0,

    CONSTRAINT fk_repository
        FOREIGN KEY (repository_id)
        REFERENCES repositories(id)
);

CREATE TABLE scan_runs (
    id SERIAL PRIMARY KEY,
    query TEXT,
    scan_date TIMESTAMP
);