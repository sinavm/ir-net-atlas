#!/usr/bin/env python3
from __future__ import annotations
import json, ssl, time, urllib.error, urllib.request
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
TIMEOUT = 12
UA = "ir-net-atlas/1.0 (+https://github.com/sinavm/ir-net-atlas)"

def load_targets():
    return json.loads((ROOT / "targets.json").read_text(encoding="utf-8"))["targets"]

def check(url: str) -> dict:
    started = time.perf_counter()
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": UA})
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
            body = resp.read(256)
            ms = int((time.perf_counter() - started) * 1000)
            return {"ok": 200 <= resp.status < 400, "status": resp.status, "ms": ms, "error": None, "bytes": len(body)}
    except urllib.error.HTTPError as exc:
        ms = int((time.perf_counter() - started) * 1000)
        return {"ok": 200 <= exc.code < 400 or exc.code in (401, 403, 429), "status": exc.code, "ms": ms, "error": f"http_{exc.code}", "bytes": 0}
    except Exception as exc:
        ms = int((time.perf_counter() - started) * 1000)
        return {"ok": False, "status": 0, "ms": ms, "error": type(exc).__name__, "bytes": 0}

def load_history():
    path = DOCS / "history.json"
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []

def main() -> None:
    DOCS.mkdir(exist_ok=True)
    targets = load_targets()
    results = []
    up = 0
    for item in targets:
        probe = check(item["url"])
        results.append({**item, **probe})
        if probe["ok"]:
            up += 1
        print(f"{item['id']:12} ok={probe['ok']} {probe['ms']}ms {probe.get('error')}")
    total = len(results)
    ratio = round(100 * up / total, 1) if total else 0
    snapshot = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "probe_from": "github-actions",
        "disclaimer": "This run is from GitHub-hosted runners (outside Iran). Iran-user reports live in reports/iran.json.",
        "summary": {"up": up, "down": total - up, "total": total, "ratio": ratio},
        "targets": results,
    }
    iran_path = ROOT / "reports" / "iran.json"
    snapshot["iran_reports"] = json.loads(iran_path.read_text(encoding="utf-8")) if iran_path.exists() else []
    (DOCS / "status.json").write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    history = load_history()
    history.append({"generated_at": snapshot["generated_at"], "ratio": ratio, "up": up, "down": total - up})
    (DOCS / "history.json").write_text(json.dumps(history[-72:], ensure_ascii=False, indent=2), encoding="utf-8")
    color = "22c55e" if ratio >= 85 else "eab308" if ratio >= 60 else "ef4444"
    (DOCS / "badge.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="168" height="20"><rect width="168" height="20" rx="4" fill="#0f172a"/><text x="8" y="14" fill="#94a3b8" font-size="11" font-family="Verdana">atlas</text><text x="52" y="14" fill="#{color}" font-size="11" font-family="Verdana">{up}/{total} up · {ratio}%</text></svg>\n', encoding="utf-8")
    print("wrote docs/status.json", ratio)

if __name__ == "__main__":
    main()
