#!/usr/bin/env python3
"""Seed / manage API keys in the unified.db api_keys table.

Usage examples:
  Seed from config.py API_KEYS list:
    python scripts/seed_api_keys.py --from-config

  Add specific keys:
    python scripts/seed_api_keys.py --add KEY1 KEY2 KEY3

  List all keys with stats:
    python scripts/seed_api_keys.py --list

  Disable a key:
    python scripts/seed_api_keys.py --disable KEY_VALUE

  Manually set status:
    python scripts/seed_api_keys.py --set-status KEY_VALUE RATE_LIMITED
"""
import argparse
from api_key_manager import APIKeyManager

STATUSES = [
    "ACTIVE","RATE_LIMITED","TEMP_DISABLED","DISABLED","INVALID","EXPIRED"
]

def seed_from_config(m: APIKeyManager):
    try:
        from config import API_KEYS
    except ImportError:
        print("config.API_KEYS not found")
        return
    added = 0
    for k in API_KEYS:
        k = k.strip()
        if not k:
            continue
        m.add_key(k)
        added += 1
    print(f"Seeded {added} keys from config.py")

def list_keys(m: APIKeyManager, limit: int | None):
    rows = m.get_all()
    print("id | status | succ | fail | consec | last_used | rate_reset | key_prefix")
    for r in rows[:limit if limit else None]:
        kid, key, status, succ, fail, consec, last_used, rate_reset = r
        print(f"{kid:3} | {status:12} | {succ:4} | {fail:4} | {consec:2} | {last_used or '-':19} | {rate_reset or '-':19} | {key[:12]}...")
    print("Totals:", m.get_status_counts())

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--from-config', action='store_true', help='Seed keys from config.API_KEYS')
    p.add_argument('--add', nargs='*', help='Add one or more keys')
    p.add_argument('--list', action='store_true', help='List keys')
    p.add_argument('--limit', type=int, help='Limit listing rows')
    p.add_argument('--disable', help='Disable (set status=DISABLED) a key value')
    p.add_argument('--set-status', nargs=2, metavar=('KEY','STATUS'), help='Manually set status of a key')
    args = p.parse_args()

    m = APIKeyManager()

    if args.from_config:
        seed_from_config(m)

    if args.add:
        for k in args.add:
            m.add_key(k)
        print(f"Added {len(args.add)} keys")

    if args.disable:
        m.manually_set_status(args.disable, 'DISABLED')
        print(f"Disabled key prefix {args.disable[:10]}...")

    if args.set_status:
        key, status = args.set_status
        if status not in STATUSES:
            print(f"Invalid status. Choose from {STATUSES}")
        else:
            m.manually_set_status(key, status)
            print(f"Set status {status} for key prefix {key[:10]}...")

    if args.list:
        list_keys(m, args.limit)

    if not any([args.from_config, args.add, args.list, args.disable, args.set_status]):
        p.print_help()

if __name__ == '__main__':
    main()
