#!/usr/bin/env python3
from __future__ import annotations

import json
import socket
import ssl
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
TIMEOUT = 10
UA = "ir-net-atlas/1.1 (+https://github.com/sinavm/ir-net-atlas)"


def quality(ms: int, ok: bool) -> str:
    if not ok:
        return "down"
    if ms < 200:
        return "fast"
    if ms < 800:
        return "ok"
    return "slow"


def dns_ms(host: str) -> int | None:
    started = time.perf_counter()
    try:
        socket.getaddrinfo(host, 443, proto=socket.IPPROTO_TCP)
        return int((time.perf_counter() - started) * 1000)
    except Exception:
        return None


def check(url: str) -> dict:
    host = urlparse(url).hostname or ""
    resolve = dns_ms(host)
    started = time.perf_counter()
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": UA})
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
            body = resp.read(256)
            ms = int((time.perf_counter() - started) * 1000)
            ok = 200 <= resp.status < 400
            return {
                "ok": ok,
                "status": resp.status,
                "ms": ms,
                "dns_ms": resolve,
                "quality": quality(ms, ok),
                "error": None,
                "bytes": len(body),
            }
    except urllib.error.HTTPError as exc:
        ms = int((time.perf_counter() - started) * 1000)
        ok = exc.code in (401, 403, 429) or 200 <= exc.code < 400
        return {
            "ok": ok,
            "status": exc.code,
            "ms": ms,
            "dns_ms": resolve,
            "quality": quality(ms, ok),
            "error": f"http_{exc.code}",
            "bytes": 0,
        }
    except Exception as exc:
        ms = int((time.perf_counter() - started) * 1000)
        return {
            "ok": False,
            "status": 0,
            "ms": ms,
            "dns_ms": resolve,
            "quality": "down",
            "error": type(exc).__name__,
            "bytes": 0,
        }


def layer_summary(rows: list[dict]) -> dict:
    out = {}
    for row in rows:
        key = row.get("layer") or "other"
        bucket = out.setdefault(key, {"up": 0, "down": 0, "ms": []})
        if row["ok"]:
            bucket["up"] += 1
            bucket["ms"].append(row["ms"])
        else:
            bucket["down"] += 1
    for key, bucket in out.items():
        vals = bucket.pop("ms")
        bucket["avg_ms"] = int(sum(vals) / len(vals)) if vals else None
        total = bucket["up"] + bucket["down"]
        bucket["ratio"] = round(100 * bucket["up"] / total, 1) if total else 0
    return out


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    targets = json.loads((ROOT / "targets.json").read_text(encoding="utf-8"))["targets"]
    results = []
    up = 0
    latencies = []
    for item in targets:
        probe = check(item["url"])
        results.append({**item, **probe})
        if probe["ok"]:
            up += 1
            latencies.append(probe["ms"])
        print(f"{item['id']:12} {probe['quality']:5} {probe['ms']}ms dns={probe['dns_ms']}")
    total = len(results)
    ratio = round(100 * up / total, 1) if total else 0
    snapshot = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "probe_from": "github-actions",
        "disclaimer": "Probe runs outside Iran. Domestic reachability from inside Iran is collected separately.",
        "summary": {
            "up": up,
            "down": total - up,
            "total": total,
            "ratio": ratio,
            "avg_ms": int(sum(latencies) / len(latencies)) if latencies else None,
        },
        "layers": layer_summary(results),
        "targets": results,
        "iran_reports": json.loads((ROOT / "reports" / "iran.json").read_text(encoding="utf-8"))
        if (ROOT / "reports" / "iran.json").exists()
        else [],
    }
    (DOCS / "status.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    history_path = DOCS / "history.json"
    history = []
    if history_path.exists():
        try:
            history = json.loads(history_path.read_text(encoding="utf-8"))
        except Exception:
            history = []
    history.append({"generated_at": snapshot["generated_at"], "ratio": ratio, "up": up, "avg_ms": snapshot["summary"]["avg_ms"]})
    history_path.write_text(json.dumps(history[-72:], ensure_ascii=False, indent=2), encoding="utf-8")
    color = "22c55e" if ratio >= 85 else "eab308" if ratio >= 60 else "ef4444"
    (DOCS / "badge.svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="176" height="20"><rect width="176" height="20" rx="4" fill="#0f172a"/><text x="8" y="14" fill="#94a3b8" font-size="11" font-family="Verdana">atlas</text><text x="52" y="14" fill="#{color}" font-size="11" font-family="Verdana">{up}/{total} · {snapshot["summary"]["avg_ms"] or "—"}ms</text></svg>\n',
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
