#!/usr/bin/env python3
import argparse, json
from collections import defaultdict
from pathlib import Path

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--questions', required=True)
    ap.add_argument('--key', required=True)
    ap.add_argument('--answers', required=True)
    ap.add_argument('--show-mistakes', action='store_true')
    args = ap.parse_args()
    questions = load(args.questions)
    key = {x['id']: x['answer_index'] for x in load(args.key)}
    answers = load(args.answers)
    by_subject = defaultdict(lambda: [0, 0])
    mistakes = []
    correct = 0

    for q in questions:
        ok = answers.get(q['id']) == key.get(q['id'])
        correct += int(ok)
        sub = q.get('subject', 'unknown')
        by_subject[sub][1] += 1
        by_subject[sub][0] += int(ok)
        if args.show_mistakes and not ok:
            mistakes.append({
                'id': q['id'],
                'subject': sub,
                'question': q['question'],
                'selected': answers.get(q['id']),
                'correct': key.get(q['id']),
            })

    total = len(questions)
    report = {
        'total': total,
        'answered': sum(1 for q in questions if q['id'] in answers),
        'correct': correct,
        'accuracy': round(correct / total * 100, 2) if total else 0,
        'by_subject': {
            k: {
                'correct': v[0],
                'total': v[1],
                'accuracy': round(v[0] / v[1] * 100, 2) if v[1] else 0,
            }
            for k, v in sorted(by_subject.items())
        },
    }
    if args.show_mistakes:
        report['mistakes'] = mistakes
    print(json.dumps(report, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
