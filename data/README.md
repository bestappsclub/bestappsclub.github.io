# data/

## cn-holidays.json, sg-holidays.json
Public holidays for 万年历吉日, one file per region the user picks in Settings (节假日地区): `cn` = mainland China
(放假 and 调休上班), `sg` = Singapore. The app reads the region in use at most once a day.
The app keeps built-in data as a fallback, so this file only needs to change when a schedule is published.

Where the dates come from:
- China: each November the State Council publishes the next year's schedule (国务院办公厅关于XXXX年部分节假日安排的通知).
- Singapore: around June MOM publishes the next year (press release "Public Holidays for XXXX", mom.gov.sg).
  A holiday on a Sunday gives the Monday off: add that Monday as `"XX补假"`. Singapore has no make-up workdays.

To add a year:
1. Add the year to `years`, and its document to `sources`.
2. Add every date to `days`: `"YYYY-MM-DD": {"name": "春节", "type": "holiday"}` for a day off, or
   `{"name": "春节调休", "type": "workday"}` for a make-up workday.
3. Check JSON is valid (`python3 -m json.tool data/cn-holidays.json`), commit and push.

A year listed in `years` replaces the app's built-in data for that year, so corrections work too.
Keep `version` at 1 unless the format changes (the app ignores versions it doesn't know).

## Automatic check (GitHub Action)
`.github/workflows/update-holidays.yml` runs `data/scripts/update_holidays.py` on the 1st of every month
(or by hand: Actions › Update holiday data › Run workflow). It reads
[NateScarlet/holiday-cn](https://github.com/NateScarlet/holiday-cn) for mainland China and data.gov.sg
collection 691 (MOM) for Singapore, for this year and next.

When something is new or different it pushes the `holiday-update` branch and opens a pull request
(or, if Actions can't open PRs in this repo, an issue with a compare link). Review the dates in it,
then merge: the site updates in about a minute and the app picks it up within a day.
Nothing is published without that merge.
