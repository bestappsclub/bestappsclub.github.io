#!/usr/bin/env python3
"""Builds the GoSG Bus site (bestappsclub.github.io/gosgbus/). Run: python3 gosgbus/build.py

Pages are plain HTML strings below; edit the text here, not the generated files.
Facts about other apps must come from their own store page or site, with the date checked.
"""
import json, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://bestappsclub.github.io/gosgbus/"
STORE = "https://apps.apple.com/sg/app/id6758246086"
PRIVACY = "https://bestappsclub.github.io/application/gosgbus/privacy.html"
TERMS = "https://bestappsclub.github.io/application/gosgbus/terms.html"
SUPPORT = "https://bestappsclub.github.io/application/gosgbus/support.html"
EMAIL = "bestappsclub@gmail.com"
UPDATED = "2026-11-21"

APPLE = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.37 12.6c-.02-2.2 1.8-3.26 1.88-3.31-1.03-1.5-2.62-1.7-3.18-1.73-1.35-.14-2.65.8-3.33.8-.69 0-1.75-.78-2.88-.76-1.48.02-2.85.86-3.61 2.19-1.54 2.67-.39 6.62 1.11 8.79.73 1.06 1.6 2.25 2.75 2.2 1.1-.04 1.52-.71 2.85-.71 1.33 0 1.7.71 2.87.69 1.19-.02 1.94-1.08 2.66-2.14.84-1.23 1.18-2.42 1.2-2.48-.03-.01-2.3-.88-2.32-3.54zM14.2 6.1c.6-.73 1.01-1.75.9-2.76-.87.04-1.92.58-2.54 1.31-.56.65-1.05 1.69-.92 2.68.97.08 1.96-.49 2.56-1.23z"/></svg>')


def badge(ct):
    return (f'<a class="badge" href="{STORE}?ct={ct}&amp;pt=127920570" aria-label="Download GoSG Bus on the App Store">'
            f'{APPLE}<span><small>Download on the</small><b>App Store</b></span></a>')


GUIDES = [
    ("best-sg-bus-app", "Best Singapore bus app for iPhone? What to check",
     "Five checks to run on your own commute before you pick a bus app.", "Buying guide"),
    ("gosg-vs-bussing", "GoSG Bus vs BusSing: which Singapore bus app fits you?",
     "An honest side-by-side, including where BusSing is ahead.", "App comparison"),
    ("bus-widget-iphone", "How to put Singapore bus times on your iPhone Home Screen",
     "Add the GoSG widget, pick a stop, and track a bus on the Lock Screen.", "iPhone tips"),
    ("causeway-traffic-cameras", "Check Woodlands and Tuas Causeway traffic before you go",
     "Live checkpoint camera photos, right next to your bus times.", "Travel tips"),
    ("last-bus-singapore", "How to check the last bus in Singapore",
     "Find first and last bus times for any service at your stop.", "Bus basics"),
    ("how-to-use-gosg", "How to use GoSG Bus, in short videos",
     "Arrivals, widgets, leave-now alerts, Ask, Causeway cameras, MRT and traffic, each in a few seconds.", "How-to"),
]

# Screen recordings from the iOS simulator (GoSG 2.1), made by busSgUITests/DemoRecordings.swift.
CLIPS = {
    "arrivals": ("Live arrivals", "Open a nearby stop, then tap a bus to see where it is on the map."),
    "widget-star": ("Pick buses for the widget", "Touch and hold a bus: Show in widget, or Track on Lock Screen."),
    "add-widget": ("Add the Home Screen widget", "Touch and hold the Home Screen, tap Edit › Add Widget, search GoSG Bus."),
    "leave-now": ("Leave-now alerts", "Favourites › turn on alerts. GoSG tells you when to walk out the door."),
    "ask": ("Just ask", "Type a question like “How do I get to VivoCity?” and get buses, changes and time."),
    "cameras": ("Causeway cameras", "Search shows Woodlands and Tuas checkpoint photos. Swipe for the next one."),
    "mrt": ("MRT stations", "The MRT tab has every station and exit, as a map or a list."),
}


def clip(name, up=""):
    t, c = CLIPS[name]
    return (f'<figure class="clip"><video src="{up}vid/{name}.mp4" poster="{up}vid/{name}.jpg" muted loop playsinline preload="none" '
            f'aria-label="{html.escape(t)}: {html.escape(c)}"></video><figcaption><b>{t}</b>{c}</figcaption></figure>')


# Plays a clip only while it is on screen, so the page doesn't download 8 videos at once.
PLAY_IN_VIEW = """<script>(()=>{const v=document.querySelectorAll('video[preload=none]');if(!v.length)return;
const io=new IntersectionObserver(es=>es.forEach(e=>{const x=e.target;if(e.isIntersecting){x.play().catch(()=>{})}else{x.pause()}}),{threshold:.35});
v.forEach(x=>io.observe(x))})()</script>"""


def page(path, title, desc, body, *, h_nav=True, schema=None):
    depth = path.count("/")
    up = "../" * depth
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in (schema or []))
    canonical = BASE + (path[:-10] if path.endswith("index.html") else path)
    compare = "".join(f'<a href="{up}guides/{slug}.html">{html.escape(t.split(":")[0].split("?")[0])}</a>' for slug, t, _, _ in GUIDES)
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="apple-itunes-app" content="app-id=6758246086">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{BASE}img/icon.jpg">
<link rel="icon" href="{up}img/icon.jpg">
<link rel="stylesheet" href="{up}site.css">
{ld}
<script async src="https://www.googletagmanager.com/gtag/js?id=G-153BDPCC9N"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-153BDPCC9N',{{allow_google_signals:false,allow_ad_personalization_signals:false}});</script>
</head>
<body>
<header class="bar"><div class="wrap">
  <a class="logo" href="{up}index.html"><img src="{up}img/icon.jpg" alt=""> GoSG Bus</a>
  <nav><a href="{up}index.html#features">Features</a><a href="{up}guides/index.html">Guides</a><a href="{up}index.html#faq">FAQ</a>
  <a class="get" href="{STORE}?ct=gosgbus-nav&amp;pt=127920570">Get GoSG</a></nav>
</div></header>
{body}
<footer><div class="wrap cols">
  <div><b>GoSG Bus</b><p>Live Singapore bus times, from official LTA DataMall data. Times are estimates and can be briefly unavailable during LTA maintenance.</p></div>
  <div><b>Guides</b>{compare}</div>
  <div><b>Product</b><a href="{up}index.html#features">Features</a><a href="{up}index.html#faq">FAQ</a><a href="{SUPPORT}">Support</a><a href="mailto:{EMAIL}">Contact</a></div>
  <div><b>Legal</b><a href="{PRIVACY}">Privacy policy</a><a href="{TERMS}">Terms of use</a></div>
</div><div class="wrap fine">© 2026 Best Apps Club · Bus data: LTA DataMall · Camera images: data.gov.sg</div></footer>
{PLAY_IN_VIEW if "<video" in body else ""}
</body>
</html>
"""
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(doc)


FAQ = [
    ("Where do the bus times come from?", "From LTA DataMall, the Land Transport Authority's official data, for SBS Transit, SMRT, Tower Transit and Go-Ahead buses."),
    ("How often do times refresh?", "Every few seconds while a stop is open. Times are estimates, so they can jump when a bus speeds up or gets stuck in traffic."),
    ("Does it need internet?", "Yes for live times. Your favourites and the stop list stay on your phone."),
    ("Why did an arrival time change?", "Times are LTA's live estimates. They move when a bus speeds up, gets held at a stop, or hits traffic. Open the bus map to see where the bus actually is."),
    ("Is GoSG free?", "Yes. Live times, Nearby, Favourites, Search, routes, the bus map, cameras and the MRT map are free, with no ads. GoSG Plus is optional and adds more leave-now alerts and AI answers."),
    ("Do I need an account?", "No. Open the app and use it."),
    ("Which devices and languages?", "iPhone and iPad with iOS 17 or later, and Macs with Apple silicon. English, 简体中文, 繁體中文, Bahasa Melayu, தமிழ் and हिन्दी."),
    ("Is there an Apple Watch app?", "Not yet. Widgets, the Lock Screen and Siri cover the quick look for now."),
    ("How do I report a problem?", f"Use Settings › Send feedback in the app, or email {EMAIL}."),
]

# (eyebrow, heading, one sentence, clip, guide slug) — one demo video per feature, like a store preview.
FEATURES = [
    ("Live arrivals", "Your stop. Already open.", "Nearby stops are on the first screen with the next three buses for every service. Tap a bus to see where it is on the map.", "arrivals", "best-sg-bus-app"),
    ("Home Screen widgets <span class=tag>New in 2.1</span>", "Your usual stop. One glance away.", "Put a favourite stop on the Home Screen, or let the widget pick the favourite nearest to you. Tap ↻ for fresh times.", "add-widget", "bus-widget-iphone"),
    ("Lock Screen &amp; Dynamic Island <span class=tag>New in 2.1</span>", "Your bus. Always in view.", "Touch and hold a bus to track it. It counts down on the Lock Screen and in the Dynamic Island while you get ready.", "widget-star", "bus-widget-iphone"),
    ("Leave-now alerts", "Walk out. Right on time.", "Pick your bus and your usual times. GoSG tells you when it's time to leave, so you're not waiting at the stop.", "leave-now", None),
    ("Ask", "Just ask. Get there.", "“How do I get to VivoCity?” “Last 52 tonight?” Get the buses, where to change and the time door to door. Or ask Siri.", "ask", "last-bus-singapore"),
]


def home():
    feats = ""
    for i, (eb, h, d, name, link) in enumerate(FEATURES):
        more = f'<a class="more" href="guides/{link}.html">Read the guide →</a>' if link else ""
        feats += (f'<div class="row{" flip" if i % 2 else ""}"><div><p class="eyebrow">{eb}</p><h3>{h}</h3><p>{d}</p>{more}</div>'
                  f'<video class="demo" src="vid/{name}.mp4" poster="vid/{name}.jpg" muted loop playsinline preload="none" aria-label="{html.escape(CLIPS[name][0])} demo"></video></div>')
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
    cards = "".join(f'<a class="card" href="guides/{s}.html"><small>{c}</small><b>{t}</b><span>{d}</span></a>' for s, t, d, c in GUIDES[:3])
    body = f"""
<section class="hero"><div class="wrap grid2">
  <div>
    <p class="eyebrow">Singapore bus timings &amp; MRT</p>
    <h1>Your next bus,<br><em>at a glance.</em></h1>
    <p class="lead">Live arrival times for every bus stop in Singapore. Know when to leave, see where your bus is, and plan the trip by just asking.</p>
    <div class="cta">{badge("gosgbus-hero")}<span class="note">Free · iPhone &amp; iPad · iOS 17+</span></div>
    <div class="chips"><span>No ads</span><span>No account</span><span>6 languages</span></div>
  </div>
  <div class="phones" aria-hidden="true"><img src="img/1-nearby.jpg" alt=""><img src="img/3-busmap.jpg" alt=""></div>
</div></section>

<section class="ops"><div class="wrap">
  <b>One app. Every bus stop.</b>
  <span>SBS Transit</span><span>SMRT</span><span>Tower Transit</span><span>Go-Ahead</span><em>Official LTA DataMall data</em>
</div></section>

<section id="features"><div class="wrap">
  <p class="eyebrow">A better everyday commute</p><h2>Everything for the bus ride, nothing extra</h2>
  {feats}
</div></section>

<section id="how"><div class="wrap">
  <div class="head"><h2>And on the road</h2><a href="guides/how-to-use-gosg.html">All how-to videos →</a></div>
  <div class="clips">{clip("cameras")}{clip("mrt")}</div>
</div></section>

<section class="more-grid"><div class="wrap narrow">
  <p class="eyebrow">Privacy</p><h2>Your commute is your business.</h2>
  <p class="lead dark">No ads and no account. Your favourites stay on your iPhone, and your location is used on the device to find stops near you. It isn't sent to us.</p>
</div></section>

<section class="more-grid"><div class="wrap">
  <h2>And there's more on board</h2>
  <div class="grid4">
    <div class="f"><i>🔔</i><h3>Get-off alerts <span class=tag>2.1</span></h3><p>Pick your stop on the bus map. GoSG nudges you 2 stops before, and again at the stop before yours.</p></div>
    <div class="f"><i>🚦</i><h3>Causeway cameras</h3><p>Woodlands and Tuas checkpoint photos before you head to JB. <a href="guides/causeway-traffic-cameras.html">How it works</a></p></div>
    <div class="f"><i>🚇</i><h3>MRT map</h3><p>Every station and exit on one map, with directions in Apple Maps.</p></div>
    <div class="f"><i>🗣️</i><h3>Siri</h3><p>"When's my next bus?" "Track my bus." "Any traffic incidents near me?"</p></div>
  </div>
</div></section>

<section><div class="wrap">
  <h2>At a glance</h2>
  <dl class="glance">
    <dt>Free</dt><dd>Live times, Nearby, Favourites, Search, routes, bus map, cameras, MRT map, 1 leave-now alert, 5 AI answers a day. No ads.</dd>
    <dt>GoSG Plus (optional)</dt><dd>Up to 10 leave-now alerts and 50 AI answers a day. Cancel anytime in your Apple Account.</dd>
    <dt>Devices</dt><dd>iPhone and iPad on iOS 17 or later. Macs with Apple silicon via the Mac App Store.</dd>
    <dt>Languages</dt><dd>English, 简体中文, 繁體中文, Bahasa Melayu, தமிழ், हिन्दी</dd>
  </dl>
</div></section>

<section><div class="wrap">
  <div class="head"><h2>Guides</h2><a href="guides/index.html">All guides →</a></div>
  <div class="cards">{cards}</div>
</div></section>

<section id="faq"><div class="wrap narrow">
  <h2>Common questions</h2>{faq}
</div></section>

<section class="final"><div class="wrap">
  <img src="img/icon.jpg" alt="" class="bigicon"><h2>Next stop: never missing your bus.</h2>{badge("gosgbus-bottom")}
</div></section>
"""
    schema = [
        {"@context": "https://schema.org", "@type": "SoftwareApplication", "name": "GoSG Bus",
         "operatingSystem": "iOS 17.0 or later", "applicationCategory": "TravelApplication",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "SGD"}, "url": BASE, "downloadUrl": STORE},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ]
    page("index.html", "GoSG Bus – Singapore bus timings & MRT for iPhone",
         "Live arrival times for every bus stop in Singapore from official LTA data. Leave-now alerts, live bus map, widgets, Causeway cameras and an Ask tab. Free, no ads, 6 languages.",
         body, schema=schema)


def article(slug, title, desc, category, sections, *, disclosure=False):
    toc = "".join(f'<li><a href="#{a}">{h}</a></li>' for a, h, _ in sections)
    secs = "".join(f'<h2 id="{a}">{h}</h2>{c}' for a, h, c in sections)
    others = [g for g in GUIDES if g[0] != slug][:2]
    keep = "".join(f'<a class="card" href="{s}.html"><small>{c}</small><b>{t}</b><span>{d}</span></a>' for s, t, d, c in others)
    disc = '<p class="disclose">We make GoSG Bus. Facts about other apps come from their App Store page and website, checked on 21 Nov 2026.</p>' if disclosure else ""
    body = f"""
<article class="wrap narrow post">
  <p class="crumb"><a href="../index.html">Home</a> / <a href="index.html">Guides</a></p>
  <p class="eyebrow">{category}</p>
  <h1 class="ph1">{title}</h1>
  <p class="lead dark">{desc}</p>
  <p class="meta">GoSG Bus team · Updated 21 Nov 2026</p>
  {disc}
  <nav class="toc"><b>In this guide</b><ol>{toc}</ol></nav>
  {secs}
  <div class="tryit"><b>Try it on your next commute.</b><span>Free on the App Store.</span>{badge("gosgbus-" + slug)}</div>
  <h2>Keep reading</h2><div class="cards">{keep}</div>
</article>
"""
    schema = [{"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc,
               "dateModified": UPDATED, "author": {"@type": "Organization", "name": "Best Apps Club"},
               "mainEntityOfPage": BASE + f"guides/{slug}.html"}]
    page(f"guides/{slug}.html", f"{title} | GoSG Bus", desc, body, schema=schema)


def guides():
    article("best-sg-bus-app", *GUIDES[0][1:3], GUIDES[0][3], [
        ("quick", "The short answer",
         "<p>Every Singapore bus app reads the same LTA DataMall feed, so no app has “more accurate” times than another. What differs is how fast you get to your bus, and what the app does when you're not looking at it. Pick the app that wins the five checks below on <em>your</em> commute.</p>"),
        ("checks", "Five checks on your usual journey", """<ol class="steps">
<li><b>Open to answer.</b> From tapping the icon, how many seconds until you see your bus at your stop? Nearby stops should already be there.</li>
<li><b>Without opening the app.</b> Can you see the time on the Home Screen or Lock Screen? Does it count down by itself?</li>
<li><b>When to leave.</b> Will it tell you when to walk out, for the bus you take on weekdays?</li>
<li><b>When something's wrong.</b> Does it show where the bus actually is, and traffic incidents on the way?</li>
<li><b>Your language.</b> Can your parents or helper use it in their language?</li></ol>"""),
        ("table", "Which app suits which job", """<table><thead><tr><th>Job</th><th>What to look for</th><th>In GoSG</th></tr></thead><tbody>
<tr><td>Daily commute</td><td>Favourites, widget, leave-now alert</td><td>Favourites tab, Home Screen widget (2.1), leave-now alerts</td></tr>
<tr><td>Unfamiliar trip</td><td>Directions with changes</td><td>Ask: “How do I get to VivoCity?”</td></tr>
<tr><td>Late night</td><td>First and last bus</td><td>Settings › Show arrival details, or ask “Last 52 tonight?”</td></tr>
<tr><td>Going to JB</td><td>Checkpoint traffic</td><td>Causeway cameras on Search and on stops near the checkpoints</td></tr>
<tr><td>Family members</td><td>Language</td><td>6 languages, including 中文, Melayu, தமிழ் and हिन्दी</td></tr>
</tbody></table>"""),
        ("free", "What is free in GoSG?",
         "<p>All live times, Nearby, Favourites, Search, routes, the bus map, cameras and the MRT map, with no ads and no account. GoSG Plus is optional: 10 leave-now alerts instead of 1, and 50 AI answers a day instead of 5.</p>"),
        ("compare", "Compare with the app you use now",
         '<p>See <a href="gosg-vs-bussing.html">GoSG Bus vs BusSing</a> for a side-by-side, including where BusSing is ahead.</p>'),
    ])
    article("gosg-vs-bussing", *GUIDES[1][1:3], GUIDES[1][3], [
        ("short", "The short version",
         "<p>Both apps show live LTA bus times for every stop, without ads. <b>BusSing</b> is ahead on Apple Watch and offline MRT routing. <b>GoSG</b> is ahead on languages, plain-language trip planning, leave-now alerts and the live bus map with traffic incidents.</p>"),
        ("table", "Side by side", """<table><thead><tr><th></th><th>GoSG Bus</th><th>BusSing</th></tr></thead><tbody>
<tr><td>Live LTA arrivals</td><td>✓</td><td>✓</td></tr>
<tr><td>Home and Lock Screen widgets</td><td>✓ (from 2.1)</td><td>✓</td></tr>
<tr><td>Live Activity / Dynamic Island</td><td>✓ (from 2.1)</td><td>✓</td></tr>
<tr><td>Apple Watch app</td><td>Not yet</td><td>✓</td></tr>
<tr><td>Offline MRT routing</td><td>MRT map (online)</td><td>✓</td></tr>
<tr><td>Plan a trip by asking</td><td>✓ Ask tab and Siri</td><td>Directions</td></tr>
<tr><td>Leave-now alerts at set times</td><td>✓</td><td>–</td></tr>
<tr><td>Get-off (alight) alerts</td><td>✓ (from 2.1)</td><td>✓</td></tr>
<tr><td>Bus map with traffic incidents</td><td>✓</td><td>Bus progress with traffic</td></tr>
<tr><td>Causeway cameras</td><td>✓</td><td>✓</td></tr>
<tr><td>Languages</td><td>6 (English, 简体, 繁體, Melayu, தமிழ், हिन्दी)</td><td>English</td></tr>
<tr><td>Minimum iOS</td><td>iOS 17</td><td>iOS 18</td></tr>
<tr><td>Ads</td><td>None</td><td>None</td></tr>
<tr><td>Paid tier</td><td>GoSG Plus (optional)</td><td>BusSing Express (optional)</td></tr>
</tbody></table>"""),
        ("bussing", "Where BusSing is better",
         "<p>If you want your bus on your wrist, BusSing has an Apple Watch app and GoSG doesn't yet. BusSing also plans MRT trips with no signal, which helps underground. It has more ratings on the App Store and ships updates often.</p>"),
        ("gosg", "Where GoSG is better",
         "<p>GoSG speaks six languages, so it works for parents and grandparents who read 中文, Melayu or தமிழ். You can type or say a question in plain words and get buses, transfers and time door to door. Leave-now alerts tell you when to walk out for your usual bus. It also runs on iOS 17, so older iPhones are covered.</p>"),
        ("pick", "Which should you try?",
         "<p>Try both on the same commute for a day; both are free to start. If Watch support is a must, pick BusSing. If you want alerts, Ask, or another language, pick GoSG.</p>"),
    ], disclosure=True)
    article("bus-widget-iphone", *GUIDES[2][1:3], GUIDES[2][3], [
        ("first", "First, star a stop", "<p>Open GoSG, find your stop on Nearby or Search, and tap the ☆. The widget shows your favourite stops, so it stays empty until you have one.</p>"),
        ("add", "Add the widget", '<ol class="steps"><li>Touch and hold an empty spot on the Home Screen until the apps jiggle.</li><li>Tap <b>Edit</b>, then <b>Add Widget</b>.</li><li>Search for <b>GoSG Bus</b> and pick small, medium or large.</li><li>Touch and hold the widget, tap <b>Edit Widget</b>, and choose which stop it shows.</li></ol><p>Widgets and Live Activities arrive in GoSG 2.1.</p>' + clip("add-widget", "../")),
        ("pick", "Show only the buses you take", '<p>Open your stop, touch and hold a bus, and tap <b>Show in widget</b>. The widget then lists only the starred buses for that stop. With none starred, it shows them all.</p>' + clip("widget-star", "../")),
        ("lock", "Lock Screen and Dynamic Island", "<p>Touch and hold a bus and tap <b>Track on Lock Screen</b>. It counts down on your Lock Screen and in the Dynamic Island, even when GoSG is closed. You can also say “Track my bus with GoSG” to Siri.</p>"),
        ("battery", "Does it drain the battery?", "<p>The widget fetches once and then counts down on its own, refreshing every few minutes. It doesn't poll every second.</p>"),
    ])
    article("causeway-traffic-cameras", *GUIDES[3][1:3], GUIDES[3][3], [
        ("where", "Where to find the cameras", "<p>Open <b>Search</b>: the checkpoint cameras are at the top. They also appear on bus stops for Causeway services such as the CW buses, 160, 170 and 950.</p>" + clip("cameras", "../")),
        ("which", "Which cameras", "<p>Woodlands Causeway and the Tuas Second Link, from the public traffic camera feed on data.gov.sg. Photos update every few minutes; pull down to refresh.</p>"),
        ("share", "Share with family", "<p>Tap Share on a camera to send the photo with a caption, so the people waiting for you know what the jam looks like.</p>"),
    ])
    article("last-bus-singapore", *GUIDES[4][1:3], GUIDES[4][3], [
        ("details", "Turn on arrival details", "<p>Go to <b>Settings › Show arrival details</b>. Each service then shows its destination, how often it comes, and first and last bus times for your stop.</p>"),
        ("ask", "Or just ask", "<p>Open the <b>Ask</b> tab and type “Last 52 tonight?” or “When's the first 14 tomorrow?”. GoSG answers for the stop you're at or the one you name.</p>" + clip("ask", "../")),
        ("note", "Holidays and eves", "<p>Last bus times follow the operator's published timetable. On eves of public holidays some services run later; LTA's live times will show the extra buses when they're on the road.</p>"),
    ])
    article("how-to-use-gosg", *GUIDES[5][1:3], GUIDES[5][3], [
        ("arrivals", "Live arrivals and the bus map", "<p>Nearby stops are on the first screen. Tap a stop for the next three buses of every service, then tap a bus to follow it on the map.</p>" + clip("arrivals", "../")),
        ("widget", "Widgets and the Lock Screen", "<p>Touch and hold a bus to pick it for the widget or to track it on the Lock Screen and in the Dynamic Island.</p>" + clip("widget-star", "../") + clip("add-widget", "../")),
        ("alerts", "Leave-now alerts", "<p>On Favourites, turn on alerts and pick your bus and your usual times. Free includes one alert; GoSG Plus has ten.</p>" + clip("leave-now", "../")),
        ("ask", "Ask", "<p>Type a question in plain words. GoSG answers with buses, where to change and the time door to door. Free includes five answers a day.</p>" + clip("ask", "../")),
        ("cameras", "Causeway cameras", "<p>Open Search to see the Woodlands and Tuas checkpoint cameras before you head to JB.</p>" + clip("cameras", "../")),
        ("mrt", "MRT stations", "<p>The MRT tab shows every station and exit. Switch to the list to find a station by name.</p>" + clip("mrt", "../")),
        ("traffic", "Traffic on the map", "<p>Traffic is off by default. Open the map, tap the map-style button and turn on <b>Show traffic on map</b>. Accidents and breakdowns appear as pins you can tap.</p>"),
    ])
    cards = "".join(f'<a class="card" href="{s}.html"><small>{c}</small><b>{t}</b><span>{d}</span></a>' for s, t, d, c in GUIDES)
    page("guides/index.html", "Singapore bus guides & app comparisons | GoSG Bus",
         "Guides to Singapore bus times, widgets, last buses and Causeway traffic, and honest bus app comparisons.",
         f'<section><div class="wrap"><p class="eyebrow">GoSG guides</p><h1 class="ph1">Singapore bus guides for your iPhone</h1><div class="cards">{cards}</div></div></section>')


def sitemap():
    urls = [BASE] + [BASE + "guides/"] + [BASE + f"guides/{s}.html" for s, *_ in GUIDES]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
        "".join(f"  <url><loc>{u}</loc><lastmod>{UPDATED}</lastmod></url>\n" for u in urls) + "</urlset>\n"
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(xml)


if __name__ == "__main__":
    home(); guides(); sitemap()
    print("built", ROOT)
