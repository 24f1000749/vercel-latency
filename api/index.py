from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import statistics

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TELEMETRY = [
  {"region":"apac","latency_ms":235.92,"uptime_pct":99.191},
  {"region":"apac","latency_ms":154.94,"uptime_pct":98.389},
  {"region":"apac","latency_ms":138.48,"uptime_pct":99.252},
  {"region":"apac","latency_ms":136.85,"uptime_pct":98.397},
  {"region":"apac","latency_ms":168.88,"uptime_pct":98.671},
  {"region":"apac","latency_ms":203.98,"uptime_pct":98.999},
  {"region":"apac","latency_ms":208.31,"uptime_pct":97.918},
  {"region":"apac","latency_ms":199.68,"uptime_pct":98.109},
  {"region":"apac","latency_ms":152.56,"uptime_pct":97.993},
  {"region":"apac","latency_ms":128.33,"uptime_pct":98.604},
  {"region":"apac","latency_ms":123.52,"uptime_pct":98.931},
  {"region":"apac","latency_ms":207.12,"uptime_pct":99.319},
  {"region":"emea","latency_ms":198.95,"uptime_pct":97.464},
  {"region":"emea","latency_ms":132.51,"uptime_pct":98.859},
  {"region":"emea","latency_ms":205.72,"uptime_pct":97.937},
  {"region":"emea","latency_ms":139.89,"uptime_pct":99.407},
  {"region":"emea","latency_ms":158.81,"uptime_pct":98.302},
  {"region":"emea","latency_ms":164.82,"uptime_pct":97.992},
  {"region":"emea","latency_ms":115.61,"uptime_pct":99.074},
  {"region":"emea","latency_ms":172.53,"uptime_pct":97.292},
  {"region":"emea","latency_ms":213.17,"uptime_pct":98.745},
  {"region":"emea","latency_ms":208.74,"uptime_pct":98.042},
  {"region":"emea","latency_ms":158.04,"uptime_pct":98.542},
  {"region":"emea","latency_ms":195.28,"uptime_pct":98.784},
  {"region":"amer","latency_ms":196.84,"uptime_pct":99.46},
  {"region":"amer","latency_ms":233.26,"uptime_pct":97.264},
  {"region":"amer","latency_ms":155.87,"uptime_pct":99.326},
  {"region":"amer","latency_ms":134.93,"uptime_pct":99.305},
  {"region":"amer","latency_ms":116.86,"uptime_pct":97.145},
  {"region":"amer","latency_ms":130.29,"uptime_pct":99.083},
  {"region":"amer","latency_ms":132.09,"uptime_pct":97.582},
  {"region":"amer","latency_ms":205.13,"uptime_pct":98.407},
  {"region":"amer","latency_ms":145.9,"uptime_pct":97.129},
  {"region":"amer","latency_ms":142.71,"uptime_pct":99.44},
  {"region":"amer","latency_ms":198.97,"uptime_pct":97.326},
  {"region":"amer","latency_ms":187.73,"uptime_pct":98.486}
]

def percentile(data, p):
    sorted_data = sorted(data)
    n = len(sorted_data)
    index = (p / 100) * (n - 1)
    lower = int(index)
    upper = lower + 1
    if upper >= n:
        return sorted_data[-1]
    return sorted_data[lower] + (index - lower) * (sorted_data[upper] - sorted_data[lower])

@app.post("/api")
async def latency_metrics(request: Request):
    body = await request.json()
    regions = body.get("regions", [])
    threshold = body.get("threshold_ms", 0)

    result = {}
    for region in regions:
        records = [r for r in TELEMETRY if r["region"] == region]
        if not records:
            result[region] = {"avg_latency": 0, "p95_latency": 0, "avg_uptime": 0, "breaches": 0}
            continue
        latencies = [r["latency_ms"] for r in records]
        uptimes = [r["uptime_pct"] for r in records]
        result[region] = {
            "avg_latency": round(statistics.mean(latencies), 4),
            "p95_latency": round(percentile(latencies, 95), 4),
            "avg_uptime": round(statistics.mean(uptimes), 4),
            "breaches": sum(1 for l in latencies if l > threshold),
        }
    return JSONResponse(content=result)
```

And also create/update **`requirements.txt`**:
```
fastapi
uvicorn
