#!/usr/bin/env python3
import argparse, json, sys
from collections import Counter
from pathlib import Path

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--questions', required=True)
    ap.add_argument('--key')
    ap.add_argument('--allow-duplicate-stems', action='store_true')
    args = ap.parse_args()

    questions = load(args.questions)
    key = load(args.key) if args.key else []
    key_map = {x['id']: x.get('answer_index') for x in key}
    errors, warnings = [], []
    ids, stems, subjects = set(), {}, Counter()

    for q in questions:
        qid = q.get('id')
        if not qid:
            errors.append('question missing id')
            continue
        if qid in ids:
            errors.append(f'duplicate id: {qid}')
        ids.add(qid)
        text = str(q.get('question', '')).strip()
        if not text:
            errors.append(f'{qid}: empty question')
        norm = ' '.join(text.lower().split())
        if norm in stems:
            msg = f'duplicate question stem: {qid} duplicates {stems[norm]}'
            (warnings if args.allow_duplicate_stems else errors).append(msg)
        stems[norm] = qid
        choices = q.get('choices')
        if not isinstance(choices, list) or not (2 <= len(choices) <= 10):
            errors.append(f'{qid}: choices must contain 2-10 items')
            continue
        clean = [str(c).strip() for c in choices]
        if any(not c for c in clean):
            errors.append(f'{qid}: empty choice')
        if len(set(clean)) != len(clean):
            errors.append(f'{qid}: duplicate choices')
        subjects[q.get('subject', 'unknown')] += 1
        if key_map:
            if qid not in key_map:
                errors.append(f'{qid}: missing key')
            else:
                idx = key_map[qid]
                if not isinstance(idx, int) or not (0 <= idx < len(clean)):
                    errors.append(f'{qid}: invalid answer_index {idx}')

    if key_map:
        for qid in key_map:
            if qid not in ids:
                errors.append(f'key has unknown id: {qid}')

    report = {
        'questions': len(questions),
        'subjects': dict(subjects),
        'errors': errors,
        'warnings': warnings,
        'ok': not errors,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if not errors else 1)

if __name__ == '__main__':
    main()
