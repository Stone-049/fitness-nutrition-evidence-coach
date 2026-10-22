#!/usr/bin/env python3
import re, sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "fitness-coach"
SKILL = SKILL_DIR / "SKILL.md"

def main():
    text = SKILL.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    errors = []
    if not m:
        print("missing YAML frontmatter"); sys.exit(1)
    fm = yaml.safe_load(m.group(1)) or {}
    if fm.get("name") != "fitness-nutrition-evidence-coach":
        errors.append("unexpected skill name")
    if len(str(fm.get("description", ""))) < 20:
        errors.append("description is too short")
    for rel in re.findall(r"references/[A-Za-z0-9._/-]+", text):
        if not (SKILL_DIR / rel).exists(): errors.append(f"missing reference: {rel}")
    print({"ok": not errors, "errors": errors, "skill_chars": len(text)})
    sys.exit(0 if not errors else 1)

if __name__ == "__main__":
    main()
