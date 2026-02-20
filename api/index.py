from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import json
import statistics
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "latency_data.json")
with open(DATA_PATH) as f:
    TELEMETRY = json.load(f)

class LatencyRequest(BaseModel):
    regions: List[str]
    threshold_ms: float

def percentile(data: List[float], p: float) -> float:
    if not data:
        return 0.0
    sorted_data = sorted(data)
    n = len(sorted_data)
    index = (p / 100) * (n - 1)
    lower = int(index)
    upper = lower + 1
    if upper >= n:
        return sorted_data[-1]
    fraction = index - lower
    return sorted_data[lower] + fraction * (sorted_data[upper] - sorted_data[lower])

@app.post("/api")
async def latency_metrics(req: LatencyRequest):
    result = {}
    for region in req.regions:
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
            "breaches": sum(1 for l in latencies if l > req.threshold_ms),
        }
    return result
```

---

**File 2: `api/latency_data.json`**

Copy the entire JSON from the file you uploaded (`q-vercel-latency.json`) — paste it as-is.

---

**File 3: `requirements.txt`**
```
fastapi
