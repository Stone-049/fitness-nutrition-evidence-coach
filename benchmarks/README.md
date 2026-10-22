# Benchmarks

This directory contains reproducibility checks and evaluation guidance.

## Run smoke tests

```bash
python benchmarks/run_smoke_tests.py
```

The smoke tests check:

- coaching-profile validation
- training CSV import
- weekly review generation
- question-bank schema
- blind scoring

## Current evidence

- GitHub skill scan: 909 `SKILL.md` files
- Reference catalog: 100 skills
- Academic index: 31 papers
- Community corpus: 3,854 public items
- De-identified case prototypes: 20

## Important limitation

These are structural and regression checks. They do not prove real-world coaching effectiveness, clinical safety, or certification readiness.

Read `EVALUATION_PROTOCOL.md` before claiming performance improvements.
