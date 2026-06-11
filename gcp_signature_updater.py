#!/usr/bin/env python3
"""
Gmail signature updater (demo).

This is a small, safe project that mirrors a real automation pattern:
- read user data (CSV)
- build a signature string
- plan vs apply
- retry on transient errors
- write a run report

This demo does NOT call Google APIs. It simulates "update Gmail signature"
by writing the result to a local JSON file.
"""

import argparse
import csv
import json
import random
import time


def read_users(csv_path):
    """Read users from a CSV file."""
    users = []
    with open(csv_path, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            users.append(row)
    return users


def build_signature(user):
    """Create a simple signature based on user fields."""
    name = user.get("full_name", "").strip()
    dept = user.get("department", "").strip()
    phone = user.get("phone", "").strip()

    parts = []
    if name:
        parts.append(name)
    if dept:
        parts.append(dept)
    if phone:
        parts.append(phone)

    return " | ".join(parts)


def load_directory(path):
    """Load the local 'directory' JSON (simulates current signatures)."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_directory(path, directory):
    """Save the local 'directory' JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(directory, f, indent=2, sort_keys=True)


def simulated_update(email, new_sig):
    """
    Simulate a remote update that can occasionally fail.
    This lets us demonstrate retry logic without real Google API calls.
    """
    # 15% chance of transient failure
    if random.random() < 0.15:
        raise RuntimeError("Transient error (simulated)")
    return True


def apply_updates(users, directory, dry_run=False, retries=3, sleep_seconds=0.3):
    """
    Apply updates with idempotency:
    - If signature is already correct, do nothing.
    - Otherwise update it (or show what would change in dry-run).
    """
    report = {
        "dry_run": dry_run,
        "total_users": len(users),
        "changed": 0,
        "unchanged": 0,
        "failed": 0,
        "results": [],
    }

    for u in users:
        email = (u.get("email") or "").strip().lower()
        if not email:
            report["failed"] += 1
            report["results"].append({"email": None, "status": "failed", "reason": "missing email"})
            continue

        desired = build_signature(u)
        current = directory.get(email)

        if current == desired:
            report["unchanged"] += 1
            report["results"].append({"email": email, "status": "unchanged"})
            continue

        if dry_run:
            report["changed"] += 1
            report["results"].append({"email": email, "status": "would_change", "from": current, "to": desired})
            continue

        # apply with retries
        attempt = 0
        ok = False
        last_err = None
        while attempt < retries and not ok:
            attempt += 1
            try:
                simulated_update(email, desired)
                ok = True
            except Exception as e:
                last_err = str(e)
                time.sleep(sleep_seconds)

        if not ok:
            report["failed"] += 1
            report["results"].append({"email": email, "status": "failed", "reason": last_err})
            continue

        directory[email] = desired
        report["changed"] += 1
        report["results"].append({"email": email, "status": "changed", "to": desired})

    return report


def main():
    parser = argparse.ArgumentParser(description="Demo: update Gmail signatures from CSV (simulated).")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_plan = sub.add_parser("plan", help="Show what would change (dry-run)")
    p_plan.add_argument("--input", default="sample_users.csv")
    p_plan.add_argument("--directory", default="directory.json")
    p_plan.add_argument("--report", default="run_report.json")

    p_apply = sub.add_parser("apply", help="Apply changes (writes to directory.json)")
    p_apply.add_argument("--input", default="sample_users.csv")
    p_apply.add_argument("--directory", default="directory.json")
    p_apply.add_argument("--report", default="run_report.json")

    args = parser.parse_args()

    users = read_users(args.input)
    directory = load_directory(args.directory)

    if args.cmd == "plan":
        report = apply_updates(users, directory, dry_run=True)
    else:
        report = apply_updates(users, directory, dry_run=False)
        save_directory(args.directory, directory)

    with open(args.report, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Wrote report to {args.report}")
    if args.cmd == "apply":
        print(f"Updated directory file: {args.directory}")


if __name__ == "__main__":
    main()
