import json
import sqlite3
import hashlib
import os
import subprocess

def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True, text=True).strip()

db_path = 'lisanapp.db'
if not os.path.exists(db_path):
    print("No DB")
    exit(1)

# DB Hash before
db_hash_before = hashlib.sha256(open(db_path, 'rb').read()).hexdigest()

conn = sqlite3.connect(db_path)
c = conn.cursor()

# Phase 4 - ResearchRun audit
c.execute("SELECT id, target_expression FROM research_runs WHERE id LIKE 'run_%'")
runs = c.fetchall()

# Phase 8 - Claims
c.execute("SELECT id, research_run_id, revision_id FROM semantic_claims WHERE id LIKE 'claim_%'")
claims = c.fetchall()

# Phase 12 - VerificationRecords
c.execute("SELECT id, claim_id FROM verification_records")
verifications = c.fetchall()

# Observations
# Assuming table is observation_artifacts or similar, let's just check if it exists
try:
    c.execute("SELECT COUNT(*) FROM observation_artifacts")
    obs_count = c.fetchone()[0]
except:
    obs_count = 0

print(f"Runs: {len(runs)}")
print(f"Claims: {len(claims)}")
print(f"Verifications: {len(verifications)}")
print(f"Observations: {obs_count}")

db_hash_after = hashlib.sha256(open(db_path, 'rb').read()).hexdigest()
print(f"DB Hash Match: {db_hash_before == db_hash_after}")
