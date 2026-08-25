#!/usr/bin/env python3
"""Scan luma.com for Madrid events, diff against a seen-list, print anything new.

Standalone: only needs curl + python3. Used by the weekly Niah event tracker routine.
  python3 luma_scan.py            -> report new events, update seen-list
  python3 luma_scan.py --all      -> report everything found
"""
import json, re, subprocess, sys, os, csv, datetime

CITY_URL = "https://luma.com/madrid"
SEEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "luma-seen-events.csv")
# what Niah cares about: events with an audience that needs matchmaking
RELEVANT = re.compile(r'(summit|conferenc|congres|\bcon\b|con.?\d\d|forum|networking|meetup|mixer|'
                      r'demo ?day|pitch|founder|startup|investor|expo|fair|convention|community|'
                      r'breakfast|panel|workshop|hackathon|show.?and.?tell|b2b|business|tech|ai\b)', re.I)
# obvious non-fits: parties, dating, sport, purely social
IRRELEVANT = re.compile(r'(speed dating|summer party|aperitivo|social run|workout|yoga|brunch club|padel)', re.I)

def fetch(url):
    out = subprocess.run(["curl","-sS","-m","30","-A","Mozilla/5.0 (Windows NT 10.0; Win64; x64)",url],
                         capture_output=True, text=True)
    return out.stdout

def parse(html):
    """Pull event objects out of the embedded JSON blobs."""
    events, seen_ids = [], set()
    for m in re.finditer(r'\{"api_id":"(evt-[A-Za-z0-9]+)"', html):
        start = m.start()
        depth, i, n = 0, start, len(html)
        while i < n:                       # walk to the matching brace
            if html[i] == '{': depth += 1
            elif html[i] == '}':
                depth -= 1
                if depth == 0: break
            i += 1
        chunk = html[start:i+1]
        try: obj = json.loads(chunk)
        except Exception: continue
        # entries come as {"api_id":..,"event":{..}} or as the event object itself
        ev = obj.get("event") if isinstance(obj.get("event"), dict) else obj
        eid = ev.get("api_id") or obj.get("api_id")
        if not eid or eid in seen_ids: continue
        name = ev.get("name")
        if not name: continue
        hosts_src = obj.get("hosts") or ev.get("hosts") or []
        obj = {**ev, "hosts": hosts_src,
               "guest_count": obj.get("guest_count") or ev.get("guest_count") or 0,
               "ticket_info": obj.get("ticket_info") or ev.get("ticket_info") or {}}
        seen_ids.add(eid)
        geo = obj.get("geo_address_info") or {}
        ticket = obj.get("ticket_info") or {}
        price = ticket.get("price") or {}
        events.append({
            "api_id": eid,
            "name": name.strip(),
            "start": (obj.get("start_at") or "")[:10],
            "city": geo.get("city") or "",
            "venue": geo.get("address") or "",
            "url": "https://luma.com/" + (obj.get("url") or ""),
            "hosts": "; ".join(h.get("name") or "" for h in (obj.get("hosts") or []) if h.get("name")),
            "guests": obj.get("guest_count") or 0,
            "price": "free" if ticket.get("is_free") else (f"{price.get('cents',0)//100} {price.get('currency','')}".strip() or "paid"),
            "approval": "yes" if ticket.get("require_approval") else "no",
            "sold_out": "yes" if ticket.get("is_sold_out") else "no",
        })
    return events

def load_seen():
    if not os.path.exists(SEEN): return {}
    with open(SEEN, newline="", encoding="utf-8") as f:
        return {r["api_id"]: r for r in csv.DictReader(f)}

def save_seen(rows):
    cols = ["api_id","name","start","city","venue","url","hosts","guests","price","approval","sold_out","first_seen","relevant"]
    with open(SEEN, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
        for r in sorted(rows.values(), key=lambda x: x.get("start") or ""):
            w.writerow({c: r.get(c, "") for c in cols})

def main():
    show_all = "--all" in sys.argv
    today = datetime.date.today().isoformat()
    html = fetch(CITY_URL)
    if len(html) < 5000:
        print("SCAN FAILED: could not fetch luma.com/madrid"); sys.exit(1)
    found = parse(html)
    seen = load_seen()
    new = []
    for e in found:
        e["relevant"] = "no" if IRRELEVANT.search(e["name"]) else ("yes" if RELEVANT.search(e["name"]) else "no")
        if e["api_id"] not in seen:
            e["first_seen"] = today
            seen[e["api_id"]] = e
            new.append(e)
        else:
            seen[e["api_id"]].update({k: v for k, v in e.items() if v})
    save_seen(seen)
    report = found if show_all else new
    upcoming = [e for e in report if e["start"] >= today]
    print(f"scanned luma.com/madrid: {len(found)} events on page, {len(new)} new, {len(seen)} tracked total\n")
    if not upcoming:
        print("No new upcoming Madrid events this week.")
        return
    for e in sorted(upcoming, key=lambda x: x["start"]):
        flag = "*" if e["relevant"] == "yes" else " "
        extra = []
        if e["sold_out"] == "yes": extra.append("SOLD OUT")
        if e["approval"] == "yes": extra.append("approval needed")
        print(f"{flag} {e['start']}  {e['name'][:52]:<52} {e['price']:<10} {e['guests']:>4} guests  {' '.join(extra)}")
        print(f"    {e['url']}   hosts: {e['hosts'][:60]}")
    print("\n* = matches Niah's relevance filter (conference/summit/networking/founder/etc)")

if __name__ == "__main__":
    main()
