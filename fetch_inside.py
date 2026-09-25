#!/usr/bin/env python3
"""Collect inside-Iran measurements.
Primary: public radar monitoring API.
Fallback: OONI measurements from probe_cc=IR.
The public page never names third-party products.
"""
from __future__ import annotations

import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
UA = "ir-net-atlas/1.2 (+https://github.com/sinavm/ir-net-atlas)"
ISPS = {
    "mci": "همراه اول",
    "irancell": "ایرانسل",
    "afranet": "افرانت",
    "parsonline": "پارس‌آنلاین",
    "mobinnet": "مبین‌نت",
}
RADAR = "https://radar.arvancloud.ir/api/v1/internet-monitoring?isp={isp}"
OONI = "https://api.ooni.io/api/v1/measurements?probe_cc=IR&test_name=web_connectivity&limit=40"


def get(url: str, timeout: int = 20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read(2_000_000)
    return json.loads(raw.decode("utf-8", "replace"))


def last_point(series):
    if not isinstance(series, list) or not series:
        return None
    val = series[-1]
    if isinstance(val, dict):
        return val.get("value", val.get("y", val.get("loss")))
    return val


def fetch_radar() -> dict | None:
    isps = []
    for key, title in ISPS.items():
        try:
            payload = get(RADAR.format(isp=key), timeout=18)
        except Exception as exc:
            print("radar miss", key, type(exc).__name__)
            continue
        services = []
        if isinstance(payload, dict):
            for name, series in payload.items():
                if name in ("isp", "timestamp", "meta"):
                    continue
                point = last_point(series) if not isinstance(series, (int, float)) else series
                if point is None:
                    continue
                try:
                    score = float(point)
                except Exception:
                    continue
                services.append({"id": str(name), "score": score, "ok": score < 50})
        if services:
            isps.append({"isp": key, "title": title, "services": services[:12]})
    if not isps:
        return None
    return {"source": "in-country-radar", "ok": True, "isps": isps}


def fetch_ooni() -> dict | None:
    try:
        payload = get(OONI, timeout=25)
    except Exception as exc:
        print("ooni miss", type(exc).__name__)
        return None
    rows = payload.get("results") if isinstance(payload, dict) else payload
    if not isinstance(rows, list):
        return None
    grouped = {}
    for row in rows:
        url = ((row.get("input") or "").split("/") + [""])[2] or row.get("input") or "unknown"
        anomaly = bool(row.get("anomaly") or row.get("confirmed"))
        isp = (row.get("probe_asn") or "AS0")
        item = grouped.setdefault(isp, {"isp": isp, "title": isp, "services": []})
        item["services"].append({
            "id": url,
            "ok": not anomaly,
            "score": 80 if anomaly else 5,
        })
    isps = list(grouped.values())[:8]
    if not isps:
        return None
    return {"source": "in-country-measurements", "ok": True, "isps": isps}


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    path = DOCS / "inside.json"
    data = fetch_radar() or fetch_ooni()
    if not data:
        if path.exists():
            prev = json.loads(path.read_text(encoding="utf-8"))
            prev["stale"] = True
            path.write_text(json.dumps(prev, ensure_ascii=False, indent=2), encoding="utf-8")
            print("kept stale inside.json")
            return
        data = {"source": "none", "ok": False, "isps": [], "stale": True}
    data["generated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    data["label"] = "پروب از داخل ایران"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("wrote", data["source"], "isps", len(data.get("isps", [])))


if __name__ == "__main__":
    main()
