// Live Singapore bus arrival times in the browser. Same data as the GoSG app:
// stops from data/stops.json (LTA Bus Stops), live times from GoSG's getbusarrivals
// (LTA BusArrival), first/last bus from GoSG's public timetable (bus_static_v1/hours_XX).
(() => {
  const ARRIVALS = "https://asia-southeast1-bussg-1289.cloudfunctions.net/getbusarrivals";
  const HOURS = "https://firestore.googleapis.com/v1/projects/bussg-1289/databases/(default)/documents/bus_static_v1/hours_";
  const $ = (s) => document.querySelector(s);
  const q = $("#q"), results = $("#results"), panel = $("#stop"), recentBox = $("#recent");
  let stops = [], current = null, timer = null, fetchedAt = 0;

  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const store = {
    get() { try { return JSON.parse(localStorage.getItem("gosg.recent") || "[]"); } catch { return []; } },
    add(code) { try { localStorage.setItem("gosg.recent", JSON.stringify([code, ...store.get().filter((c) => c !== code)].slice(0, 6))); } catch {} },
  };
  const byCode = (c) => stops.find((s) => s[0] === c);

  function stopItem(s, extra = "") {
    return `<button class="bt-item" data-code="${s[0]}"><b>${esc(s[1])}</b><span>${esc(s[2])} · ${s[0]}${extra}</span></button>`;
  }
  function list(items, title) {
    results.innerHTML = items.length
      ? (title ? `<p class="bt-label">${title}</p>` : "") + items.join("")
      : `<p class="bt-empty">No stops match. Try a road name or the 5-digit code on the bus stop pole.</p>`;
  }
  function search(text) {
    const t = text.trim().toLowerCase();
    if (!t) { results.innerHTML = ""; return; }
    const hits = stops.filter((s) => s[0].startsWith(t) || s[1].toLowerCase().includes(t) || s[2].toLowerCase().includes(t));
    hits.sort((a, b) => (b[1].toLowerCase().startsWith(t) - a[1].toLowerCase().startsWith(t)) || (b[0] === t) - (a[0] === t));
    list(hits.slice(0, 12).map((s) => stopItem(s)));
  }

  function near() {
    if (!navigator.geolocation) return list([], "");
    results.innerHTML = `<p class="bt-empty">Finding stops near you…</p>`;
    navigator.geolocation.getCurrentPosition((p) => {
      const { latitude: la, longitude: lo } = p.coords;
      const d = (s) => Math.hypot((s[3] - la) * 111.2, (s[4] - lo) * 111.2 * Math.cos(la * Math.PI / 180));
      const hits = stops.map((s) => [s, d(s)]).sort((a, b) => a[1] - b[1]).slice(0, 8);
      list(hits.map(([s, km]) => stopItem(s, ` · ${Math.round(km * 1000)} m`)), "Nearest stops");
    }, () => { results.innerHTML = `<p class="bt-empty">Location is off. Search by stop name or code instead.</p>`; },
    { enableHighAccuracy: true, timeout: 10000 });
  }

  // First/last bus: "service|dir|wdFirst|wdLast|satFirst|satLast|sunFirst|sunLast", times HHMM.
  async function hours(code) {
    try {
      const r = await fetch(HOURS + code.slice(0, 2));
      const rows = (await r.json()).fields?.h?.mapValue?.fields?.[code]?.arrayValue?.values || [];
      const day = new Date(Date.now() + 8 * 3600e3).getUTCDay();           // Singapore time
      const col = day === 0 ? 6 : day === 6 ? 4 : 2;
      const out = {};
      for (const v of rows) {
        const p = v.stringValue.split("|");
        if (p[col] && p[col] !== "-" && !out[p[0]]) out[p[0]] = [p[col], p[col + 1]];
      }
      return out;
    } catch { return {}; }
  }
  const hhmm = (t) => (t && t.length === 4 ? `${t.slice(0, 2)}:${t.slice(2)}` : "–");

  function mins(iso) {
    if (!iso) return null;
    return Math.max(0, Math.floor((new Date(iso) - Date.now()) / 60000));
  }
  const loadCls = { SEA: "seats", SDA: "stand", LSD: "full" };
  const loadText = { SEA: "Seats", SDA: "Standing", LSD: "Limited standing" };
  function cell(bus) {
    const m = mins(bus?.EstimatedArrival);
    if (m === null) return `<td class="bt-none">–</td>`;
    const dd = bus.Type === "DD" ? " · double deck" : bus.Type === "BD" ? " · bendy" : "";
    return `<td><span class="bt-m ${loadCls[bus.Load] || ""}" title="${loadText[bus.Load] || ""}${dd}">${m < 1 ? "Arr" : m}</span>${m >= 1 ? "<small>min</small>" : ""}</td>`;
  }

  async function show(code, push = true) {
    const s = byCode(code);
    if (!s) return;
    current = s;
    store.add(code); recent();
    if (push) history.replaceState(null, "", `?stop=${code}`);
    document.title = `${s[1]} (${code}) bus arrival times | GoSG Bus`;
    panel.hidden = false;
    panel.innerHTML = `<div class="bt-head"><div><h2>${esc(s[1])}</h2><p>${esc(s[2])} · Stop ${code}</p></div>
      <button class="bt-refresh" aria-label="Refresh">↻</button></div><div id="bt-body"><p class="bt-empty">Loading live times…</p></div>`;
    panel.querySelector(".bt-refresh").onclick = () => load();
    panel.scrollIntoView({ behavior: "smooth", block: "start" });
    await load();
  }

  async function load() {
    if (!current) return;
    const code = current[0], body = $("#bt-body");
    try {
      const [r, hrs] = await Promise.all([
        fetch(ARRIVALS, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ data: { busStopCode: code } }) }),
        hours(code),
      ]);
      if (!r.ok) throw new Error(r.status);
      const services = ((await r.json()).result?.Services || []).sort((a, b) =>
        a.ServiceNo.localeCompare(b.ServiceNo, undefined, { numeric: true }));
      if (current[0] !== code) return;
      fetchedAt = Date.now();
      body.innerHTML = services.length ? `<table class="bt-table"><thead><tr><th>Bus</th><th>Next</th><th>2nd</th><th>3rd</th><th>First / last today</th></tr></thead><tbody>
        ${services.map((x) => `<tr><th>${esc(x.ServiceNo)}</th>${cell(x.NextBus)}${cell(x.NextBus2)}${cell(x.NextBus3)}
          <td class="bt-hours">${hrs[x.ServiceNo] ? `${hhmm(hrs[x.ServiceNo][0])} – ${hhmm(hrs[x.ServiceNo][1])}` : "–"}</td></tr>`).join("")}
        </tbody></table><p class="bt-meta"><span id="bt-age"></span> · <i class="bt-dot seats"></i>Seats <i class="bt-dot stand"></i>Standing <i class="bt-dot full"></i>Limited standing</p>`
        : `<p class="bt-empty">No buses on the way right now. Services may have ended for the night.</p>`;
      age();
    } catch {
      body.innerHTML = `<p class="bt-empty">Can't load live times right now. LTA's feed may be briefly down; try again in a minute.</p>`;
    }
    clearTimeout(timer);
    timer = setTimeout(() => { if (document.visibilityState === "visible") load(); else timer = null; }, 20000);
  }
  function age() {
    const el = $("#bt-age");
    if (el && fetchedAt) el.textContent = `Updated ${Math.round((Date.now() - fetchedAt) / 1000)} s ago`;
  }
  setInterval(age, 1000);
  document.addEventListener("visibilitychange", () => { if (document.visibilityState === "visible" && current && !timer) load(); });

  function recent() {
    const codes = store.get().map(byCode).filter(Boolean);
    recentBox.innerHTML = codes.length ? `<p class="bt-label">Recent</p>` + codes.map((s) => stopItem(s)).join("") : "";
  }

  document.addEventListener("click", (e) => {
    const b = e.target.closest(".bt-item");
    if (b) show(b.dataset.code);
  });
  q.addEventListener("input", () => search(q.value));
  $("#near").addEventListener("click", near);

  fetch("data/stops.json").then((r) => r.json()).then((d) => {
    stops = d.stops;
    recent();
    const code = new URLSearchParams(location.search).get("stop");
    if (code && byCode(code)) show(code, false);
    if (q.value) search(q.value);
  });
})();
