#!/usr/bin/env python3
"""
Script to enable WAL mode on existing SQLite database.
Run this once to enable WAL mode, then restart your application.
"""

import sqlite3
import sys
from pathlib import Path

def enable_wal_mode(db_path: str):
    """Enable WAL mode for better concurrency."""
    
    if not Path(db_path).exists():
        print(f"❌ Database not found: {db_path}")
        return False
    
    try:
        print(f"📊 Connecting to database: {db_path}")
        conn = sqlite3.connect(db_path, timeout=30.0)
        
        # Check current journal mode
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode;")
        current_mode = cursor.fetchone()[0]
        print(f"Current journal mode: {current_mode}")
        
        if current_mode.lower() == 'wal':
            print("✅ WAL mode already enabled!")
            return True
        
        # Enable WAL mode
        print("🔄 Enabling WAL mode...")
        cursor.execute("PRAGMA journal_mode=WAL;")
        new_mode = cursor.fetchone()[0]
        
        # Verify
        cursor.execute("PRAGMA journal_mode;")
        verify_mode = cursor.fetchone()[0]
        
        if verify_mode.lower() == 'wal':
            print(f"✅ WAL mode enabled successfully! (was: {current_mode}, now: {verify_mode})")
            
            # Set other optimizations
            print("🔧 Applying additional optimizations...")
            cursor.execute("PRAGMA busy_timeout = 30000;")
            cursor.execute("PRAGMA synchronous = NORMAL;")  # Faster, still safe with WAL
            
            conn.commit()
            conn.close()
            
            print("\n✅ All optimizations applied!")
            print(f"📁 You should now see these files:")
            print(f"   - {db_path}")
            print(f"   - {db_path}-wal")
            print(f"   - {db_path}-shm")
            print("\n🚀 Restart your application to use WAL mode.")
            return True
        else:
            print(f"❌ Failed to enable WAL mode. Current mode: {verify_mode}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    # Find all SQLite databases
    databases = [
        "data/app.db",
        "unified.db",
        "data/unified.db"
    ]
    
    print("=" * 60)
    print("🔧 SQLite WAL Mode Enabler")
    print("=" * 60)
    print()
    
    success_count = 0
    for db_path in databases:
        if Path(db_path).exists():
            print(f"\nProcessing: {db_path}")
            print("-" * 60)
            if enable_wal_mode(db_path):
                success_count += 1
            print()
    
    if success_count == 0:
        print("⚠️  No databases found or processed.")
        print("\nSearched for:")
        for db in databases:
            print(f"  - {db}")
        sys.exit(1)
    else:
        print("=" * 60)
        print(f"✅ Successfully processed {success_count} database(s)")
        print("=" * 60)
        print("\n🚀 Next steps:")
        print("1. Restart your Flask application")
        print("2. Check for -wal and -shm files")
        print("3. Monitor logs for 'database is locked' errors")
        print("4. They should be gone or very rare now!")
        sys.exit(0)
