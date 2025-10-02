#!/usr/bin/env python3
"""
Quick script to replace unified_database.py with the refactored version.
"""
import shutil
from datetime import datetime
from pathlib import Path

# Create backup
backup_name = f"unified_database_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
shutil.copy2("unified_database.py", backup_name)
print(f"✅ Backup created: {backup_name}")

# Replace with refactored version
shutil.copy2("unified_database_refactored.py", "unified_database.py")
print(f"✅ Replaced unified_database.py with refactored version")

print(f"\n🎉 Done! Your imports should now work.")
print(f"\nTo rollback: cp {backup_name} unified_database.py")
