# Project Metrics – Pokédex API

This file tracks quantitative indicators of code quality and performance.
All numbers should be reproducible via the commands in **Reproduce** blocks.

---

## 1  API Latency Benchmarks

| Route | Environment | Metric | Value | Reproduce |
|-------|-------------|--------|-------|-----------|
| `/user/login` | Local (env: Windows, Python 3.13) | **median** | **245 ms** | `pytest tests/test_benchmarks.py --benchmark-only` |
|  |  | p95 | 252 ms | JSON output: `benchmarks/auth.json` |
|  |  | Rounds × Iterations | 5 × 1 | See CLI summary |

> Guardrail: CI fails if median > 300 ms (see `tests/test_benchmarks.py`).

---

## 2  Test Suite Health

| Metric | Current | Target | Command |
|--------|---------|--------|---------|
| Unit tests passing | 7 / 7 (100 %) | 100 % | `python -m pytest -q` |
| Warnings | 0 deprecation warnings related to Firestore filters | 0 | Handled with `FieldFilter` |

*(Coverage will be added after integrating `pytest --cov`.)*

---

## 3  Static Checks

| Tool | Status | Notes |
|------|--------|-------|
| `black` | Pending | Will be added to pre-commit |
| `mypy` | Pending | To be enabled once type hints are complete |
| ESLint (Angular repo) | Pending | Tracked in front-end metrics |

---

## 4  Planned Metrics

| Area | Metric | Threshold / Goal |
|------|--------|------------------|
| **ETL** | Time to sync 151 Pokémon from PokéAPI → Firestore | ≤ 10 s |
| **Angular** | Lighthouse LCP (mobile) | ≥ 90 |
| **Error Rate** | Sentry weekly errors | < 0.1 % of requests |

---

### How to Update

1. Run the **Reproduce** command after each significant change.  
2. Paste new numbers or replace old ones; commit with message `docs: update metrics`.
3. For automated benchmarks, link the CI artifact (or Grafana panel) in the *Value* column.

