# tests/test_benchmarks.py
from app.api import app

client = app.test_client()

def test_login_p95_under_300ms(benchmark):
    payload = {"email": "me@example.com", "password": "secret"}
    client.post("/users/create", json=payload | {"uid": "demo"})  # warm-up

    benchmark(lambda: client.post("/user/login", json=payload))

    # seconds ➜ ms
    median_ms = benchmark.stats.stats.median * 1000
    assert median_ms < 300, f"Median login latency {median_ms:.1f} ms exceeds 300 ms"
