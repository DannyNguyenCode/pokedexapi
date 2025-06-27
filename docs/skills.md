# Skills & Achievements Log

> One-liner purpose: Track résumé-worthy wins while building **Pokédex API**.

| Date | Area | Achievement | Notes / Metrics |
|------|------|-------------|-----------------|
| 2025-06-27 | **Testing & CI** | Added `pytest-benchmark`; CI fails if login median > 300 ms | Median 245 ms (local), artifact: `benchmarks/auth.json` |
| 2025-06-27 | **Performance Monitoring** | Built Flask request-timing middleware; adds `X-Response-Time` header | p95 & p50 logged to Cloud Logs |
| 2025-06-27 | **Firestore v2.x** | Replaced positional filters with `FieldFilter` / keyword API | No deprecation warnings on client v2.11 |
| 2025-06-27 | **Timezone Safety** | Switched from `datetime.utcnow()` to `datetime.now(UTC)` | Future-proofs JWT expiry handling |
| 2025-06-27 | **Robust CRUD Layer** | Standardised on `.get()` to return deterministic lists; fixed unit tests | 100 % test pass rate |
| 2025-06-27 | **Debugging Discipline** | Traced MagicMock vs iterable mismatch; resolved missing `()` errors | Maintains green builds |

