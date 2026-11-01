"""Dimensional SVG charts with fixed readable labels and real GitHub values."""
from collections import Counter
from datetime import date, timedelta
from html import escape
from math import cos, sin, pi
from pathlib import Path
import xml.etree.ElementTree as ET


def render_dashboard(destination, repositories, days, current, longest, stamp):
    assert days and all(day["contributionCount"] >= 0 for day in days)
    languages = Counter(repo["primaryLanguage"]["name"] for repo in repositories if repo["primaryLanguage"])
    assert languages and len(repositories) <= 100
    colors = ["#D8F1FC", "#85B6D0", "#527C99", "#36536E", "#294154"]
    ordered = languages.most_common(4)
    other = sum(languages.values()) - sum(value for _, value in ordered)
    if other:
        ordered.append(("Other", other))
    weeks = {}
    for day in days:
        value = date.fromisoformat(day["date"])
        monday = value - timedelta(days=value.weekday())
        weeks[monday.isoformat()] = weeks.get(monday.isoformat(), 0) + day["contributionCount"]
    weekly = list(weeks.items())[-8:]
    assert len(weekly) == 8

    def text(x, y, value, size=16, color="#D9E6EE", extra=""):
        return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {extra}>{escape(str(value))}</text>'

    def tile(x, y, width, label, value):
        return (f'<rect x="{x+5}" y="{y+8}" width="{width}" height="86" rx="12" fill="#020509"/>'
                f'<rect x="{x}" y="{y}" width="{width}" height="86" rx="12" fill="url(#metal)" stroke="#42586B"/>'
                f'<path d="M{x+14} {y+1}H{x+width-14}" stroke="#C8E4F4" stroke-opacity=".35"/>'
                + text(x+20, y+27, label, 12, "#9FB8CA", 'letter-spacing="1"')
                + text(x+20, y+66, f"{value:,}", 32, "#F5FAFF", 'font-weight="600"'))

    def ring_path(start, end, offset=0):
        def point(radius, angle):
            return 134 + radius*cos(angle), 116 + radius*.58*sin(angle) + offset
        a,b = point(97,start),point(97,end)
        c,d = point(60,end),point(60,start)
        large = int(end-start > pi)
        return (f'M{a[0]:.2f},{a[1]:.2f} A97,56.26 0 {large} 1 {b[0]:.2f},{b[1]:.2f} '
                f'L{c[0]:.2f},{c[1]:.2f} A60,34.8 0 {large} 0 {d[0]:.2f},{d[1]:.2f}Z')

    ring = [text(0, 0, "Languages in the public portfolio", 20, "#F5FAFF"),
            '<ellipse cx="139" cy="148" rx="105" ry="52" fill="#000" opacity=".4"/>']
    segments, angle = [], -pi/2
    for index, (name, count) in enumerate(ordered):
        end = angle + count / sum(languages.values()) * 2*pi
        segments.append((angle+.015, end-.015, colors[index]))
        ring += [text(270, 62+index*29, name, 15),
                 text(450, 62+index*29, f"{count} repos", 14, "#9FB8CA", 'text-anchor="end"'),
                 f'<rect x="249" y="{51+index*29}" width="9" height="9" rx="2" fill="{colors[index]}"/>']
        angle = end
    assert abs(angle - 3*pi/2) < .0001
    for start, end, _ in segments:
        ring.append(f'<path d="{ring_path(start,end,17)}" fill="#223A4E" stroke="#162736"/>')
    for start, end, color in segments:
        ring.append(f'<path d="{ring_path(start,end)}" fill="{color}" stroke="#0C1824" stroke-width="1.2"/>')
    ring += [text(134, 121, sum(languages.values()), 24, "#F5FAFF", 'text-anchor="middle" font-weight="600"'),
             text(0, 225, f"{sum(languages.values())} classified / {len(repositories)} public non-fork repositories", 12, "#8DA8BD")]

    bars = [text(0, 0, "Contribution momentum", 20, "#F5FAFF")]
    for y in (75, 125, 175):
        bars.append(f'<path d="M8 {y+10}L26 {y}H421" fill="none" stroke="#2B4154" stroke-opacity=".5"/>')
    maximum = max(value for _, value in weekly) or 1
    for index, (day, count) in enumerate(weekly):
        x, y, height, width = 17+index*49, 176, count/maximum*108, 25
        top = y-height
        bars += [f'<path d="M{x} {y}L{x+12} {y-8}H{x+width+12}L{x+width} {y}Z" fill="#122231"/>',
                 f'<path d="M{x+width} {y}L{x+width+12} {y-8}V{top-8}L{x+width} {top}Z" fill="#31546E"/>',
                 f'<path d="M{x} {top}L{x+12} {top-8}H{x+width+12}L{x+width} {top}Z" fill="#D3EAF6"/>',
                 f'<rect x="{x}" y="{top}" width="{width}" height="{height}" fill="url(#bar)"/>',
                 text(x+12, top-16, count, 12, "#E8F5FD", 'text-anchor="middle"'),
                 text(x+12, 201, day[5:].replace("-","/"), 10, "#A0B9CA", 'text-anchor="middle"')]
    bars.append(text(0, 225, "8 calendar weeks · week starting · latest week partial", 12, "#8DA8BD"))

    for mobile in (False, True):
        width, height = (520, 900) if mobile else (1000, 490)
        svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
               '<title id="title">GitHub engineering dashboard</title>',
               '<desc id="desc">Real contribution totals and streaks, a dimensional language ring, and extruded weekly contribution bars. Values are refreshed daily.</desc>',
               '<defs><linearGradient id="metal" x2=".2" y2="1"><stop stop-color="#243747"/><stop offset=".4" stop-color="#13212F"/><stop offset="1" stop-color="#0B141F"/></linearGradient><linearGradient id="bar" x2="1" y2=".3"><stop stop-color="#79A8C2"/><stop offset=".5" stop-color="#ACCDDF"/><stop offset="1" stop-color="#5B839E"/></linearGradient><radialGradient id="sky"><stop stop-color="#172D40"/><stop offset="1" stop-color="#080E16"/></radialGradient></defs>',
               f'<rect x="2" y="6" width="{width-4}" height="{height-8}" rx="18" fill="#010408"/>',
               f'<rect x=".5" y=".5" width="{width-8}" height="{height-12}" rx="18" fill="url(#sky)" stroke="#3B5267"/>',
               '<g font-family="Segoe UI,Arial,sans-serif">', text(32, 37, "ENGINEERING / GITHUB SIGNAL", 14, "#9FB8CA", 'letter-spacing="2"')]
        values = [("CONTRIBUTIONS", sum(day["contributionCount"] for day in days)),
                  ("CURRENT STREAK / DAYS", current), ("LONGEST / LAST 365 DAYS", longest),
                  ("PUBLIC REPOSITORIES", len(repositories))]
        for index, (label, value) in enumerate(values):
            x, y = (24+(index%2)*248, 68+(index//2)*108) if mobile else (32+index*240, 68)
            svg.append(tile(x,y,226,label,value))
        svg += [f'<g transform="translate({24 if mobile else 40},{330 if mobile else 212})">'+"".join(ring)+'</g>',
                f'<g transform="translate({35 if mobile else 550},{625 if mobile else 212})">'+"".join(bars)+'</g>',
                text(32,height-25,f"GitHub data · {stamp} UTC · contributions and streaks: last 365 days",11,"#7793A8"),'</g></svg>']
        output = "\n".join(svg)
        ET.fromstring(output)
        Path(destination, "dashboard-mobile.svg" if mobile else "dashboard.svg").write_text(output,encoding="utf-8")
