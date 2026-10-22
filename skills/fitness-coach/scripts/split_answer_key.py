#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--questions-out', required=True)
    ap.add_argument('--key-out', required=True)
    args = ap.parse_args()
    data = json.loads(Path(args.input).read_text(encoding='utf-8'))
    questions, key = [], []
    for row in data:
        qid = row['id']
        ans = row.get('answer_index', row.get('answer'))
        if not isinstance(ans, int):
            raise SystemExit(f'{qid}: missing integer answer_index')
        questions.append({k: v for k, v in row.items() if k not in ('answer_index', 'answer')})
        key.append({'id': qid, 'answer_index': ans})
    Path(args.questions_out).write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding='utf-8')
    Path(args.key_out).write_text(json.dumps(key, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'questions': len(questions), 'key': len(key)}, ensure_ascii=False))

if __name__ == '__main__':
    main()
