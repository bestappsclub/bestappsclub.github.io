#!/usr/bin/env python3
"""Refresh data/stops.json from GoSG's public Firestore copy of LTA Bus Stops (bus_stops_v2).
LTA changes stops a few times a year; run this after the quarterly syncbusstops job."""
import json, os, urllib.request
BASE = "https://firestore.googleapis.com/v1/projects/bussg-1289/databases/(default)/documents/bus_stops_v2/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "stops.json")

def get(doc):
    with urllib.request.urlopen(BASE + doc, timeout=30) as r:
        return json.load(r)["fields"]

def val(v):
    for k in ("stringValue", "integerValue", "doubleValue"):
        if k in v: return v[k]

meta = get("meta")
stops = []
for i in range(int(val(meta["chunkCount"]))):
    for s in get(f"chunk_{i}")["stops"]["arrayValue"].get("values", []):
        f = s["mapValue"]["fields"]
        stops.append([val(f["c"]), val(f["d"]), val(f["r"]), round(float(val(f["lat"])), 5), round(float(val(f["lng"])), 5)])
stops.sort()
json.dump({"v": val(meta["version"])[:8], "updated": val(meta["updatedAt"])[:10], "stops": stops},
          open(OUT, "w"), separators=(",", ":"), ensure_ascii=False)
print(len(stops), "stops →", OUT, os.path.getsize(OUT) // 1024, "KB")
