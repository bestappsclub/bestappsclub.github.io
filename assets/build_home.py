"""Builds index.html from assets/apps.json (Apple's public lookup for developer 1632188995).
Refresh the list: curl 'https://itunes.apple.com/lookup?id=1632188995&entity=software&limit=200&country=us' and rerun."""
import json, html, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
apps = json.loads((root / "assets/apps.json").read_text())
featured = {6759566214: "/videoflow/"}  # apps with their own page here
# Only apps the owner chose to show (App Store IDs from assets/apps.json). Add IDs here to list more.
shown = []
cards = []
for a in apps:
    if a["id"] not in shown or a["id"] in featured:
        continue
    cards.append(f'''<a class="app" href="{a['url']}"><img src="{a['icon']}" alt="" loading="lazy" width="64" height="64"><span><b>{html.escape(a['name'])}</b><small>{html.escape(a['genre'] or '')}</small></span></a>''')
page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Best Apps Club – Simple, useful apps for iPhone</title>
<meta name="description" content="Best Apps Club makes small, focused apps for iPhone and iPad, including Video Flow.">
<link rel="icon" href="/videoflow/img/icon.png">
<style>
:root{{--bg:#fbfaff;--surface:#fff;--text:#15132b;--muted:#625f7a;--line:#e6e3f5;--brand:#6052fc;--shadow:0 18px 50px rgba(48,36,160,.12)}}
@media (prefers-color-scheme:dark){{:root{{--bg:#0e0d1a;--surface:#191729;--text:#f2f1fb;--muted:#a3a0bd;--line:#2a2742;--brand:#8a7cff;--shadow:0 18px 50px rgba(0,0,0,.45)}}}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text","Segoe UI",Roboto,sans-serif;line-height:1.55;-webkit-font-smoothing:antialiased}}
a{{color:inherit;text-decoration:none}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 20px}}
header{{padding:72px 0 40px}}
h1{{font-size:clamp(34px,5vw,52px);letter-spacing:-.03em;line-height:1.08}}
.lead{{color:var(--muted);font-size:19px;margin-top:12px;max-width:32em}}
.feature{{display:grid;grid-template-columns:auto 1fr auto;gap:24px;align-items:center;background:var(--surface);border:1px solid var(--line);border-radius:24px;padding:26px;box-shadow:var(--shadow);margin-bottom:56px}}
.feature img{{width:96px;height:96px;border-radius:22px}}
.feature small{{color:var(--brand);font-weight:700;font-size:13px;letter-spacing:.06em;text-transform:uppercase}}
.feature h2{{font-size:26px;letter-spacing:-.02em;margin:4px 0}}
.feature p{{color:var(--muted)}}
.btn{{background:var(--brand);color:#fff;font-weight:700;border-radius:999px;padding:12px 22px;white-space:nowrap}}
h3{{font-size:22px;margin-bottom:18px}}
.apps{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px}}
.app{{display:flex;gap:14px;align-items:center;background:var(--surface);border:1px solid var(--line);border-radius:18px;padding:14px}}
.app:hover,.feature:hover{{border-color:var(--brand)}}
.app img{{width:56px;height:56px;border-radius:13px;flex:none}}
.app b{{display:block;font-size:15px;line-height:1.3}}
.app small{{color:var(--muted);font-size:13px}}
footer{{border-top:1px solid var(--line);margin-top:64px;padding:28px 0 48px;color:var(--muted);font-size:14px;display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px}}
footer a{{color:var(--brand)}}
@media (max-width:640px){{.feature{{grid-template-columns:auto 1fr}}.feature .btn{{grid-column:1/-1;text-align:center}}.feature img{{width:72px;height:72px}}header{{padding-top:44px}}}}
</style>
</head>
<body>
<div class="wrap">
<header>
  <h1>Best Apps Club</h1>
  <p class="lead">Small, focused apps for iPhone and iPad. Each one does a single job well, with no clutter.</p>
</header>
<a class="feature" href="/videoflow/">
  <img src="/videoflow/img/icon.png" alt="Video Flow icon">
  <span><small>Featured</small><h2>Video Flow – Player &amp; Browser</h2><p>Watch video on the web, without the clutter. Tabs with previews, a one-tap quick menu, background audio and on-device AI summaries.</p></span>
  <span class="btn">Learn more</span>
</a>
{('<h3>More apps</h3>' + chr(10) + '<div class="apps">' + chr(10).join(cards) + '</div>') if cards else ''}
<footer><span>© 2026 Best Apps Club</span><span>Questions? <a href="mailto:bestappsclub@gmail.com">bestappsclub@gmail.com</a></span></footer>
</div>
</body>
</html>
'''
(root / "index.html").write_text(page)
print("apps listed:", len(cards) + len(featured))
