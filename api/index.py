import json, statistics
from http.server import BaseHTTPRequestHandler

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

def pct(data, p):
    s = sorted(data); n = len(s)
    i = (p/100)*(n-1); lo = int(i); hi = lo+1
    return s[-1] if hi >= n else s[lo]+(i-lo)*(s[hi]-s[lo])

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length",0))))
        regions, threshold = body.get("regions",[]), body.get("threshold_ms",0)
        result = {}
        for region in regions:
            rows = [r for r in TELEMETRY if r["region"]==region]
            lat = [r["latency_ms"] for r in rows]
            upt = [r["uptime_pct"] for r in rows]
            result[region] = {
                "avg_latency": round(statistics.mean(lat),4),
                "p95_latency": round(pct(lat,95),4),
                "avg_uptime": round(statistics.mean(upt),4),
                "breaches": sum(1 for l in lat if l > threshold)
            }
        res = json.dumps(result).encode()
        self.send_response(200)
        self._cors()
        self.send_header("Content-Type","application/json")
        self.send_header("Content-Length",str(len(res)))
        self.end_headers()
        self.wfile.write(res)

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods","GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers","*")
