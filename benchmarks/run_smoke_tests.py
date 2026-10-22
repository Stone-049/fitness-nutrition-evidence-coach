#!/usr/bin/env python3
import json, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "fitness-coach"
FIX = ROOT / "benchmarks" / "fixtures"

def run(args):
    p = subprocess.run(args, text=True, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(map(str,args))}\n{p.stdout}\n{p.stderr}")
    return p.stdout

def main():
    py = sys.executable
    checks = []
    out = run([py, str(SKILL/"scripts/validate_coaching_profile.py"), "--input", str(FIX/"profile.json")])
    checks.append(("profile validator", json.loads(out).get("ok") is True))
    with tempfile.TemporaryDirectory() as td:
        normalized = Path(td)/"sessions.json"
        run([py, str(SKILL/"scripts/import_training_csv.py"), "--input", str(FIX/"training.csv"), "--output", str(normalized)])
        sessions = json.loads(normalized.read_text(encoding="utf-8"))
        checks.append(("CSV importer", len(sessions) == 2 and sessions[0]["volume_load"] > 0))
        review = json.loads(run([py, str(SKILL/"scripts/weekly_review.py"), "--sessions", str(normalized)]))
        checks.append(("weekly review", review.get("sessions") == 2))
    q = SKILL/"tests"/"sample_questions.json"
    k = SKILL/"tests"/"sample_key.json"
    a = SKILL/"tests"/"sample_answers.json"
    if q.exists() and k.exists() and a.exists():
        out = run([py, str(SKILL/"scripts/validate_question_bank.py"), "--questions", str(q), "--key", str(k)])
        checks.append(("question bank", json.loads(out).get("ok") is True))
        score = json.loads(run([py, str(SKILL/"scripts/score_blind.py"), "--questions", str(q), "--key", str(k), "--answers", str(a)]))
        checks.append(("blind scorer", score.get("answered") == score.get("total")))
    failed = [name for name, ok in checks if not ok]
    print(json.dumps({"checks": checks, "passed": len(checks)-len(failed), "failed": failed}, ensure_ascii=False, indent=2))
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
