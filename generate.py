#!/usr/bin/env python3
"""Generate Neem email signature pages from people.json.

Usage:
  python3 generate.py            # build a page for everyone in people.json
  python3 generate.py "Name"     # build only the person whose name matches

Each page is written to signatures/<first-last>.html. Open it in a browser,
click "Copy signature", and paste into Gmail (Settings > Signature).
"""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).parent
BASE = "https://raw.githubusercontent.com/neemdotio/email-assets/main/"
FONT = "'General Sans','Helvetica Neue',Helvetica,Arial,sans-serif"
LINK = 'style="color:#111111;text-decoration:none;"'
SEP = '<span style="color:#C9C5BD;">&nbsp;&nbsp;|&nbsp;&nbsp;</span>'
BRANDS = {
    "neem": {
        "logo": "neem-logo-keyline.png", "alt": "Neem", "logo_w": 80, "logo_h": 24,
        "web_url": "https://www.neem.io", "web_text": "neem.io",
        "linkedin_url": "https://www.linkedin.com/company/neemdotio",
    },
    # Set "brand": "paymenow" on a person in people.json to use this template.
    "paymenow": {
        "logo": "paymenow-logo-keyline.png", "alt": "Neem Paymenow", "logo_w": 163, "logo_h": 21,
        "web_url": "https://paymenow.neem.io/", "web_text": "paymenow.neem.io",
        "linkedin_url": "https://www.linkedin.com/showcase/neem-paymenow",
    },
}


def icon(name):
    return (f'<img src="{BASE}{name}.png" alt="" width="14" height="14" '
            'style="display:inline-block;vertical-align:middle;border:0;'
            'width:14px;height:14px;margin:0 6px 2px 0;">')


def stacked_signature(p):
    """Brand layout: logo, tagline, then website | LinkedIn | Instagram (for shared mailboxes)."""
    b = BRANDS[p.get("brand", "neem")]
    links = [(icon("web"), b["web_url"], b["web_text"]),
             (icon("linkedin"), b["linkedin_url"], "LinkedIn")]
    if p.get("instagram"):
        links.append((icon("instagram"), f'https://www.instagram.com/{p["instagram"]}/', "Instagram"))
    row = SEP.join(f'{ic}<a href="{u}" {LINK}>{t}</a>' for ic, u, t in links)
    return f'''<table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;font-family:{FONT};font-size:13px;line-height:20px;color:#111111;">
<tr><td style="padding:0 0 8px 0;"><img src="{BASE}{b["logo"]}" alt="{b["alt"]}" width="{b["logo_w"]}" height="{b["logo_h"]}" style="display:block;border:0;width:{b["logo_w"]}px;height:{b["logo_h"]}px;"></td></tr>
<tr><td style="padding:0 0 8px 0;font-size:13px;line-height:20px;color:#6B6B6B;">{html.escape(p["tagline"])}</td></tr>
<tr><td style="border-top:1px solid #E0DDD7;padding:8px 0 0 0;font-size:12px;line-height:18px;white-space:nowrap;">{row}</td></tr>
</table>'''


def signature(p):
    if p.get("layout") == "stacked":
        return stacked_signature(p)
    b = BRANDS[p.get("brand", "neem")]
    e = lambda v: html.escape(v, quote=True)
    contact = []
    phones = p.get("phone") or []
    if isinstance(phones, str):
        phones = [phones]
    if phones:
        links = [f'<a href="tel:+{re.sub(r"\D", "", ph)}" {LINK}>{e(ph)}</a>' for ph in phones]
        contact.append(", ".join(links))
    if p.get("email"):
        contact.append(f'<a href="mailto:{e(p["email"])}" {LINK}>{e(p["email"])}</a>')
    # Title and contact details are optional (shared mailboxes like support@ have neither).
    title_html = f'<div style="color:#6B6B6B;padding:0 0 6px 0;">{e(p["title"])}</div>' if p.get("title") else ""
    contact_html = f'<div style="font-size:12px;line-height:18px;">{SEP.join(contact)}</div>' if contact else ""
    rule = "border-top:1px solid #E0DDD7;margin-top:6px;padding-top:6px;" if (title_html or contact_html) else ""
    return f'''<table cellpadding="0" cellspacing="0" border="0" style="border-collapse:collapse;font-family:{FONT};font-size:13px;line-height:20px;color:#111111;"><tr>
<td style="padding:0 18px 0 0;vertical-align:middle;"><img src="{BASE}{b["logo"]}" alt="{b["alt"]}" width="{b["logo_w"]}" height="{b["logo_h"]}" style="display:block;border:0;width:{b["logo_w"]}px;height:{b["logo_h"]}px;"></td>
<td style="padding:0 0 0 18px;border-left:1px solid #E0DDD7;vertical-align:middle;">
<div style="font-size:14px;line-height:20px;font-weight:600;">{e(p["name"])}</div>
{title_html}{contact_html}
<div style="{rule}font-size:12px;line-height:18px;white-space:nowrap;">{icon("web")}<a href="{b["web_url"]}" {LINK}>{b["web_text"]}</a><span style="display:inline-block;width:16px;font-size:0;line-height:0;">&nbsp;</span>{icon("linkedin")}<a href="{b["linkedin_url"]}" {LINK}>LinkedIn</a></div>
</td></tr></table>'''


PAGE = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{name} — Neem email signature</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{{margin:0;background:#F5F4F1;font-family:'General Sans','Helvetica Neue',Helvetica,Arial,sans-serif;color:#111}}
.wrap{{max-width:640px;margin:0 auto;padding:40px 24px}}
h1{{font-size:22px;font-weight:600;margin:0 0 6px}} p.sub{{color:#6B6B6B;margin:0 0 24px;font-size:14px}}
.box{{background:#fff;border:1px solid #E0DDD7;border-radius:8px;padding:28px;overflow-x:auto}}
button{{margin-top:18px;background:#111;color:#fff;border:0;border-radius:6px;padding:10px 18px;font:500 14px inherit;font-family:inherit;cursor:pointer}}
ol{{font-size:14px;line-height:1.7;padding-left:20px;margin:24px 0 0}}
</style></head><body><div class="wrap">
<h1>{name} — email signature</h1>
<p class="sub">Copy the signature below and paste it into Gmail.</p>
<div class="box"><div id="sig">
{sig}
</div></div>
<button id="btn" onclick="copySig()">Copy signature</button>
<ol>
<li>Click <b>Copy signature</b>.</li>
<li>In Gmail: <b>Settings (gear) → See all settings → General → Signature</b>.</li>
<li>Click <b>Create new</b>, name it “Neem”, and paste (Ctrl/Cmd + V) into the box.</li>
<li>Under <b>Signature defaults</b>, choose it for new emails and replies. Click <b>Save changes</b>.</li>
</ol></div>
<script>
function copySig(){{var el=document.getElementById('sig'),r=document.createRange();r.selectNodeContents(el);var s=getSelection();s.removeAllRanges();s.addRange(r);var ok=document.execCommand('copy');s.removeAllRanges();document.getElementById('btn').textContent=ok?'Copied ✓':'Press Ctrl/Cmd+C instead';}}
</script></body></html>
'''


def main():
    people = json.loads((ROOT / "people.json").read_text(encoding="utf-8"))
    if len(sys.argv) > 1:
        want = " ".join(sys.argv[1:]).lower()
        people = [p for p in people if want in p["name"].lower()]
        if not people:
            sys.exit(f"No one in people.json matches {want!r}")
    out = ROOT / "signatures"
    out.mkdir(exist_ok=True)
    for p in people:
        slug = re.sub(r"[^a-z0-9]+", "-", p["name"].lower()).strip("-")
        path = out / f"{slug}.html"
        path.write_text(PAGE.format(name=html.escape(p["name"]), sig=signature(p)), encoding="utf-8")
        print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
