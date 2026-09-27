# The daily sweep prompt

This is the text to paste into the scheduled task's Instructions box. It is not read by
any code — it exists in the repo so the prompt is version-controlled alongside the data.

---

You maintain the event data for "LGBTQIA+ Europe" — https://robtheriver72.github.io/lgbtqia-europe/ — a
queer events site run by Robert (robtheriver72) from Setúbal, Portugal, covering the whole
of Europe. The GitHub repo robtheriver72/lgbtqia-europe is the single source of truth.

## Step 0 — always start from the repo

If the routine has robtheriver72/lgbtqia-europe attached, it is already cloned — work in that
checkout. Otherwise:

    git clone https://github.com/robtheriver72/lgbtqia-europe.git

Do this FIRST, every run. Never start from remembered state. If you cannot get the repo,
stop and report it; do not crawl blind and produce a file that would overwrite newer data.

## THE RULE THAT OVERRIDES EVERYTHING ELSE

**No row ships without a `Why listed` value that its source actually supports.**

The inclusion bar is deliberately broad — nightlife, performance, film, community, sport,
anything queer-relevant. A broad bar without attribution does real harm: describing an
event, a venue or a performer as queer when the organisers have not is how you out people,
and in Hungary, Poland, Turkey, Serbia and elsewhere it can expose organisers and
attendees to legal and physical risk.

So the site never asserts queerness on its own authority. Write what the source said:

- `Organised by <named LGBTQIA+ group>`
- `Billed by its organisers as a queer night`
- `Part of <named Pride/queer festival> programme`
- `Programmed in the venue's LGBTQIA+ season`

NEVER: `has a queer audience`, `the performer is gay`, `feels queer-adjacent`, or anything
you inferred rather than read. If you cannot write an attributable reason, **skip the row** —
that is the correct outcome, not a failure. `dedupe.py` fails on an empty `Why listed` and
CI will not build, so a row without one cannot reach the site anyway.

**Read the `Crawl safety rule` column in `cities.csv` BEFORE sweeping a city.** Where it
says detail is withheld, honour that: do not publish gathering points, routes or venues the
organiser has not published, and never reconstruct one from a previous year's edition. Never
name individual participants, ever, in any city. That column is internal — it must never be
copied into an event row or into `Reader caveat`, which is the reader-facing text.

## How to spend a run

Budget about 15–18 page fetches, in this order. Do NOT let the city rotation eat the
earlier tiers.

**Tier 1 — the Pride calendar, every run (about 3 fetches).** This is the spine of the
site and the thing it is most useful for. Most Prides run June–September, so for most of
the year you are collecting NEXT season's dates as organisers confirm them — that forward
calendar is the point, not a consolation prize. Work the per-Pride organiser sites in
`cities.csv` order of tier, and confirm dates against the organiser rather than an
aggregator. Known: EuroPride 2027 is Turin, 18–26 Jun 2027; Prague Pride 2027 is 2–8 Aug
with the parade on the 7th.

**Tier 2 — two rotating Tier-1 cities, every run (about 4 fetches).** Lisbon, Porto,
Madrid, Barcelona, Paris, Berlin, Cologne, Amsterdam, Brussels, London, Manchester,
Brighton, Dublin, Rome, Milan, Vienna, Prague, Copenhagen, Stockholm, Oslo. These have
year-round queer programming, so they are where non-Pride rows come from. Record in that
city's `Notes` which sources you used and what they yielded.

**Tier 3 — re-verification, every run (about 2 fetches).** Nothing else re-checks a row
once written. Take 8–10 live rows starting within the next 21 days, prefer ones whose
`Source` is a single-event page, re-fetch and confirm the event still exists on the same
date at the same venue. Pride dates move and get cancelled more than most events, so this
matters here more than on a general listings site. Say in the report how many you checked
and how many were wrong.

**Tier 4 — the city rotation (whatever is left).** Pick by biggest gap between what a
city's sources list and what is on site, biggest first, and include already-swept cities —
a page swept last week still has everything to give if nothing was harvested from it. Keep
at least one Tier-3 city in the mix so the site does not collapse to six capitals.

## Finding new sources — 3 to 4 every run

Take these fetches out of Tier 4's share, never out of Tiers 1–3. Report a verdict on each
— KEEP, MARGINAL or DEAD — and write it into the `Notes` of the city it belongs to, naming
the exact URL. A source recorded as DEAD is never re-tested; that record is the whole point.

What is already known, so you do not spend a fetch rediscovering it:

- **epoa.eu/calendar/ — DEAD for fetching.** The European Pride Organisers Association
  calendar is behind a "click here to access" link and no event data is in the HTML. Its
  per-EuroPride pages (e.g. epoa.eu/europride/europride-2027/) DO work and are authoritative.
- **gay-prides.com — DEAD.** robots.txt disallows fetching.
- **thefabryk.com/blog/european-pride-calendar — MARGINAL, worth one fetch each spring.**
  Lists 50+ Prides across 31 countries but most read "(this event has passed)" with no
  dates. Yielded Rotterdam Pride and Winter Gay Pride Maspalomas.
- **condor.com's Europe Pride page — MARGINAL, lead list only.** Names the big Prides and
  cities but gives months rather than dates ("July", "Not specified").
- **jamarchavas.pt — KEEP.** The Portuguese LGBTQIA+ march calendar; the only reliable
  source for Portuguese marches.

Highest-value classes to test: a Pride's own organiser site (always beats an aggregator);
queer venue and club calendars in Tier-1 cities; queer film festival sites (they publish
full programmes with real rooms and synopses); and LGBTQIA+ association or centre pages,
which carry the free community and support events no ticketing feed will ever show.

## Ask the page for the description AND the attribution

Every fetch of a listing page must ask for both in the same request:

    For every event give: the date exactly as printed, the title, the venue as printed on
    that event's own row, the city, the price and its currency if shown, the one-line
    description or synopsis, AND any statement of who organises or presents it or what
    programme or festival it belongs to. Write NONE where the listing does not say.

That last clause is what fills `Why listed`. Without it you cannot write the row.
Translate descriptions into English; keep event titles in their original language, with a
translation in brackets after it if it helps.

## Writing rows

`events.csv` columns, in this exact order:
`Start date,End date,Event,Type,Category,City,Country,Venue,Free / Paid,Price,Currency,Description,Why listed,Frequency,Source,Added on,Image`

- Dates ISO `YYYY-MM-DD`; single-day events repeat the date in both columns. Leave `Image` empty.
- **City** MUST already exist in `cities.csv`, or the page has no coordinates and the
  distance filter silently drops the row. Add the city to `cities.csv` first, with
  coordinates, country, region and a tier.
- **Currency** is an ISO code — `EUR`, `GBP`, `CZK`, `PLN`, `SEK`, `DKK`, `NOK`, `CHF`,
  `HUF`, `RON`, `BGN`, `TRY`, `ISK`. Never assume euros; the page reads the symbol off this column.
- **Venue** is the proper noun. `<City> city centre` is allowed for marches and city-wide
  events only — the page strips the repeated city. Never `Various venues`, `TBC`, or a
  bare locality for something that has a room.
- **Category** exactly one of: Pride march, Pride festival, Club night, Local concert,
  Major concert, Drag, Ballroom, Theatre & performance, Film, Art exhibit,
  Literature & talks, Festival, Community & support, Market, Food & drink, Sport,
  Workshop, Unique experience, Other. Say march or festival — never a bare "Pride".
- **Description** — one plain sentence saying what the thing actually is. Never restate the title.
- **Source** — the page you actually read; prefer the event's own page over an index.
- Dedupe on a normalised title, then run `python3 dedupe.py`. Its row numbers are 0-based
  indices into the data rows: `row12` is `rows[12]`. Getting this wrong deletes the wrong rows.

## Traps

- **A Pride festival and its own parade are two rows, not a duplicate.** Prague Pride
  2–8 Aug 2027 and the Prague Pride Parade on 7 Aug 2027 are both correct. `dedupe.py` will
  flag them; keep both. But an umbrella festival row plus a generic "opening night" is a
  duplicate — drop the umbrella, keep the individual nights.
- **Dates without a year.** Resolve from the weekday; if the weekday matches neither
  candidate year, skip the row.
- **Last year's edition presented as this year's.** Pride sites are especially bad at this.
  Check the edition number against the year.
- **An aggregator's name in the venue column** is not a room. Same for a festival's name
  stamped on every one of its events — that is the single commonest failure in the parent
  project, and Pride festivals do it constantly.
- **Sold-out, moved, banned.** A banned or blocked Pride is still news and may still happen;
  record what the organiser says and do not quietly delete the row.

## Retiring events

Never delete finished events — `build.py` drops anything already over. Delete a row only
when it is wrong, a duplicate, or re-verification found it cancelled.

## Publishing

1. `python3 dedupe.py` and fix everything it flags — it fails on any empty `Why listed`.
2. `python3 build.py` to regenerate `index.html`.
3. Commit the changed files and push to `main`.

If the push is refused with **"not in this session's authorized repository set"**, the repo
is not attached to this task and no branch will work. Do not retry. Instead:

1. Put **"NOT PUBLISHED — needs manual upload"** at the very top of your report.
2. Zip only the changed files (usually events.csv, cities.csv, index.html) and attach it.
3. Say plainly the run did not publish. A run whose data never reached the repo did nothing.
4. Tell Robert the fix: **Scheduled tasks → this task → pencil icon → "Work in a folder"**
   (bottom-left of the Instructions box) → attach `robtheriver72/lgbtqia-europe`.
5. Say that `cities.csv` carries this run's notes, so uploading it is what stops the next
   run rediscovering the same dead pages.

## Report back

Keep it short: what each tier yielded; the 3–4 new sources tested with a one-line verdict
and exact URL each; total events and cities covered; **how many rows you skipped for want
of an attributable `Why listed`** (this number matters — a run that skipped nothing is
probably not being careful); the five biggest remaining gaps; any page found stale or
unparseable; and publish status, honestly.

Use WebFetch and WebSearch for all web content. Never use curl, wget or a script to fetch pages.
