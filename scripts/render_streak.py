"""Render an accurate streak card from GitHub's last 365 days of contributions."""
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from dashboard_art import render_dashboard


def streaks(counts):
    current = longest = run = 0
    for count in counts:
        run = run + 1 if count else 0
        longest = max(longest, run)
    eligible = counts[:-1] if counts and counts[-1] == 0 else counts
    for count in reversed(eligible):
        if not count:
            break
        current += 1
    return current, longest


assert streaks([]) == (0, 0)
assert streaks([0, 2, 1, 0]) == (2, 2)
assert streaks([1, 1, 0, 0]) == (0, 2)
assert streaks([1, 0, 2, 3, 4]) == (3, 3)

now = datetime.now(timezone.utc)
start = now - timedelta(days=364)
query = '''query($from:DateTime!,$to:DateTime!){
  user(login:"loktrishal-05"){
    repositories(first:100,privacy:PUBLIC,isFork:false,ownerAffiliations:OWNER){
      totalCount nodes{primaryLanguage{name}}
    }
    contributionsCollection(from:$from,to:$to){
      contributionCalendar{weeks{contributionDays{date contributionCount}}}
    }
  }
}'''
result = subprocess.run(
    ["gh", "api", "graphql", "-f", "query=" + query,
     "-f", "from=" + start.strftime("%Y-%m-%dT00:00:00Z"),
     "-f", "to=" + now.strftime("%Y-%m-%dT%H:%M:%SZ")],
    check=True, capture_output=True, text=True, encoding="utf-8"
)
data = json.loads(result.stdout)
if data.get("errors"):
    raise RuntimeError("GitHub contribution query failed")
weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
days = [day for week in weeks for day in week["contributionDays"]
        if start.date().isoformat() <= day["date"] <= now.date().isoformat()]
counts = [day["contributionCount"] for day in days]
assert days and all(isinstance(n, int) and n >= 0 for n in counts)
current, longest = streaks(counts)
values = [(150, sum(counts), "CONTRIBUTIONS"), (450, current, "CURRENT STREAK"),
          (750, longest, "LONGEST IN WINDOW")]
svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 210" role="img" aria-labelledby="title desc">',
       '<title id="title">Contribution streaks</title>',
       '<desc id="desc">Last 365 days. Current streak allows today to be unfinished. Longest streak is limited to this window.</desc>',
       '<rect x=".5" y=".5" width="899" height="209" rx="14" fill="#0B1018" stroke="#23445E"/>',
       '<path d="M300 40V155M600 40V155" stroke="#23445E"/>',
       '<g font-family="Segoe UI,Arial,sans-serif" text-anchor="middle">']
for x, value, label in values:
    svg += [f'<text x="{x}" y="95" font-size="42" font-weight="600" fill="#F8FAFC">{value:,}</text>',
            f'<text x="{x}" y="128" font-size="12" letter-spacing="1.5" fill="#7DD3FC">{label}</text>']
svg += [f'<text x="450" y="182" font-size="12" fill="#94A3B8">GitHub contribution calendar · last 365 days · {now.date()} UTC</text>', '</g></svg>']
destination = Path(sys.argv[1])
destination.parent.mkdir(parents=True, exist_ok=True)
destination.write_text("\n".join(svg) + "\n", encoding="utf-8")
repositories = data["data"]["user"]["repositories"]
# shortcut: the language chart covers up to 100 public repositories; paginate before exceeding 100.
assert repositories["totalCount"] <= 100, "Add repository pagination before publishing a partial dashboard"
render_dashboard(destination.parent, repositories["nodes"], days, current, longest, now.date())
print(f"Verified streak card: {current} current, {longest} longest in window")
