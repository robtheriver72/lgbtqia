#!/usr/bin/env python3
"""Build index.html for LGBTQIA+ Europe from events.csv + template.html.
Usage: python3 build.py [snapshot-date]  (defaults to today, Europe/Lisbon)

Distances are computed in the page from the city coordinates in TOWNS, from
whatever city the reader picks — there is no fixed origin, because a
continent-wide site has no single sensible one."""
import csv, json, sys, datetime, zoneinfo, pathlib
root = pathlib.Path(__file__).parent
date = sys.argv[1] if len(sys.argv) > 1 else datetime.datetime.now(zoneinfo.ZoneInfo("Europe/Lisbon")).date().isoformat()
rows = list(csv.DictReader(open(root/'events.csv', encoding='utf-8')))
ev = [dict(start=r['Start date'], end=r['End date'] or r['Start date'], name=r['Event'], type=r['Type'],
           cat=r['Category'] or 'Other', city=r['City'], town=r['City'], country=r['Country'], venue=r['Venue'],
           fp=r['Free / Paid'] or 'Unknown', price=r['Price'], cur=r['Currency'] or 'EUR',
           desc=r['Description'], why=r['Why listed'], freq=r['Frequency'], src=r['Source'],
           img=r.get('Image','')) for r in rows]
ev = [e for e in ev if e['end'] >= date]  # never ship past events
cities = list(csv.DictReader(open(root/'cities.csv', encoding='utf-8')))
# Two different audiences, so two different columns. 'Reader caveat' is written FOR
# readers and is the only one that ships. 'Crawl safety rule' is an instruction to the
# daily routine (what it may and may not publish) and must never reach the page.
safety = {c['City']: c['Reader caveat'] for c in cities if c['Reader caveat'].strip()}
snap = json.dumps({'date': date, 'events': ev, 'safety': safety}, ensure_ascii=False).replace('</', '<\\/')
body = open(root/'template.html', encoding='utf-8').read().replace('__SNAPSHOT__', snap)
i = body.index('</style>') + len('</style>')
doc = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
       + body[:i] + '</head><body>' + body[i:] + '</body></html>')
(root/'index.html').write_text(doc, encoding='utf-8')
missing = sorted({e['city'] for e in ev} - {c['City'] for c in cities})
print(f'index.html built: {len(ev)} live events of {len(rows)}, snapshot {date}')
if missing: print(f'WARNING: cities not in cities.csv (no coordinates, so no distance): {missing}')
