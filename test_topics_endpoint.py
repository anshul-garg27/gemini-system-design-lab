#!/usr/bin/env python3
"""Quick test to see what's causing the 500 error."""

import sys
import traceback
from unified_database import unified_db

print("Testing database methods...\n")

try:
    # Test 1: Get topics paginated
    print("Test 1: get_topics_paginated(limit=20, offset=0)")
    topics = unified_db.get_topics_paginated(
        limit=20,
        offset=0,
        sort_by="created_date",
        sort_order="desc"
    )
    print(f"✅ Success! Retrieved {len(topics)} topics")
    if topics:
        print(f"   First topic keys: {list(topics[0].keys())}")
    print()
    
except Exception as e:
    print(f"❌ Error: {e}")
    traceback.print_exc()
    print()

try:
    # Test 2: Get topics count
    print("Test 2: get_topics_count()")
    count = unified_db.get_topics_count()
    print(f"✅ Success! Total count: {count}")
    print()
    
except Exception as e:
    print(f"❌ Error: {e}")
    traceback.print_exc()
    print()

try:
    # Test 3: Get topics with limit=0 (should fail validation)
    print("Test 3: get_topics_paginated(limit=0)")
    topics = unified_db.get_topics_paginated(
        limit=0,
        offset=5
    )
    print(f"✅ Success! Retrieved {len(topics)} topics")
    print()
    
except Exception as e:
    print(f"❌ Error: {e}")
    traceback.print_exc()
    print()

print("\n" + "="*50)
print("Testing complete!")
