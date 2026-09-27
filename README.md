# LGBTQIA+ Europe

Queer events across Europe — Pride marches and festivals, film, nightlife, performance,
literature and community — gathered by a daily routine and published as a single static page.

Live site: https://robtheriver72.github.io/lgbtqia-europe/

Sibling project to [Bora y'all!](https://robtheriver72.github.io/borasetubal/), and it
reuses that project's page and build machinery deliberately: `template.html` came from
there already accessibility-audited, so that repo's STYLE.md still describes the layout
and type decisions baked into this page. The colour is this project's own — see
`STYLE.md` here. In short: black and white, with ROYGBIV as the accent, light mode only.

## The one rule that makes this project different

**Every row must say why it is listed, in the words of its source.**

That is the `Why listed` column, and it ships on the card as "Listed because …". It exists
because the inclusion bar here is deliberately broad, and a broad bar without attribution
does harm: calling an event, a venue or a performer queer when the organisers have not is
how you out people. Across Europe that is not abstract — in Hungary, Poland, Turkey and
elsewhere it can expose organisers and attendees to legal and physical risk.

So the site never asserts queerness on its own authority. It reports what the organiser,
the venue or the listing said, and links to it. Acceptable values look like:

- `Organised by [named LGBTQIA+ group]`
- `Billed by its organisers as a queer night`
- `Part of [named Pride / queer festival] programme`
- `Programmed as part of the venue's LGBTQIA+ season`

Not acceptable: `Has a queer audience`, `The performer is gay`, `Feels queer-adjacent`.
`dedupe.py` fails loudly on any row with an empty `Why listed`, and the CI workflow runs
`dedupe.py` before it will build, so such a row cannot reach the site.

## Safety

`cities.csv` carries two separate columns, for two separate audiences:

- **`Reader caveat`** — written for readers, and the only one that ships. It appears on
  every card in that city, as a note with a mustard rule beside it.
- **`Crawl safety rule`** — an instruction to the daily routine about what it may and may
  not publish for that city. **This must never reach the page.** `build.py` ships only the
  reader caveat; keep it that way.

Where organisers deliberately withhold a route or a meeting point, this site withholds it
too. Never reconstruct a location from a previous year's edition.

## How it works

- `events.csv` is the data. This repo is the source of truth.
- `cities.csv` is the crawl's backbone — 93 cities in 34 countries, each with coordinates,
  a tier for the rotation, its own known sources, when it was last swept, and notes.
- `template.html` is the page, with a `__SNAPSHOT__` placeholder. `index.html` is generated —
  never hand-edit it.
- `build.py` bakes the CSVs into the template. Events that have already finished are dropped
  at build time, so a freshly built page never ships a past event.
- `dedupe.py` flags same-date same-city near-duplicate titles, rows with no `Why listed`,
  and rows whose city is missing from `cities.csv`.
- `.github/workflows/rebuild.yml` rebuilds on every data change and again daily at 06:25 UTC.

### events.csv columns

`Start date,End date,Event,Type,Category,City,Country,Venue,Free / Paid,Price,Currency,Description,Why listed,Frequency,Source,Added on,Image`

- Dates ISO `YYYY-MM-DD`; single-day events repeat the date in both columns.
- **City** must match a `City` in `cities.csv`, or the page has no coordinates for it and
  the distance filter silently drops the row. Add the city to `cities.csv` first.
- **Currency** is an ISO code (`EUR`, `GBP`, `CZK`, `PLN`, `SEK`…). A continent means many
  currencies — the page reads the symbol off this column, so never assume euros.
- **Venue** is the proper noun. City-wide events — marches above all — may use
  `<City> city centre`; the page strips the repeated city so the card reads
  "Budapest, Hungary · city centre". This is the one sanctioned exception to the
  proper-noun rule, and it exists because a parade route genuinely has no single room.
- **Category** is one of: Pride march, Pride festival, Club night, Local concert,
  Major concert, Drag, Ballroom, Theatre & performance, Film, Art exhibit,
  Literature & talks, Festival, Community & support, Market, Food & drink, Sport,
  Workshop, Unique experience, Other. A bare "Pride" is folded into Pride festival —
  say which you mean.

## Retiring events

Never delete finished events; `build.py` drops anything already over at build time. Delete
a row only when it is wrong, a duplicate, or re-verification found it cancelled.

## Publishing

1. `python3 dedupe.py` and fix anything it flags.
2. `python3 build.py` to regenerate `index.html`.
3. Commit and push to `main`.
