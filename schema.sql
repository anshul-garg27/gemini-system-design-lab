CREATE TABLE jobs (
            id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL,
            topic_id TEXT NOT NULL,
            topic_name TEXT NOT NULL
        );
CREATE TABLE tasks (
            id TEXT PRIMARY KEY,
            job_id TEXT NOT NULL,
            platform TEXT NOT NULL,
            format TEXT NOT NULL,
            status TEXT NOT NULL,
            cached INTEGER DEFAULT 0,
            started_at TIMESTAMP,
            finished_at TIMESTAMP,
            error TEXT,
            FOREIGN KEY (job_id) REFERENCES jobs (id)
        );
CREATE TABLE results (
            task_id TEXT PRIMARY KEY,
            raw_response TEXT NOT NULL,
            normalized_json TEXT NOT NULL,
            FOREIGN KEY (task_id) REFERENCES tasks (id)
        );
CREATE TABLE prompts (
            task_id TEXT PRIMARY KEY,
            platform TEXT NOT NULL,
            format TEXT NOT NULL,
            prompt_version TEXT NOT NULL,
            body TEXT NOT NULL,
            FOREIGN KEY (task_id) REFERENCES tasks (id)
        );
