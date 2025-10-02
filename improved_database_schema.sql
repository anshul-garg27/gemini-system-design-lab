-- Improved Database Schema for Consistency

-- Modified topic_status table with better structure
CREATE TABLE IF NOT EXISTS topic_status_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_title TEXT NOT NULL,           -- Original input title (never changes)
    current_title TEXT,                     -- Current/modified title (can be updated)
    status TEXT NOT NULL DEFAULT 'pending', -- pending, processing, completed, failed
    error_message TEXT,
    processing_started_at TIMESTAMP,
    processing_completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Modified topics table with foreign key
CREATE TABLE IF NOT EXISTS topics_new (
    id INTEGER PRIMARY KEY,
    topic_status_id INTEGER,                -- Foreign key to topic_status
    title TEXT NOT NULL,                    -- Final generated title
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    subcategory TEXT NOT NULL,
    company TEXT NOT NULL,
    technologies TEXT NOT NULL,
    complexity_level TEXT NOT NULL,
    tags TEXT NOT NULL,
    related_topics TEXT NOT NULL,
    metrics TEXT NOT NULL,
    implementation_details TEXT NOT NULL,
    learning_objectives TEXT NOT NULL,
    difficulty INTEGER NOT NULL,
    estimated_read_time TEXT NOT NULL,
    prerequisites TEXT NOT NULL,
    created_date TEXT NOT NULL,
    updated_date TEXT NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source TEXT DEFAULT 'web_batch',
    FOREIGN KEY (topic_status_id) REFERENCES topic_status_new (id),
    UNIQUE(id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_topic_status_original_title ON topic_status_new(original_title);
CREATE INDEX IF NOT EXISTS idx_topic_status_status ON topic_status_new(status);
CREATE INDEX IF NOT EXISTS idx_topics_status_id ON topics_new(topic_status_id);
