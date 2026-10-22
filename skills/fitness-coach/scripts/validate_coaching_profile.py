#!/usr/bin/env python3
import argparse, json, sys
from pathlib import Path

REQUIRED_PROFILE = ["training_experience", "primary_goal", "equipment", "weekly_time", "injuries", "medical_flags"]

def main():
    ap = argparse.ArgumentParser(description="Validate a coaching profile JSON.")
    ap.add_argument("--input", required=True)
    args = ap.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    errors, warnings = [], []
    if not isinstance(data, dict):
        print(json.dumps({"ok": False, "errors": ["root must be an object"]})); sys.exit(1)
    profile = data.get("profile")
    if not isinstance(profile, dict):
        errors.append("missing profile object")
    else:
        for key in REQUIRED_PROFILE:
            if key not in profile:
                errors.append(f"profile.{key} is required")
        if profile.get("training_experience") not in {"新手", "中级", "高级"}:
            warnings.append("training_experience should be 新手/中级/高级")
        if profile.get("medical_flags") and "red_flags" not in data:
            warnings.append("medical_flags present; consider recording red_flags and referral status")
    for section in ["baselines", "current_plan", "recent_logs"]:
        if section not in data:
            errors.append(f"missing {section}")
    report = {"ok": not errors, "errors": errors, "warnings": warnings}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if not errors else 1)

if __name__ == "__main__":
    main()
