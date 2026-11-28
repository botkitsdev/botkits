#!/usr/bin/env python3
"""channel_scan.py: read-only scan of one public YouTube channel.

Needs: python3.9+ and yt-dlp on PATH. Pillow is optional (thumbnail sheet).
Never signs in. No API key needed.

Usage:
  python3 channel_scan.py @handle [--long 60] [--shorts 60] [--niche education]
                                  [--out DIR] [--thumbs 6] [--workers 6]

Writes to DIR: videos.csv, summary.json, report.md, thumbs/ (optional).
Prints report.md at the end.
"""
import argparse, csv, datetime as dt, json, os, re, shutil, statistics as st
import subprocess, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
RPM_FILE = os.path.join(HERE, "..", "data", "rpm-bands.json")
TODAY = dt.date.today()


def die(msg):
    sys.exit("channel_scan: " + msg)


def ytdlp(args, retries=3):
    for i in range(retries):
        p = subprocess.run(["yt-dlp", "--no-warnings"] + args,
                           capture_output=True, text=True)
        if p.returncode == 0 and p.stdout.strip():
            return p.stdout
        time.sleep(1.5 * (i + 1))
    return None


def channel_url(arg):
    a = arg.strip().rstrip("/")
    a = re.sub(r"/(videos|shorts|streams|featured)$", "", a)
    if a.startswith("http"):
        return a
    if a.startswith("@"):
        return "https://www.youtube.com/" + a
    if a.startswith("UC"):
        return "https://www.youtube.com/channel/" + a
    return "https://www.youtube.com/@" + a


def flat(url, n):
    out = ytdlp(["--flat-playlist", "-J", "--playlist-items", "1:%d" % n, url])
    if not out:
        return None, []
    d = json.loads(out)
    return d, [e for e in d.get("entries", []) if e and e.get("id")]


def detail(vid):
    out = ytdlp(["-j", "--skip-download", "--ignore-no-formats-error",
                 "https://www.youtube.com/watch?v=" + vid])
    if not out:
        return None
    return json.loads(out.split("\n")[0])


def parse_date(d):
    if d.get("upload_date"):
        s = d["upload_date"]
        return dt.date(int(s[:4]), int(s[4:6]), int(s[6:]))
    if d.get("timestamp"):
        return dt.datetime.utcfromtimestamp(d["timestamp"]).date()
    return None


def collect(url, tab, n, workers):
    top, entries = flat(url + "/" + tab, n)
    if not entries:
        return top, []
    with ThreadPoolExecutor(workers) as ex:
        details = list(ex.map(lambda e: detail(e["id"]), entries))
    rows = []
    for e, d in zip(entries, details):
        d = d or {}
        live = d.get("live_status") in ("was_live", "is_live") or d.get("was_live")
        rows.append({
            "id": e["id"],
            "title": d.get("title") or e.get("title") or "",
            "format": "live" if live else ("short" if tab == "shorts" else "long"),
            "date": parse_date(d),
            "duration": d.get("duration") or e.get("duration") or 0,
            "views": d.get("view_count") if d.get("view_count") is not None else e.get("view_count"),
            "likes": d.get("like_count"),
            "comments": d.get("comment_count"),
        })
    return top, rows


def med(xs):
    xs = [x for x in xs if x is not None]
    return st.median(xs) if xs else None


def add_scores(rows, min_age):
    """Score each video against its own channel, same format only."""
    for fmt in ("long", "short"):
        v = [r for r in rows if r["format"] == fmt and r["date"] and r["views"] is not None]
        for r in v:
            r["age"] = (TODAY - r["date"]).days
            r["vpd"] = r["views"] / max(r["age"], 1)
        matured = [r["views"] for r in v if r["age"] >= min_age]
        base = med(matured) if len(matured) >= 5 else None
        v.sort(key=lambda r: r["date"])
        for i, r in enumerate(v):
            r["base"] = base
            r["score"] = round(r["views"] / base, 2) if base else None
            prior = [p["views"] for p in v[max(0, i - 10):i]]
            r["score_roll"] = round(r["views"] / med(prior), 2) if len(prior) >= 3 and med(prior) else None
            r["young"] = r["age"] < min_age
            s = r["score"]
            r["band"] = ("" if s is None else "BREAKOUT" if s >= 10 else
                         "OUTLIER" if s >= 3 else "FLOP" if s <= 0.5 else "normal")


FEATURES = {
    "number": r"\d",
    "year": r"\b20\d\d\b",
    "question": r"\?",
    "brackets": r"[\(\[]",
    "colon_or_pipe": r"[:|]",
    "first_person": r"\bI\b|\bI'm\b|\bI've\b|(?i:\b(my|we|our)\b)",
    "how_to": r"\bhow to\b|\btutorial\b|\bguide\b|\bstep by step\b",
    "versus": r"\bvs\.?\b|\bversus\b",
    "best_or_review": r"\b(best|top \d+|review|worth it)\b",
    "tested_or_built": r"\b(tested|tried|built|made|spent|quit|gave)\b",
    "money": r"[$€£]|\bfree\b|\bcost\b",
    "caps_word": r"\b[A-Z]{3,}\b",
}
SEARCH_RE = re.compile(r"\bhow to\b|\btutorial\b|\bguide\b|\bvs\.?\b|\bversus\b|\bbest\b|\breview\b|"
                       r"\bexplained\b|\bfor beginners\b|\bwhat is\b|\bstep by step\b|\bsetup\b|"
                       r"\binstall\b|\bfix\b|\btemplate\b|\b20\d\d\b", re.I)
BROWSE_RE = re.compile(r"\bI\b|\bmy\b|\bwe\b|\btested\b|\btried\b|\bbuilt\b|\bspent\b|\bquit\b|"
                       r"\bnever\b|\bworst\b|\bsecret\b|\btruth\b|\bwhy\b|\bstop\b|\?", re.I)


def title_feats(t):
    return {k: bool(re.search(p, t, re.I if k not in ("caps_word", "first_person") else 0))
            for k, p in FEATURES.items()}


def lane(t):
    s, b = len(SEARCH_RE.findall(t)), len(BROWSE_RE.findall(t))
    if s == b == 0:
        return "unclear"
    return "search" if s > b else "browse" if b > s else "mixed"


def cadence(rows, fmt):
    d = sorted([r["date"] for r in rows if r["format"] == fmt and r["date"]], reverse=True)
    if not d:
        return None
    gaps = [(d[i] - d[i + 1]).days for i in range(len(d) - 1)]
    cnt = lambda days: sum(1 for x in d if (TODAY - x).days <= days)
    wd = [0] * 7
    for x in d:
        wd[x.weekday()] += 1
    return {"n_in_sample": len(d), "span_days": (TODAY - d[-1]).days, "first": str(d[-1]), "last": str(d[0]),
            "days_since_last": (TODAY - d[0]).days, "last30": cnt(30), "last90": cnt(90),
            "last365": cnt(365), "median_gap_days": med(gaps), "max_gap_days": max(gaps) if gaps else None,
            "weekday_mon_to_sun": wd}


def length_buckets(rows, fmt):
    edges = ([(0, 30, "<30s"), (30, 61, "30-60s"), (61, 10**6, ">60s")] if fmt == "short" else
             [(0, 240, "<4m"), (240, 480, "4-8m"), (480, 900, "8-15m"), (900, 1800, "15-30m"), (1800, 10**9, "30m+")])
    out = []
    for lo, hi, name in edges:
        g = [r for r in rows if r["format"] == fmt and r.get("views") is not None and r["duration"] and lo <= r["duration"] < hi]
        if g:
            out.append({"bucket": name, "n": len(g), "median_views": med([r["views"] for r in g]),
                        "median_score": med([r["score"] for r in g])})
    return out


def feature_table(rows, fmt):
    g = [r for r in rows if r["format"] == fmt and r.get("score") is not None]
    outl = [r for r in g if r["score"] >= 3]
    out = []
    for k in FEATURES:
        w = [r for r in g if r["feats"][k]]
        wo = [r for r in g if not r["feats"][k]]
        out.append({"feature": k, "n_with": len(w), "n_without": len(wo),
                    "median_score_with": med([r["score"] for r in w]) if len(w) >= 3 else None,
                    "median_score_without": med([r["score"] for r in wo]) if len(wo) >= 3 else None,
                    "share_of_outliers": round(sum(1 for r in outl if r["feats"][k]) / len(outl), 2) if outl else None,
                    "share_of_all": round(len(w) / len(g), 2) if g else None})
    return out


def revenue(rows, niche):
    try:
        bands = json.load(open(RPM_FILE))
    except Exception:
        return None
    b = bands["niches"].get(niche.lower()) if niche else None
    if niche and not b:
        return {"error": "unknown niche '%s'. Known: %s" % (niche, ", ".join(sorted(bands["niches"])))}
    if not b:
        return None
    mv = med([r["views"] for r in rows if r["format"] == "long" and r.get("views") is not None and not r.get("young")])
    sv = med([r["views"] for r in rows if r["format"] == "short" and r.get("views") is not None and not r.get("young")])
    out = {"niche": niche, "rpm_low_median_high": [b["p25"], b["median"], b["p75"]], "source": bands["source"],
           "caveat": bands["caveat"]}
    if mv:
        out["median_long_views"] = mv
        out["per_typical_long_video_usd"] = [round(mv * x / 1000, 2) for x in (b["p25"], b["median"], b["p75"])]
    if sv:
        lo, hi = bands["shorts_rpm_range"]
        out["median_short_views"] = sv
        out["per_typical_short_usd"] = [round(sv * lo / 1000, 2), round(sv * hi / 1000, 2)]
    return out


def sheet(rows, outdir, k):
    try:
        from PIL import Image, ImageDraw
    except Exception:
        return None
    os.makedirs(os.path.join(outdir, "thumbs"), exist_ok=True)
    picks = []
    for fmt in ("long", "short"):
        g = sorted([r for r in rows if r["format"] == fmt and r.get("score") is not None],
                   key=lambda r: -r["score"])
        if not g:
            continue
        picks += [("TOP", r) for r in g[:k]] + [("LOW", r) for r in g[-k:] if r not in g[:k]]
    tiles = []
    for tag, r in picks:
        p = os.path.join(outdir, "thumbs", r["id"] + ".jpg")
        try:
            urllib.request.urlretrieve("https://i.ytimg.com/vi/%s/hqdefault.jpg" % r["id"], p)
            im = Image.open(p).convert("RGB").resize((320, 180))
            d = ImageDraw.Draw(im)
            d.rectangle((0, 0, 320, 16), fill=(0, 0, 0))
            d.text((3, 2), "%s %s %sx %s" % (tag, r["format"], r["score"], r["title"][:34]), fill=(255, 255, 255))
            tiles.append(im)
        except Exception:
            pass
    if not tiles:
        return None
    cols = 4
    rws = (len(tiles) + cols - 1) // cols
    sh = Image.new("RGB", (cols * 320, rws * 180), (20, 20, 20))
    for i, t in enumerate(tiles):
        sh.paste(t, ((i % cols) * 320, (i // cols) * 180))
    path = os.path.join(outdir, "thumbs", "sheet.jpg")
    sh.save(path, quality=85)
    return path


def S_span(vs):
    return max([r["age"] for r in vs], default=0)


def fmt_n(x):
    return "-" if x is None else ("%.2f" % x if isinstance(x, float) and x < 100 else "%s" % int(x))


def write_report(S, rows, outdir):
    L = ["# Channel scan: %s" % S["channel"], "",
         "Scanned %s. Subscribers: %s. Sample: %d long, %d Shorts, %d live (newest first)." % (
             TODAY, S["subscribers"], S["n_long"], S["n_short"], S["n_live"]),
         "Views are lifetime views today. Videos under %d days old are marked young and their scores are provisional." % S["min_age"], ""]
    for fmt in ("long", "short"):
        g = [r for r in rows if r["format"] == fmt and r.get("views") is not None]
        if not g:
            continue
        L += ["## %s" % ("Long-form" if fmt == "long" else "Shorts"), "",
              "Median views (matured): %s. Median views per day: %s." % (
                  fmt_n(S["baseline"].get(fmt)), fmt_n(med([r["vpd"] for r in g if r.get("vpd") is not None])))]
        c = S["cadence"].get(fmt)
        if c:
            L += ["Cadence: %d uploads in 30 days, %d in 90, %d in 365. Median gap %s days, longest gap %s days, %d days since last upload." % (
                c["last30"], c["last90"], c["last365"], fmt_n(c["median_gap_days"]), fmt_n(c["max_gap_days"]), c["days_since_last"])]
            L += ["Sample covers %d days (%d videos). Counts for 90 and 365 days stop at the sample edge.%s" % (
                c["span_days"], c["n_in_sample"], " Raise --%s to cover at least 180 days." % ("long" if fmt == "long" else "shorts") if c["span_days"] < 180 else "")]
            if c["days_since_last"] > 180:
                L += ["WARNING: no upload in 180 days or more."]
        if not S["baseline"].get(fmt):
            L += ["Not enough matured videos (need 5 or more older than %d days) to score outliers. Read the raw views in videos.csv." % S["min_age"]]
        L += ["", "Top by score:", "", "| score | views | age d | min | band | title |", "|---|---|---|---|---|---|"]
        for r in sorted([x for x in g if x.get("score") is not None], key=lambda x: -x["score"])[:8]:
            L.append("| %s%s | %s | %s | %.1f | %s | %s |" % (r["score"], "*" if r["young"] else "", fmt_n(r["views"]), r["age"],
                                                          (r["duration"] or 0) / 60, r["band"], r["title"][:70].replace("|", "/")))
        L += ["", "Length mix:", "", "| bucket | n | median views | median score |", "|---|---|---|---|"]
        for b in S["length"][fmt]:
            L.append("| %s | %d | %s | %s |" % (b["bucket"], b["n"], fmt_n(b["median_views"]), fmt_n(b["median_score"])))
        L += ["", "Title features (score with vs without, needs 3+ each):", "",
              "| feature | n with | median with | median without | share of outliers | share of all |", "|---|---|---|---|---|---|"]
        for f in S["features"][fmt]:
            if f["n_with"]:
                L.append("| %s | %d | %s | %s | %s | %s |" % (f["feature"], f["n_with"], fmt_n(f["median_score_with"]),
                                                          fmt_n(f["median_score_without"]), fmt_n(f["share_of_outliers"]), fmt_n(f["share_of_all"])))
        L.append("")
    L += ["## Traffic lane (guess from titles only)", "",
          "Search-style titles: %(search)d. Browse-style: %(browse)d. Mixed: %(mixed)d. Unclear: %(unclear)d." % S["lanes"],
          "Share of long-form views from videos older than 90 days: %s (a weak proxy: search videos keep earning; needs a sample of 180 days or more)." % fmt_n(S["old_view_share"]),
          "Check the real split in YouTube Studio (Reach tab) for your own channels. For other channels this stays a guess.", ""]
    if S.get("revenue"):
        rv = S["revenue"]
        L += ["## Revenue band (rough, long-form)", ""]
        if "error" in rv:
            L += [rv["error"], ""]
        else:
            L += ["Niche: %s. RPM low / median / high (USD per 1,000 views): %s." % (rv["niche"], rv["rpm_low_median_high"]),
                  "Per typical long video: %s USD." % rv.get("per_typical_long_video_usd"),
                  "Per typical Short: %s USD." % rv.get("per_typical_short_usd"),
                  "Source: %s" % rv["source"], "Caveat: %s" % rv["caveat"], ""]
    if S.get("sheet"):
        L += ["Thumbnail sheet (TOP and LOW by score): %s" % S["sheet"], ""]
    L += ["Next: read the sheet, then fill the pattern, lane and idea steps in the skill. This script finds numbers. It does not judge ideas."]
    txt = "\n".join(L)
    open(os.path.join(outdir, "report.md"), "w").write(txt)
    return txt


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("channel")
    ap.add_argument("--long", type=int, default=60)
    ap.add_argument("--shorts", type=int, default=60)
    ap.add_argument("--min-age", type=int, default=14)
    ap.add_argument("--niche")
    ap.add_argument("--out")
    ap.add_argument("--thumbs", type=int, default=6)
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()
    if not shutil.which("yt-dlp"):
        die("yt-dlp not found. Install it with: pip install -U yt-dlp")
    url = channel_url(a.channel)
    top, longs = collect(url, "videos", a.long, a.workers)
    _, shorts = collect(url, "shorts", a.shorts, a.workers)
    if not longs and not shorts:
        die("no videos found for %s. Check the handle, or YouTube may be blocking this machine." % url)
    rows = longs + shorts
    name = (top or {}).get("channel") or a.channel
    handle = re.sub(r"[^A-Za-z0-9_-]", "", (top or {}).get("uploader_id") or a.channel)
    outdir = a.out or os.path.join("channel-scan", "%s-%s" % (handle, TODAY))
    os.makedirs(outdir, exist_ok=True)
    add_scores(rows, a.min_age)
    for r in rows:
        r["feats"] = title_feats(r["title"])
        r["lane"] = lane(r["title"])
    longv = [r for r in rows if r["format"] == "long" and r.get("views") is not None and r.get("age") is not None]
    tot = sum(r["views"] for r in longv)
    old = sum(r["views"] for r in longv if r["age"] > 90)
    S = {"channel": name, "url": url, "subscribers": (top or {}).get("channel_follower_count"),
         "min_age": a.min_age, "scanned": str(TODAY),
         "n_long": len(longs) - sum(1 for r in longs if r["format"] == "live"), "n_short": len(shorts),
         "n_live": sum(1 for r in rows if r["format"] == "live"),
         "baseline": {f: next((r["base"] for r in rows if r["format"] == f and r.get("base")), None) for f in ("long", "short")},
         "cadence": {f: cadence(rows, f) for f in ("long", "short")},
         "length": {f: length_buckets(rows, f) for f in ("long", "short")},
         "features": {f: feature_table(rows, f) for f in ("long", "short")},
         "lanes": {k: sum(1 for r in rows if r["format"] in ("long", "short") and r["lane"] == k)
                   for k in ("search", "browse", "mixed", "unclear")},
         "old_view_share": round(old / tot, 2) if tot and (S_span(longv) >= 180) else None}
    S["revenue"] = revenue(rows, a.niche)
    S["sheet"] = sheet(rows, outdir, a.thumbs) if a.thumbs else None
    with open(os.path.join(outdir, "videos.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "format", "date", "age_days", "duration_s", "views", "views_per_day", "score", "score_roll",
                    "band", "young", "lane", "likes", "comments", "title"])
        for r in sorted(rows, key=lambda r: r["date"] or dt.date.min, reverse=True):
            w.writerow([r["id"], r["format"], r["date"], r.get("age"), r["duration"], r["views"],
                        round(r["vpd"], 1) if r.get("vpd") is not None else "", r.get("score"), r.get("score_roll"),
                        r.get("band"), r.get("young"), r["lane"], r["likes"], r["comments"], r["title"]])
    json.dump(S, open(os.path.join(outdir, "summary.json"), "w"), indent=1, default=str)
    print(write_report(S, rows, outdir))
    print("\nFiles: %s" % outdir)


if __name__ == "__main__":
    main()
