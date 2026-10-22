#!/usr/bin/env python3
import argparse, csv, json, math
from collections import defaultdict
from pathlib import Path

def num(value, field, row_no):
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"row {row_no}: {field} must be numeric")

def main():
    ap = argparse.ArgumentParser(description="Normalize a generic training CSV into session JSON.")
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    sessions = defaultdict(lambda: {"date": None, "type": "strength", "duration_min": 0, "rpe": 0, "exercises": [], "volume_load": 0, "session_load": 0})
    with Path(args.input).open("r", encoding="utf-8-sig", newline="") as fh:
        for i, row in enumerate(csv.DictReader(fh), 2):
            date = (row.get("date") or "").strip()
            if not date:
                raise ValueError(f"row {i}: date is required")
            s = sessions[date]
            s["date"] = date
            s["type"] = (row.get("type") or s["type"]).strip() or "strength"
            s["duration_min"] = max(s["duration_min"], num(row.get("duration_min") or 0, "duration_min", i))
            s["rpe"] = max(s["rpe"], num(row.get("rpe") or 0, "rpe", i))
            exercise = (row.get("exercise") or "").strip()
            if exercise:
                weight = num(row.get("weight") or 0, "weight", i)
                reps = num(row.get("reps") or 0, "reps", i)
                s["exercises"].append({"exercise": exercise, "weight": weight, "reps": reps})
                s["volume_load"] += weight * reps
    out = []
    for s in sessions.values():
        s["session_load"] = s["duration_min"] * s["rpe"]
        s["volume_load"] = round(s["volume_load"], 2)
        s["session_load"] = round(s["session_load"], 2)
        out.append(s)
    out.sort(key=lambda x: x["date"])
    Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"sessions": len(out), "output": args.output}, ensure_ascii=False))

if __name__ == "__main__":
    main()
