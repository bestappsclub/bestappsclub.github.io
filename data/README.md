# data/

## cn-holidays.json
China's public holidays (放假) and make-up workdays (调休上班), read by 万年历吉日 at most once a day.
The app keeps built-in data as a fallback, so this file only needs to change when a schedule is published.

Each November the State Council publishes the next year's schedule (国务院办公厅关于XXXX年部分节假日安排的通知).
To add it:
1. Add the year to `years`, and its document to `sources`.
2. Add every date to `days`: `"YYYY-MM-DD": {"name": "春节", "type": "holiday"}` for a day off, or
   `{"name": "春节调休", "type": "workday"}` for a make-up workday.
3. Check JSON is valid (`python3 -m json.tool data/cn-holidays.json`), commit and push.

A year listed in `years` replaces the app's built-in data for that year, so corrections work too.
Keep `version` at 1 unless the format changes (the app ignores versions it doesn't know).
