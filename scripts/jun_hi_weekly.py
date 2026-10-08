#!/usr/bin/env python3
"""Weekly intake from the public Telegram channel @jun_hi («Дизайнер, привет»).

Finds «Inspiration #N» posts newer than the last processed issue, extracts the site links,
drops ones already on Brandcraft (or previously rejected), checks they are alive and not
Russian, and writes candidates to source/jun_hi_pending.json for classification.

Run: python3 scripts/jun_hi_weekly.py
State: source/jun_hi_state.json  ({"last_issue": N, "rejected": [hosts...]})
"""
import html
import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "source" / "jun_hi_state.json"
PENDING = ROOT / "source" / "jun_hi_pending.json"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
SKIP_HOSTS = {"t.me", "hirehi.ru"}
RU_TLD = re.compile(r"\.(ru|su|xn--p1ai|moscow|spb|msk)$")
BAD = re.compile(r"casino|togel|toto macau|gacor|for sale|domain is|buy this domain|parked|hugedomains|"
                 r"afternic|dan\.com|atom\.com/(name|lpd)|spaceship\.com|expireddomains|coming soon", re.I)


def curl(url, timeout=20):
    p = subprocess.run(["curl", "-sL", "-m", str(timeout), "--max-redirs", "8", "-A", UA,
                        "-H", "Accept-Language: en-US,en;q=0.9", "-o", "-",
                        "-w", "\n__C__%{http_code} %{url_effective}", url], capture_output=True)
    out = p.stdout.decode("utf-8", "replace")
    body, _, tail = out.rpartition("\n__C__")
    code, _, final = tail.partition(" ")
    return int(code or 0), final, body


def host_of(url):
    return (urlparse(url).hostname or "").lower().removeprefix("www.")


def base_domain(host):
    """example.com for ru.example.com / share.example.com; keeps example.co.uk."""
    parts = host.split(".")
    if len(parts) > 2 and parts[-2] in ("co", "com", "org", "net", "gov", "ac") and len(parts[-1]) == 2:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


def catalogue_hosts():
    """Every host already on the site (items + chips), plus dead/dropped lists."""
    js = (ROOT / "data.js").read_text()
    cat = json.loads(js.split("window.CATALOGUE = ", 1)[1].split(";\nwindow.AI_GUIDE", 1)[0])
    hosts = set()
    for c in cat:
        for s in c["sections"]:
            for i in s["items"]:
                hosts.add(host_of(i["url"]))
                hosts.update(host_of(k["url"]) for k in i.get("cases", []))
    dead = ROOT / "source" / "product-sites-dead.txt"
    if dead.exists():
        hosts.update(h.strip().removeprefix("www.") for h in dead.read_text().split() if h.strip())
    return hosts | {base_domain(h) for h in hosts}


def fetch_posts(pages=3):
    """Latest channel posts from the public web preview (t.me/s/…), newest pages first."""
    posts, before = {}, None
    for _ in range(pages):
        _, _, b = curl("https://t.me/s/jun_hi" + (f"?before={before}" if before else ""), 25)
        items = re.findall(r'data-post="jun_hi/(\d+)"(.*?)(?=data-post="jun_hi/|\Z)', b, re.S)
        if not items:
            break
        for pid, chunk in items:
            txt = re.search(r'<div class="tgme_widget_message_text[^"]*"[^>]*>(.*?)</div>', chunk, re.S)
            raw = txt.group(1) if txt else ""
            date = re.search(r'<time datetime="([^"]+)"', chunk)
            posts[int(pid)] = {
                "text": html.unescape(re.sub(r"<[^>]+>", " ", raw)),
                "links": [html.unescape(x) for x in re.findall(r'href="(https?://[^"]+)"', raw)],
                "date": date.group(1)[:10] if date else "",
            }
        before = min(int(p) for p, _ in items)
    return posts


def inspect(url):
    code, final, b = curl(url)
    meta = lambda n: (re.search(r'<meta[^>]+(?:name|property)=["\']' + n + r'["\'][^>]*content=["\']([^"\']*)', b, re.I)
                      or re.search(r'<meta[^>]+content=["\']([^"\']*)["\'][^>]*(?:name|property)=["\']' + n + r'["\']', b, re.I))
    m = meta("og:description") or meta("description")
    t = re.search(r"<title[^>]*>(.*?)</title>", b, re.S | re.I)
    lang = re.search(r'<html[^>]*\blang=["\']?([a-zA-Z-]+)', b)
    text = re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", b, flags=re.S)
    cyr = len(re.findall(r"[А-Яа-яЁё]", text))
    uk = len(re.findall(r"[ІіЇїЄєҐґ]", text))
    lat = len(re.findall(r"[A-Za-z]", text))
    title = html.unescape(re.sub(r"\s+", " ", t.group(1))).strip()[:140] if t else ""
    desc = html.unescape(m.group(1)).strip()[:240] if m else ""
    status = "ok"
    if code == 0 or code >= 500 or code in (402, 404, 410):
        status = "dead"
    elif RU_TLD.search(host_of(final or url)) or (lang and lang.group(1).lower().startswith("ru")) \
            or (cyr > 300 and cyr > lat * 0.6 and uk < cyr * 0.01):
        status = "russian"
    elif BAD.search(f"{title} {desc} {final}"):
        status = "parked_or_spam"
    elif code in (401, 403, 429):
        status = "bot_protected"  # alive, but the page is a bot check
    return {"url": url, "final": re.sub(r"[?#].*$", "", final or url), "code": code,
            "status": status, "title": title, "desc": desc}


def main():
    state = json.loads(STATE.read_text()) if STATE.exists() else {"last_issue": 0, "rejected": []}
    posts = fetch_posts()
    issues = []
    for pid, p in sorted(posts.items()):
        m = re.search(r"Inspiration\s*#\s*(\d+)", p["text"], re.I)
        if m and int(m.group(1)) > state["last_issue"]:
            issues.append((int(m.group(1)), pid, p))
    if not issues:
        PENDING.write_text(json.dumps({"issues": [], "candidates": []}, ensure_ascii=False, indent=1))
        print(f"No new Inspiration posts after #{state['last_issue']}.")
        return

    have = catalogue_hosts() | set(state.get("rejected", []))
    seen, urls = set(), []
    for num, pid, p in issues:
        for link in p["links"]:
            u = urlparse(link)
            h = host_of(link)
            if not h or h in SKIP_HOSTS or h in have or base_domain(h) in have or h in seen:
                continue
            seen.add(h)
            path = u.path if u.path not in ("", "/") else "/"
            urls.append((num, f"https://{h}{path}"))

    checked = list(ThreadPoolExecutor(24).map(lambda x: {**inspect(x[1]), "issue": x[0]}, urls))
    PENDING.write_text(json.dumps({
        "issues": [{"issue": n, "post": f"https://t.me/jun_hi/{pid}", "date": p["date"]} for n, pid, p in issues],
        "candidates": checked,
    }, ensure_ascii=False, indent=1))
    by = {}
    for c in checked:
        by[c["status"]] = by.get(c["status"], 0) + 1
    print(f"Issues: {[n for n, _, _ in issues]}; new links: {len(checked)}; by status: {by}")


if __name__ == "__main__":
    main()
