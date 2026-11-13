#!/usr/bin/env python3
"""Monthly check for new public-holiday schedules (run by .github/workflows/update-holidays.yml).

- Mainland China: NateScarlet/holiday-cn (built from the State Council notice).
- Singapore: data.gov.sg collection 691 "Singapore Public Holidays" (Ministry of Manpower).

For this year and next, a year is (re)written only when its set of (date, type) changes, so name
differences never cause churn. Writes a summary to holiday-update.md and prints changed=true|false
for GitHub Actions. Standard library only.
"""
import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # data/
TODAY = dt.date.today()
YEARS = [TODAY.year, TODAY.year + 1]
UA = {"User-Agent": "bestappsclub-holiday-updater"}

SG_NAMES = {
    "New Year's Day": "元旦", "New Year’s Day": "元旦", "Chinese New Year": "春节",
    "Hari Raya Puasa": "开斋节", "Good Friday": "受难日", "Labour Day": "劳动节",
    "Hari Raya Haji": "哈芝节", "Vesak Day": "卫塞节", "National Day": "国庆日",
    "Deepavali": "屠妖节", "Christmas Day": "圣诞节", "Polling Day": "投票日",
}


def get_json(url, tries=5):
    """GET JSON; None on 404. Backs off on 429/5xx (data.gov.sg rate-limits shared CI IPs)."""
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code in (429, 500, 502, 503, 504) and attempt < tries - 1:
                wait = int(e.headers.get("Retry-After") or 0) or 10 * (attempt + 1)
                time.sleep(min(wait, 60))
                continue
            raise


# ---------- sources ----------

def fetch_cn(year):
    d = get_json(f"https://raw.githubusercontent.com/NateScarlet/holiday-cn/master/{year}.json")
    if not d or not d.get("days"):
        return None, None
    days = {}
    for x in d["days"]:
        name = x["name"]
        if x["isOffDay"]:
            days[x["date"]] = {"name": name, "type": "holiday"}
        else:
            days[x["date"]] = {"name": ("国庆" if name == "国庆节" else name) + "调休", "type": "workday"}
    source = "、".join(d.get("papers") or []) or "NateScarlet/holiday-cn"
    return days, f"国务院办公厅关于{year}年部分节假日安排的通知（{source}）"


def fetch_sg_all():
    meta = get_json("https://api-production.data.gov.sg/v2/public/api/collections/691/metadata")
    ids = meta["data"]["collectionMetadata"]["childDatasets"]
    out = {}
    for rid in reversed(ids):   # newest datasets are listed last
        if all(y in out for y in YEARS):
            break
        time.sleep(3)
        res = get_json(f"https://data.gov.sg/api/action/datastore_search?resource_id={rid}&limit=100")
        recs = (res or {}).get("result", {}).get("records", [])
        if not recs:
            continue
        year = int(recs[0]["date"][:4])
        if year < min(YEARS):
            break                # older than anything we need
        if year not in YEARS:
            continue
        days, unknown = {}, []
        for r in recs:
            raw = r["holiday"].strip()
            observed = raw.endswith("(Observed)")
            base = raw.replace("(Observed)", "").strip()
            zh = SG_NAMES.get(base)
            if zh is None:
                unknown.append(raw)
                zh = base
            days[r["date"]] = {"name": zh + ("补假" if observed else ""), "type": "holiday"}
        out[year] = (days, f"data.gov.sg {rid} (MOM)", unknown)
    return out


# ---------- checks ----------

def check(region, year, days):
    problems = []
    for date, v in days.items():
        d = dt.date.fromisoformat(date)
        if d.year != year:
            problems.append(f"{date} 不在 {year} 年")
        if region == "cn" and v["type"] == "workday" and d.weekday() < 5:
            problems.append(f"{date} 调休上班却不是周末")
    holidays = sum(v["type"] == "holiday" for v in days.values())
    if region == "cn" and not 20 <= holidays <= 45:
        problems.append(f"放假天数 {holidays} 不正常")
    if region == "sg" and not 9 <= holidays <= 16:
        problems.append(f"公共假期 {holidays} 天不正常")
    return problems


def key_set(days):
    return {(k, v["type"]) for k, v in days.items()}


# ---------- main ----------

def main():
    report, changed = [], False
    for region in ("cn", "sg"):
        path = os.path.join(ROOT, f"{region}-holidays.json")
        data = json.load(open(path, encoding="utf-8"))
        found = {}
        try:
            if region == "cn":
                for y in YEARS:
                    days, src = fetch_cn(y)
                    if days:
                        found[y] = (days, src, [])
            else:
                found = fetch_sg_all()
        except Exception as e:  # a source being down shouldn't fail the whole check
            report.append(f"- ⚠️ {region}: 这次取不到数据（{e}），下个月会再试")
            continue

        for y in YEARS:
            if y not in found:
                report.append(f"- {region} {y}: 还没有公布")
                continue
            days, src, unknown = found[y]
            mine = {k: v for k, v in data["days"].items() if k.startswith(f"{y}-")}
            if key_set(mine) == key_set(days):
                report.append(f"- {region} {y}: 和现有数据一致")
                continue
            problems = check(region, y, days)
            added = sorted(key_set(days) - key_set(mine))
            removed = sorted(key_set(mine) - key_set(days))
            report.append(f"- **{region} {y}: 有更新**（来源：{src}）")
            report += [f"  - 新增 {d} {t} {days[d]['name']}" for d, t in added]
            report += [f"  - 删除 {d} {t}" for d, t in removed]
            report += [f"  - ⚠️ {p}" for p in problems]
            report += [f"  - ⚠️ 没有对应中文名的假期：{u}" for u in unknown]
            data["days"] = {k: v for k, v in data["days"].items() if not k.startswith(f"{y}-")} | days
            data["days"] = dict(sorted(data["days"].items()))
            data["years"] = sorted(set(data["years"]) | {y})
            data.setdefault("sources", {})[str(y)] = src
            data["updated"] = TODAY.isoformat()
            changed = True
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)

    # December and next year's China schedule still missing: say so in the report.
    cn = json.load(open(os.path.join(ROOT, "cn-holidays.json"), encoding="utf-8"))
    missing_next_cn = TODAY.month == 12 and (TODAY.year + 1) not in cn["years"]
    if missing_next_cn:
        report.append(f"- ⚠️ 已经 12 月，还没有 {TODAY.year + 1} 年中国大陆放假安排，请手动确认。")

    body = "\n".join(["节假日数据检查（" + TODAY.isoformat() + "）", ""] + report)
    open("holiday-update.md", "w", encoding="utf-8").write(body + "\n")
    print(body, file=sys.stderr)
    print(f"changed={'true' if changed else 'false'}")
    print(f"missing_next_cn={'true' if missing_next_cn else 'false'}")


if __name__ == "__main__":
    main()
