#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def main():
    ap = argparse.ArgumentParser(description="Create a compact weekly coaching review from normalized sessions.")
    ap.add_argument("--sessions", required=True)
    ap.add_argument("--output")
    args = ap.parse_args()
    sessions = json.loads(Path(args.sessions).read_text(encoding="utf-8"))
    if not isinstance(sessions, list) or not sessions:
        result = {"sessions": 0, "summary": "No sessions recorded.", "action": "Record at least one session before adjusting the plan."}
    else:
        total_load = sum(float(s.get("session_load", 0)) for s in sessions)
        total_volume = sum(float(s.get("volume_load", 0)) for s in sessions)
        dates = sorted({s.get("date") for s in sessions if s.get("date")})
        types = sorted({s.get("type", "unknown") for s in sessions})
        result = {
            "sessions": len(sessions),
            "training_days": len(dates),
            "date_range": [dates[0], dates[-1]] if dates else [],
            "types": types,
            "total_session_load": round(total_load, 2),
            "total_volume_load": round(total_volume, 2),
            "summary": "Review progress, recovery, pain, nutrition adherence, and choose one variable to change next week.",
            "decision_prompt": {
                "trigger": "What changed this week?",
                "observation": "Which data support that change?",
                "decision": "What single variable will change?",
                "expected": "What result do you expect?",
                "review_date": "When will you reassess?"
            }
        }
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        print(text)

if __name__ == "__main__":
    main()
