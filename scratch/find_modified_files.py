import os
import sys
import datetime
sys.stdout.reconfigure(encoding='utf-8')

now = datetime.datetime.now()
print(f"Current check time: {now}")

# Check files modified in the last 2 hours
for root, dirs, files in os.walk('.'):
    if '.git' in root or '.gemini' in root or 'scratch' in root: continue
    for f in files:
        p = os.path.join(root, f)
        try:
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(p))
            diff_minutes = (now - mtime).total_seconds() / 60
            if diff_minutes < 120 or '378' in f or 'MB52' in f or 'ANALISIS' in f:
                print(f"{p} -> Modified: {mtime} ({diff_minutes:.1f} mins ago)")
        except Exception:
            pass
