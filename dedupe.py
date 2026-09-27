#!/usr/bin/env python3
"""Catch same-event-two-spellings pairs that a normalised-title match misses.

Two rows on the same date in the same CITY whose titles share most of their
meaningful words are almost certainly one event listed twice. Printed row
numbers are 0-based indices into the DATA rows: row12 is rows[12].

Also flags the two failures specific to this project: a row with no
'Why listed' value, and a row whose city is missing from cities.csv.
"""
import csv, re, unicodedata, os
from itertools import combinations

BASE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(BASE, "events.csv")

STOP = {"de","da","do","das","dos","e","a","o","as","os","em","no","na","the","of","and",
        "march","marcha","pride","orgulho","festival","festa","parade","csd","concerto",
        "concert","com","para","um","uma","por","ao","aos","2026","2027","queer","lgbt",
        "lgbtqia","fiertes","fierte"}

def toks(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii","ignore").decode().lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return {w for w in s.split() if len(w) > 2 and w not in STOP}

rows = list(csv.DictReader(open(PATH, encoding="utf-8")))
cities = {c["City"] for c in csv.DictReader(open(os.path.join(BASE,"cities.csv"), encoding="utf-8"))}

by = {}
for i, r in enumerate(rows):
    by.setdefault((r["Start date"], r["City"]), []).append((i, r))

sus = []
for key, group in by.items():
    for (i, a), (j, b) in combinations(group, 2):
        ta, tb = toks(a["Event"]), toks(b["Event"])
        if not ta or not tb: continue
        ov = len(ta & tb) / min(len(ta), len(tb))
        if ov >= 0.6: sus.append((ov, i, j, a, b))

sus.sort(reverse=True, key=lambda x: x[0])
print(f"{len(sus)} suspected duplicate pair(s)\n")
for ov, i, j, a, b in sus:
    print(f"  [{ov:.0%}] {a['Start date']} {a['City']}")
    print(f"        A row{i}: {a['Event'][:60]!r}  @ {a['Venue'][:34]!r}  ({a['Added on']})")
    print(f"        B row{j}: {b['Event'][:60]!r}  @ {b['Venue'][:34]!r}  ({b['Added on']})")

nowhy = [(i, r) for i, r in enumerate(rows) if not r["Why listed"].strip()]
print(f"\n{len(nowhy)} row(s) with no 'Why listed' — these MUST NOT ship:")
for i, r in nowhy: print(f"  row{i}: {r['Event'][:70]!r} ({r['City']})")

nocity = [(i, r) for i, r in enumerate(rows) if r["City"].strip() and r["City"] not in cities]
print(f"\n{len(nocity)} row(s) whose city is not in cities.csv (no coordinates, so no distance):")
for i, r in nocity: print(f"  row{i}: {r['City']!r} — {r['Event'][:56]!r}")
