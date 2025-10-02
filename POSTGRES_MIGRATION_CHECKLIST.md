# PostgreSQL Migration Checklist

## Quick Summary

**Current**: SQLite with JSON arrays as TEXT  
**Target**: PostgreSQL with native arrays and JSONB  
**Timeline**: 1 week  
**Performance Gain**: 50-100x on filtered queries  
**Effort**: Medium (mostly straightforward)

---

## Why PostgreSQL?

| Feature | SQLite (Current) | PostgreSQL (Target) |
|---------|------------------|---------------------|
| Array filtering | `LIKE '%"api"%'` (500ms) | `'api' = ANY(tags)` (5ms) |
| Full-text search | Limited | Advanced with ranking |
| Array indexes | ❌ No | ✅ GIN indexes |
| Concurrent writes | ❌ Locks entire DB | ✅ Row-level locking |
| Scalability | 20k topics max | Millions of topics |

---

## Migration Checklist

### **Phase 1: Setup (Day 1)** ⏱️ 2-3 hours

- [ ] Install Docker Desktop (if not already)
- [ ] Create `docker-compose.yml` for PostgreSQL
- [ ] Start PostgreSQL container
- [ ] Verify connection: `psql -h localhost -U admin -d sysdesign_topics`
- [ ] Install Python dependencies: `pip install psycopg2-binary asyncpg`

### **Phase 2: Schema (Day 1)** ⏱️ 2-3 hours

- [ ] Create `schema_postgres.sql` with new schema
- [ ] Define native array columns: `TEXT[]`
- [ ] Define JSONB columns for nested data
- [ ] Add GIN indexes for arrays
- [ ] Add full-text search index
- [ ] Run schema creation
- [ ] Verify tables created: `\dt` in psql

### **Phase 3: Data Migration (Day 2)** ⏱️ 3-4 hours

- [ ] Create migration script `migrate_to_postgres.py`
- [ ] Test migration with 100 topics first
- [ ] Run full migration (~20k topics)
- [ ] Verify data integrity
- [ ] Compare counts: SQLite vs PostgreSQL
- [ ] Spot-check 10-20 random topics
- [ ] Keep SQLite as backup (don't delete yet!)

### **Phase 4: Code Updates (Days 3-4)** ⏱️ 8-12 hours

#### **Backend Updates:**

- [ ] Create `unified_database_postgres.py`
- [ ] Update `get_topics_paginated()`:
  - [ ] Change tag filter: `LIKE '%"tag"%'` → `%s = ANY(tags)`
  - [ ] Change technology filter: `LIKE` → `= ANY(technologies)`
  - [ ] Add full-text search with ranking
- [ ] Update `get_topics_count()` with same filters
- [ ] Update `get_filter_options()`:
  - [ ] Use `unnest(tags)` for tag extraction
  - [ ] Use `unnest(technologies)` for tech extraction
- [ ] Add array operators for complex filters
- [ ] Update connection string in config
- [ ] Test all CRUD operations

#### **Query Changes:**

```python
# OLD (SQLite)
WHERE tags LIKE '%"api"%'

# NEW (PostgreSQL)
WHERE 'api' = ANY(tags)

# OLD (SQLite)
WHERE technologies LIKE '%"Redis"%'

# NEW (PostgreSQL)
WHERE 'Redis' = ANY(technologies)

# NEW - Multiple tags (AND)
WHERE tags @> ARRAY['api', 'caching']

# NEW - Technologies (OR)
WHERE technologies && ARRAY['Redis', 'Kafka']

# NEW - Full-text search with ranking
WHERE search_vector @@ to_tsquery('cache & performance')
ORDER BY ts_rank(search_vector, to_tsquery('cache & performance')) DESC
```

### **Phase 5: Testing (Day 5)** ⏱️ 4-6 hours

- [ ] Test basic queries (select, insert, update, delete)
- [ ] Test all filter combinations
- [ ] Test pagination
- [ ] Test search functionality
- [ ] Load test: 100 concurrent users
- [ ] Performance benchmark vs SQLite
- [ ] Test full-text search
- [ ] Test array operations
- [ ] Frontend smoke test

### **Phase 6: Deployment (Day 6)** ⏱️ 2-4 hours

- [ ] Update production config
- [ ] Deploy PostgreSQL (Docker or managed service)
- [ ] Run migration on production data
- [ ] Update application code
- [ ] Deploy backend
- [ ] Monitor for errors
- [ ] Check performance metrics
- [ ] Keep SQLite backup for 1 week

### **Phase 7: Optimization (Day 7)** ⏱️ 2-3 hours

- [ ] Analyze slow queries: `EXPLAIN ANALYZE`
- [ ] Add missing indexes if needed
- [ ] Tune PostgreSQL config
- [ ] Set up monitoring
- [ ] Document new query patterns
- [ ] Update team documentation

---

## Docker Setup

### **docker-compose.yml**

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: sysdesign_postgres
    environment:
      POSTGRES_DB: sysdesign_topics
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-changeme}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./postgres/init.sql:/docker-entrypoint-initdb.d/init.sql
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin -d sysdesign_topics"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### **Start PostgreSQL**

```bash
# Start
docker-compose up -d postgres

# Check logs
docker-compose logs -f postgres

# Connect to database
docker exec -it sysdesign_postgres psql -U admin -d sysdesign_topics

# Stop
docker-compose down

# Stop and remove data (CAUTION!)
docker-compose down -v
```

---

## Connection Strings

### **Before (SQLite)**

```python
DATABASE_PATH = "data/app.db"
conn = sqlite3.connect(DATABASE_PATH)
```

### **After (PostgreSQL)**

```python
# Development
DATABASE_URL = "postgresql://admin:changeme@localhost:5432/sysdesign_topics"

# Production (example)
DATABASE_URL = "postgresql://admin:password@postgres.example.com:5432/sysdesign_topics"

# Using psycopg2
import psycopg2
conn = psycopg2.connect(DATABASE_URL)

# Using SQLAlchemy (recommended)
from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL)
```

---

## Key Code Changes

### **1. Update `requirements.txt`**

```txt
# Add these
psycopg2-binary==2.9.9
asyncpg==0.29.0  # If using async
sqlalchemy==2.0.23  # Optional, for ORM
```

### **2. Update Filter Queries**

```python
# Before (SQLite)
def get_topics_paginated(self, cursor, tag=None, technology=None, ...):
    if tag:
        where_conditions.append("topics.tags LIKE ?")
        params.append(f'%"{tag}"%')
    
    if technology:
        where_conditions.append("topics.technologies LIKE ?")
        params.append(f'%"{technology}"%')

# After (PostgreSQL)
def get_topics_paginated(self, cursor, tag=None, technology=None, ...):
    if tag:
        where_conditions.append("%s = ANY(topics.tags)")
        params.append(tag)
    
    if technology:
        where_conditions.append("%s = ANY(topics.technologies)")
        params.append(technology)
```

### **3. Update Filter Options**

```python
# Before (SQLite)
def get_filter_options(self, cursor):
    cursor.execute("SELECT DISTINCT technologies FROM topics")
    technologies_set = set()
    for row in cursor.fetchall():
        techs = json.loads(row[0])
        technologies_set.update(techs)
    technologies = sorted(list(technologies_set))

# After (PostgreSQL) - Much simpler!
def get_filter_options(self, cursor):
    cursor.execute("""
        SELECT DISTINCT unnest(technologies) as tech 
        FROM topics 
        ORDER BY tech
    """)
    technologies = [row[0] for row in cursor.fetchall()]
```

### **4. Add Full-Text Search**

```python
# New capability with PostgreSQL
def search_topics(self, cursor, query, limit=20):
    cursor.execute("""
        SELECT *, 
               ts_rank(search_vector, to_tsquery(%s)) as rank
        FROM topics
        WHERE search_vector @@ to_tsquery(%s)
        ORDER BY rank DESC
        LIMIT %s
    """, (query, query, limit))
    return cursor.fetchall()
```

---

## Performance Expectations

| Query Type | SQLite Time | PostgreSQL Time | Improvement |
|------------|-------------|-----------------|-------------|
| Single tag filter | 500ms | 5ms | **100x faster** |
| Multiple filters | 1.5s | 15ms | **100x faster** |
| Full-text search | 1s | 20ms | **50x faster** |
| Aggregate queries | 2s | 50ms | **40x faster** |
| Insert/Update | 10ms | 5ms | **2x faster** |

---

## Rollback Plan

If something goes wrong:

1. **Keep SQLite database** - Don't delete for 1 week
2. **Quick rollback**: 
   ```python
   # In config.py
   USE_POSTGRES = False  # Switch back to SQLite
   ```
3. **Data issues**: Re-run migration from SQLite backup
4. **Performance issues**: Check indexes, run `ANALYZE`

---

## Monitoring Checklist

After migration:

- [ ] Query response times (should be <100ms for most queries)
- [ ] Error rates (should be near 0%)
- [ ] Connection pool usage
- [ ] Database CPU/memory usage
- [ ] Slow query log (queries >1s)
- [ ] Index hit rate (should be >95%)

---

## Common Issues & Solutions

### **Issue 1: Connection errors**

```bash
# Solution: Check PostgreSQL is running
docker-compose ps

# Solution: Check connection string
psql postgresql://admin:changeme@localhost:5432/sysdesign_topics
```

### **Issue 2: Slow queries**

```sql
-- Solution: Analyze query
EXPLAIN ANALYZE SELECT * FROM topics WHERE 'api' = ANY(tags);

-- Solution: Rebuild indexes
REINDEX INDEX idx_tags_gin;

-- Solution: Update statistics
ANALYZE topics;
```

### **Issue 3: Array syntax errors**

```python
# Wrong
WHERE tags = 'api'  # ❌ Can't compare array to string

# Right
WHERE 'api' = ANY(tags)  # ✅
WHERE tags @> ARRAY['api']  # ✅
```

---

## Success Metrics

After migration, you should see:

✅ **50-100x faster** filtered queries  
✅ **10x more** concurrent users supported  
✅ **Better search** results with ranking  
✅ **Cleaner code** - no JSON parsing  
✅ **Future-proof** - can scale to millions of topics  

---

## Quick Commands Reference

```bash
# Start PostgreSQL
docker-compose up -d

# Connect to database
docker exec -it sysdesign_postgres psql -U admin -d sysdesign_topics

# List tables
\dt

# Describe table
\d topics

# Check indexes
\di

# Run migration
python migrate_to_postgres.py

# Backup database
docker exec sysdesign_postgres pg_dump -U admin sysdesign_topics > backup.sql

# Restore database
docker exec -i sysdesign_postgres psql -U admin sysdesign_topics < backup.sql
```

---

## Resources

- [PostgreSQL Array Documentation](https://www.postgresql.org/docs/current/arrays.html)
- [PostgreSQL Full-Text Search](https://www.postgresql.org/docs/current/textsearch.html)
- [GIN Index Performance](https://www.postgresql.org/docs/current/gin.html)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [PostgreSQL Performance Tuning](https://wiki.postgresql.org/wiki/Performance_Optimization)

---

## Next Steps

1. ✅ Read `DATABASE_MIGRATION_RESEARCH.md` for full analysis
2. ⬜ Set up PostgreSQL with Docker (2 hours)
3. ⬜ Run test migration with sample data (1 hour)
4. ⬜ Update application code (1-2 days)
5. ⬜ Performance testing (4 hours)
6. ⬜ Production deployment (4 hours)

**Total Timeline**: 1 week  
**Complexity**: Medium  
**Risk**: Low (keep SQLite as backup)  
**Reward**: High (100x performance improvement)
