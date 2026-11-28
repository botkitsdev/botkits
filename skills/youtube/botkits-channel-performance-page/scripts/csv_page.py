#!/usr/bin/env python3
"""Turn a YouTube Studio CSV export for one channel into one visual HTML page.

Usage:
  python3 csv_page.py EXPORT.csv --out page.html [--channel "My channel"]
                      [--title "The finding in a few words"] [--new-days 7]
                      [--short-max-s 180]

Needs Python 3.9+ and nothing else. The page loads fonts from Google Fonts
when online and falls back to system fonts offline.
"""
import argparse
import csv
import html
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "template.html"

# Studio renames columns now and then, and exports in the account's language.
# Each field lists the English headers seen so far, lowercased. Add yours here.
ALIASES = {
    "id": ["content", "video id", "video"],
    "title": ["video title", "title"],
    "date": ["video publish time", "publish time", "published", "date"],
    "duration": ["duration", "duration (s)"],
    "type": ["content type", "type", "format"],
    "visibility": ["visibility", "privacy"],
    "views": ["views"],
    "watch_h": ["watch time (hours)", "watch time"],
    "subs": ["subscribers", "subscribers gained", "net subscribers"],
    "impressions": ["impressions"],
    "ctr": ["impressions click-through rate (%)", "impressions ctr (%)", "ctr (%)", "ctr"],
    "avd": ["average view duration", "avg view duration"],
    "avg_pct": ["average percentage viewed (%)", "avg percentage viewed (%)", "average % viewed"],
    "stayed": ["stayed to watch (%)", "stayed to watch", "viewed (vs. swiped away) (%)", "viewed vs swiped away (%)"],
}
SUFFIX = {"k": 1e3, "m": 1e6, "b": 1e9}
STAYED_BANDS = (40.0, 25.0)  # 40%+ strong, 25-40% middle, under 25% weak
CTR_BANDS = (4.0, 2.0)


def parse_num(raw):
    """'1,234' -> 1234, '1.2K' -> 1200, '3.9%' -> 3.9, '' or '-' -> None."""
    if raw is None:
        return None
    s = str(raw).strip().replace(" ", "").replace(",", "").rstrip("%").strip()
    if s in ("", "-", "—", "–"):
        return None
    m = re.fullmatch(r"([-+]?\d*\.?\d+)\s*([kKmMbB]?)", s)
    if not m:
        return None
    n = float(m.group(1)) * SUFFIX.get(m.group(2).lower(), 1)
    return int(n) if n.is_integer() else n


def parse_seconds(raw):
    """'0:01:19' or '1:19' -> 79, '742' -> 742."""
    if raw is None or str(raw).strip() == "":
        return None
    s = str(raw).strip()
    if ":" in s:
        try:
            parts = [float(p) for p in s.split(":")]
        except ValueError:
            return None
        total = 0.0
        for p in parts:
            total = total * 60 + p
        return int(total)
    n = parse_num(s)
    return None if n is None else int(n)


def parse_date(raw):
    s = (raw or "").strip()
    for fmt in ("%b %d, %Y", "%Y-%m-%d", "%d %b %Y", "%B %d, %Y", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def iso(d):
    return d.isoformat() if d else ""


def map_columns(header):
    lower = [h.strip().lower() for h in header]
    cols = {}
    for field, names in ALIASES.items():
        for n in names:
            if n in lower:
                cols[field] = lower.index(n)
                break
    return cols


def read_export(path, short_max_s=180):
    """Return (rows, total_row, gaps). Keeps the raw string next to each parsed count."""
    text = Path(path).read_text(encoding="utf-8-sig")
    reader = list(csv.reader(text.splitlines()))
    if not reader:
        raise SystemExit(f"{path}: the file is empty.")
    cols = map_columns(reader[0])
    for need in ("title", "views"):
        if need not in cols:
            raise SystemExit(
                f"{path}: no '{need}' column. Headers found: {reader[0]}. "
                "Export the Content tab in English, or add your header to ALIASES in csv_page.py."
            )
    gaps = []
    for field, label in (("stayed", "% stayed"), ("ctr", "CTR"), ("duration", "duration"), ("date", "publish date")):
        if field not in cols:
            gaps.append(f"no {label} column")

    def cell(r, field):
        i = cols.get(field)
        return r[i].strip() if i is not None and i < len(r) else ""

    rows, total = [], None
    for r in reader[1:]:
        if not any(c.strip() for c in r):
            continue
        first = r[0].strip().lower() if r else ""
        if first == "total" or cell(r, "title").lower() == "total":
            total = {f: parse_num(cell(r, f)) for f in ("views", "watch_h", "subs", "impressions", "ctr")}
            continue
        dur = parse_seconds(cell(r, "duration"))
        kind = cell(r, "type").lower()
        if "short" in kind:
            kind = "short"
        elif kind:
            kind = "video"
        elif dur is not None:
            kind = "short" if dur <= short_max_s else "video"
        else:
            kind = "video"
        rows.append({
            "id": cell(r, "id"),
            "title": cell(r, "title"),
            "type": kind,
            "date": iso(parse_date(cell(r, "date"))),
            "visibility": cell(r, "visibility") or "Public",
            "views": parse_num(cell(r, "views")) or 0,
            "views_raw": cell(r, "views"),
            "watch_h": parse_num(cell(r, "watch_h")),
            "subs": parse_num(cell(r, "subs")),
            "impressions": parse_num(cell(r, "impressions")),
            "ctr": parse_num(cell(r, "ctr")),
            "avd_s": parse_seconds(cell(r, "avd")),
            "avg_pct": parse_num(cell(r, "avg_pct")),
            "stayed": parse_num(cell(r, "stayed")),
            "duration_s": dur,
        })
    if not rows:
        raise SystemExit(f"{path}: no video rows under the header.")
    if any(re.search(r"\d[kKmM]$", r["views_raw"]) for r in rows):
        gaps.append("Studio rounded some counts (1.2K), so totals are close, not exact")
    return rows, total, gaps


def band(v, bands):
    if v is None:
        return ""
    return "hi" if v >= bands[0] else "mid" if v >= bands[1] else "lo"


def short_label(title, n=46):
    t = " ".join(title.split())
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"


def build(rows, total, gaps, channel, title=None, new_days=7, source="Studio export"):
    dates = [date.fromisoformat(r["date"]) for r in rows if r["date"]]
    newest = max(dates) if dates else None
    cutoff = newest - timedelta(days=new_days) if newest else None
    for r in rows:
        r["new"] = bool(cutoff and r["date"] and date.fromisoformat(r["date"]) > cutoff)

    def tot(field):
        if total and total.get(field) is not None:
            return total[field]
        vals = [r[field] for r in rows if r.get(field) is not None]
        return sum(vals) if vals else None

    imp = [(r["impressions"], r["ctr"]) for r in rows if r["impressions"] and r["ctr"] is not None]
    ctr_all = (total or {}).get("ctr")
    if ctr_all is None and imp:
        ctr_all = round(sum(i * c for i, c in imp) / sum(i for i, _ in imp), 1)

    shorts = [r for r in rows if r["type"] == "short"]
    longs = [r for r in rows if r["type"] == "video"]
    stayed = sorted((r for r in shorts if r["stayed"] is not None), key=lambda r: -r["stayed"])
    ctr_long = sorted((r for r in longs if r["ctr"] is not None), key=lambda r: -r["ctr"])
    if shorts and not stayed and "no % stayed column" not in gaps:
        gaps.append("% stayed empty for every Short")

    by_views = sorted(rows, key=lambda r: -r["views"])
    wins = [{"t": short_label(r["title"], 40), "v": f"{r['views']:,} views"} for r in by_views[:2]]
    loses = []
    for r in stayed[::-1]:
        if r["stayed"] < STAYED_BANDS[1] and len(loses) < 2:
            loses.append({"t": short_label(r["title"], 40), "v": f"{r['stayed']:.0f}% stayed"})
    for r in ctr_long[::-1]:
        if r["ctr"] < CTR_BANDS[1] and len(loses) < 3:
            loses.append({"t": short_label(r["title"], 40), "v": f"{r['ctr']:.1f}% CTR"})

    if not title:
        top = by_views[0]
        kind = "Short" if top["type"] == "short" else "video"
        title = f"One {kind} brought {round(100 * top['views'] / max(tot('views') or 1, 1))}% of views"

    tiles = [
        {"k": "Views", "v": tot("views")},
        {"k": "Watch hours", "v": tot("watch_h")},
        {"k": "Subscribers", "v": tot("subs"), "sign": True},
        {"k": "CTR", "v": ctr_all, "unit": "%"},
        {"k": "Uploads", "v": len(rows), "sm": f"{len(shorts)} Shorts · {len(longs)} long"},
    ]
    if stayed:
        tiles.append({"k": "Best % stayed", "v": stayed[0]["stayed"], "unit": "%", "sm": short_label(stayed[0]["title"], 28)})

    span = f"{min(dates).strftime('%d %b')} to {newest.strftime('%d %b %Y')}" if dates else "dates not in export"
    return {
        "channel": channel,
        "title": title,
        "sub": f"{channel} · {len(rows)} uploads, {span}",
        "tiles": tiles,
        "wins": wins,
        "loses": loses,
        "stayed": [{"t": short_label(r["title"]), "p": r["stayed"], "b": band(r["stayed"], STAYED_BANDS), "new": r["new"]} for r in stayed],
        "ctr": [{"t": short_label(r["title"]), "p": r["ctr"], "b": band(r["ctr"], CTR_BANDS)} for r in ctr_long],
        "newDays": new_days,
        "foot": "; ".join([f"Source: {source}", f"{len(rows)} rows read"] + gaps) + ".",
    }


def render(data):
    tpl = TEMPLATE.read_text(encoding="utf-8")
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return (tpl.replace("{{TITLE}}", html.escape(data["title"]))
               .replace("{{H1}}", html.escape(data["title"]))
               .replace("{{SUB}}", html.escape(data["sub"]))
               .replace("/*{{DATA}}*/null", blob))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("csv", help="Studio export, Content tab, 'Export current view' as CSV")
    ap.add_argument("--out", default="channel-page.html")
    ap.add_argument("--channel", default="Your channel", help="name shown on the page")
    ap.add_argument("--title", help="the finding in a few words; default is generated")
    ap.add_argument("--new-days", type=int, default=7, help="star uploads this many days before the newest one")
    ap.add_argument("--short-max-s", type=int, default=180, help="longest duration counted as a Short")
    ap.add_argument("--json", help="also write the page data as JSON here")
    a = ap.parse_args(argv)
    rows, total, gaps = read_export(a.csv, a.short_max_s)
    data = build(rows, total, gaps, a.channel, a.title, a.new_days, source=Path(a.csv).name)
    Path(a.out).write_text(render(data), encoding="utf-8")
    if a.json:
        Path(a.json).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {a.out}: {len(rows)} uploads, {len(data['stayed'])} Shorts with % stayed, {len(data['ctr'])} long videos with CTR.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
