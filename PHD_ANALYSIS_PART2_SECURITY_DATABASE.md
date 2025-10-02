# 🎓 PhD-Level Project Analysis - Part 2: Security & Database

## Table of Contents
1. [Critical Security Issues](#critical-security-issues)
2. [Database Schema Analysis](#database-schema-analysis)
3. [Immediate Action Items](#immediate-action-items)

---

## 1. Critical Security Issues 🚨

### 1.1 🔴🔴🔴 SEVERITY: CRITICAL - API Keys Exposed in Git

**File:** `README.md` lines 30-38

```python
API_KEYS = [
    "AIzaSyCO67rfGWXzxeQSqoupwezNw2RiaMxU5nI",  # EXPOSED!
    "AIzaSyAbP9xIxVVGOQSqp1AxwF0ocCT1c9iRGnU",  # EXPOSED!
    "AIzaSyBTE1iv1_jTMvUNbe-hSSwVA-oqqbiTcHc",  # EXPOSED!
    "AIzaSyBNxuGnXwjcGZOerUMbXuHBJ4lppFk3vos",  # EXPOSED!
    "AIzaSyBFLtr-pr_F1Tl0m013ZkZF14i7ruZ4Emo",  # EXPOSED!
    "AIzaSyCqqid5Vci-ScNNNSKowk55tREJQrvPjN8",  # EXPOSED!
    "AIzaSyCAi57XAKoI376KJEc9iwZZ4w-5e8m46xo"   # EXPOSED!
]
```

**Impact:**
- 🔴 Anyone can use your API keys
- 🔴 Unlimited API calls on your account
- 🔴 Potential $$$$ charges
- 🔴 Keys will hit rate limits
- 🔴 Security breach if these are production keys

**IMMEDIATE ACTION REQUIRED:**

1. **Revoke ALL keys immediately** (Go to Google AI Studio NOW)
2. **Generate new keys**
3. **NEVER commit keys to git again**

**Proper Implementation:**

```python
# config.py (NO KEYS HERE!)
import os
from dotenv import load_dotenv

load_dotenv()

API_KEYS = os.getenv('GEMINI_API_KEYS', '').split(',')

if not API_KEYS or API_KEYS == ['']:
    raise ValueError(
        "No API keys found! Set GEMINI_API_KEYS in .env file"
    )

# Validate key format
for key in API_KEYS:
    if not key.startswith('AIzaSy'):
        raise ValueError(f"Invalid API key format: {key[:10]}...")
```

```bash
# .env (ADD TO .gitignore!)
GEMINI_API_KEYS=key1,key2,key3
```

```.gitignore
# Security - Never commit these!
.env
.env.*
config.py
secrets/
*.key
*.pem
```

### 1.2 🔴 No Authentication/Authorization

**Current State:**
```python
@router.post("/api/topics")
async def create_topics(request: CreateTopicsRequest):
    # Anyone can call this!
    # No API key required
    # No user identification
    # No usage limits
```

**Problems:**
- Anyone on the internet can call your API
- No accountability (who created what?)
- No usage limits per user
- Can't implement billing/quotas

**Solution:**

```python
# Add API key authentication
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    """Verify API key from request header."""
    valid_keys = get_valid_api_keys_from_db()
    
    if api_key not in valid_keys:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )
    
    # Track usage
    increment_api_key_usage(api_key)
    
    return api_key

@router.post("/api/topics", dependencies=[Depends(verify_api_key)])
async def create_topics(request: CreateTopicsRequest):
    # Now protected!
    pass
```

**Database schema for API keys:**
```sql
CREATE TABLE api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key_hash TEXT UNIQUE NOT NULL,  -- Store hash, not plaintext!
    user_email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP,
    usage_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    rate_limit_per_minute INTEGER DEFAULT 100
);
```

### 1.3 🔴 SQL Injection Risks

**Found in:** `check_duplicates.py`, some database queries

```python
# DANGEROUS (even though title_column is controlled):
cursor.execute(f"""
    SELECT {title_column} FROM topic_status
""")
```

**Why Dangerous:**
- If `title_column` ever comes from user input → SQL injection
- Bad practice even if currently safe
- Code reviews will flag this

**Correct Approach:**
```python
# Option 1: Whitelist allowed columns
ALLOWED_COLUMNS = {'title', 'original_title', 'current_title'}
if title_column not in ALLOWED_COLUMNS:
    raise ValueError(f"Invalid column: {title_column}")

cursor.execute(f"SELECT {title_column} FROM topic_status")

# Option 2: Use query builder
from sqlalchemy import select, table, column

query = select(column(title_column)).select_from(table('topic_status'))
```

### 1.4 🟠 No Input Validation

**Current:**
```python
@router.post("/api/topics")
async def create_topics(request: CreateTopicsRequest):
    titles = request.titles  # Could be ANYTHING!
    # titles = ["A" * 1000000]  # 1MB title? Sure!
    # titles = [""  * 10000]  # 10000 empty strings? Why not!
```

**Problems:**
- User can send 1MB titles
- User can send 10000 topics at once
- No validation on content

**Solution:**
```python
from pydantic import BaseModel, Field, validator

class CreateTopicsRequest(BaseModel):
    titles: List[str] = Field(
        ..., 
        min_items=1, 
        max_items=100,  # Limit bulk operations
        description="List of topic titles to create"
    )
    batch_size: int = Field(
        default=5,
        ge=1,
        le=5,
        description="Topics per API call"
    )
    
    @validator('titles')
    def validate_titles(cls, v):
        """Validate each title."""
        for title in v:
            # Remove leading/trailing whitespace
            title = title.strip()
            
            # Check length
            if len(title) < 10:
                raise ValueError(f"Title too short: {title[:20]}")
            if len(title) > 500:
                raise ValueError(f"Title too long: {title[:20]}...")
            
            # Check for suspicious patterns
            if title.count('SELECT') > 0 or title.count('DROP') > 0:
                raise ValueError("Suspicious content detected")
        
        return v
```

### 1.5 🟠 No Rate Limiting

**Problem:** User can spam 10,000 requests per second!

```python
# Missing rate limiting = DoS vulnerability
@router.post("/api/topics")
async def create_topics():
    # Attacker sends 10000 requests instantly
    # Server crashes or becomes unresponsive
    pass
```

**Solution:**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Apply to endpoints
@limiter.limit("100/minute")  # 100 requests per minute per IP
@router.post("/api/topics")
async def create_topics(request: Request):
    pass

# Different limits for different endpoints
@limiter.limit("1000/minute")  # High limit for reads
@router.get("/api/topics")
async def get_topics():
    pass

@limiter.limit("10/minute")  # Low limit for expensive operations
@router.post("/api/topics/batch")
async def batch_create_topics():
    pass
```

### 1.6 🟡 No CORS Configuration

**Current:** Uses default CORS (dangerous!)

```python
# Anyone from any domain can call your API
# https://malicious-site.com → calls your API
```

**Solution:**
```python
from fastapi.middleware.cors import CORSMiddleware

# Strict CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://app.yourdomain.com",
        "http://localhost:5173",  # Dev only
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    max_age=3600,  # Cache preflight for 1 hour
)
```

### 1.7 🟡 Exposed Database File

```python
# Predictable path!
db_path = "unified.db"
```

**Problem:** Attacker knows where your database is!

**Solution:**
```python
import secrets
from pathlib import Path

# Randomized path
DB_DIR = Path("./data/secure")
DB_DIR.mkdir(parents=True, exist_ok=True)

db_path = DB_DIR / f"{secrets.token_hex(16)}.db"

# Or use environment variable
db_path = os.getenv('DATABASE_PATH', 'unified.db')
```

---

## 2. Database Schema Analysis

### 2.1 Current Schema Issues

#### 2.1.1 🔴 Denormalized JSON Storage

**Current:**
```sql
CREATE TABLE topics (
    technologies TEXT NOT NULL,  -- Stores: '["Python", "Redis", "AWS"]'
    tags TEXT NOT NULL,          -- Stores: '["api", "backend"]'
    prerequisites TEXT NOT NULL  -- Stores: '["HTTP", "REST"]'
);
```

**Critical Problems:**

1. **Cannot Query Efficiently:**
```sql
-- IMPOSSIBLE QUERY:
SELECT * FROM topics WHERE 'Python' IN technologies;
-- Error: Can't search in JSON string!

-- SLOW WORKAROUND:
SELECT * FROM topics WHERE technologies LIKE '%Python%';
-- Problem: Matches "Python" and "IPython" and "Pythonic"
```

2. **Cannot Do Analytics:**
```sql
-- WANT: Top 10 most used technologies
-- IMPOSSIBLE with current schema!
```

3. **No Foreign Key Constraints:**
```python
# Can store invalid data
technologies = ["NonexistentTech"]  # No validation!
```

4. **Difficult Migrations:**
```sql
-- Want to rename "React" to "React.js" across all topics?
-- Have to parse JSON in every row! Extremely slow!
```

**Proper Solution - Normalized Schema:**

```sql
-- Main tables
CREATE TABLE topics (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    difficulty INTEGER CHECK(difficulty BETWEEN 1 AND 10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE technologies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    category TEXT,  -- frontend/backend/database/etc
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Junction tables (many-to-many)
CREATE TABLE topic_technologies (
    topic_id INTEGER NOT NULL,
    technology_id INTEGER NOT NULL,
    PRIMARY KEY (topic_id, technology_id),
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE,
    FOREIGN KEY (technology_id) REFERENCES technologies(id) ON DELETE CASCADE
);

CREATE TABLE topic_tags (
    topic_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (topic_id, tag_id),
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- Now you can query efficiently!
-- Top 10 technologies:
SELECT t.name, COUNT(*) as usage_count
FROM technologies t
JOIN topic_technologies tt ON t.id = tt.technology_id
GROUP BY t.id
ORDER BY usage_count DESC
LIMIT 10;

-- Topics using Python:
SELECT topics.*
FROM topics
JOIN topic_technologies tt ON topics.id = tt.topic_id
JOIN technologies t ON tt.technology_id = t.id
WHERE t.name = 'Python';
```

#### 2.1.2 🔴 Missing Critical Indexes

**Current:** Only 4 basic indexes exist

```sql
-- Existing (good but incomplete):
CREATE INDEX idx_topics_category ON topics(category);
CREATE INDEX idx_topics_company ON topics(company);
CREATE INDEX idx_topics_complexity ON topics(complexity_level);
CREATE INDEX idx_topics_difficulty ON topics(difficulty);
```

**Missing Indexes = Slow Queries:**

```sql
-- Slow queries without indexes:
SELECT * FROM topic_status WHERE status = 'pending';  -- SLOW!
SELECT * FROM topics WHERE created_date > '2024-01-01';  -- SLOW!
SELECT * FROM topics ORDER BY difficulty, complexity_level;  -- SLOW!
```

**Add These Indexes:**

```sql
-- Single-column indexes
CREATE INDEX idx_topic_status_status ON topic_status(status);
CREATE INDEX idx_topic_status_created_at ON topic_status(created_at);
CREATE INDEX idx_topic_status_updated_at ON topic_status(updated_at);
CREATE INDEX idx_topics_created_date ON topics(created_date);
CREATE INDEX idx_topics_updated_date ON topics(updated_date);
CREATE INDEX idx_topics_source ON topics(source);

-- Composite indexes for common query patterns
CREATE INDEX idx_topic_status_status_created 
ON topic_status(status, created_at);

CREATE INDEX idx_topics_category_difficulty 
ON topics(category, difficulty);

CREATE INDEX idx_topics_company_category 
ON topics(company, category);

-- Partial indexes for specific queries
CREATE INDEX idx_topic_status_pending 
ON topic_status(created_at) 
WHERE status = 'pending';

CREATE INDEX idx_topic_status_failed 
ON topic_status(created_at) 
WHERE status = 'failed';
```

**Impact:** Queries will be 10-100x faster!

#### 2.1.3 🟠 No Audit Trail

**Problem:** No way to know:
- Who modified what?
- When was it modified?
- What changed?

**Solution:**
```sql
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,
    record_id INTEGER NOT NULL,
    action TEXT NOT NULL,  -- INSERT/UPDATE/DELETE
    old_values TEXT,  -- JSON snapshot before change
    new_values TEXT,  -- JSON snapshot after change
    changed_by TEXT,  -- User identifier
    ip_address TEXT,
    user_agent TEXT,
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_audit_table_record (table_name, record_id),
    INDEX idx_audit_changed_at (changed_at)
);

-- Trigger to auto-populate
CREATE TRIGGER topics_audit_update
AFTER UPDATE ON topics
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, record_id, action, old_values, new_values)
    VALUES (
        'topics',
        NEW.id,
        'UPDATE',
        json_object('title', OLD.title, 'difficulty', OLD.difficulty),
        json_object('title', NEW.title, 'difficulty', NEW.difficulty)
    );
END;
```

#### 2.1.4 🟡 No Soft Deletes

**Problem:** DELETE is permanent!

```python
cursor.execute("DELETE FROM topics WHERE id = 123")
# Gone forever! No undo!
```

**Solution:**
```sql
ALTER TABLE topics ADD COLUMN deleted_at TIMESTAMP;
ALTER TABLE topics ADD COLUMN is_deleted BOOLEAN DEFAULT 0;

-- Soft delete
UPDATE topics 
SET is_deleted = 1, deleted_at = CURRENT_TIMESTAMP 
WHERE id = 123;

-- All queries filter deleted
SELECT * FROM topics WHERE is_deleted = 0;

-- Can restore
UPDATE topics 
SET is_deleted = 0, deleted_at = NULL 
WHERE id = 123;
```

### 2.2 Database Score: 5/10

**Strengths:**
- ✅ Dual-title system (excellent!)
- ✅ Proper timestamps
- ✅ Backward compatibility
- ✅ Some indexes

**Weaknesses:**
- ❌ Heavy denormalization
- ❌ Missing critical indexes
- ❌ No foreign keys
- ❌ No audit trail
- ❌ No soft deletes
- ❌ No query optimization

---

## 3. Immediate Action Items

### Priority 1: CRITICAL (Do NOW)

```markdown
□ Revoke ALL exposed API keys
□ Remove keys from git history (use git filter-branch)
□ Add .env to .gitignore
□ Generate new API keys
□ Move keys to environment variables
□ Add basic authentication to API endpoints
```

### Priority 2: URGENT (This Week)

```markdown
□ Implement rate limiting
□ Add input validation
□ Configure CORS properly
□ Add database indexes (performance)
□ Set up error monitoring (Sentry)
```

### Priority 3: HIGH (This Month)

```markdown
□ Start database normalization
□ Implement audit logging
□ Add soft deletes
□ Create backup system
□ Write security documentation
```

---

## 4. Security Score: 2/10 🚨

**Critical:**
- API keys exposed
- No authentication
- No authorization
- No rate limiting

**HIGH:**
- SQL injection risks
- No input validation
- Weak CORS policy

**This MUST be fixed before production use!**

---

**Next:** See Part 3 for Code Quality & Testing Analysis
