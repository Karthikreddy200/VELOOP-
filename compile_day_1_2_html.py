import markdown
import re

md_path = r"C:\Users\ckart\.gemini\antigravity\scratch\veloop_analytics_task01\VELOOP_DAY_1_2_SUBMISSION.md"
html_path = r"C:\Users\ckart\.gemini\antigravity\scratch\veloop_analytics_task01\VELOOP_DAY_1_2_SUBMISSION.html"

with open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

# Preprocess github alerts: > [!IMPORTANT]
def replace_alerts(match):
    alert_type = match.group(1).upper()
    content = match.group(2).strip()
    return f'<div class="alert alert-{alert_type.lower()}"><strong>{alert_type}:</strong> {content}</div>'

text = re.sub(r'> \[!(IMPORTANT|NOTE|WARNING|TIP|CAUTION)\]\s*\n((?:> .*\n?)+)', 
              lambda m: f'<div class="alert alert-{m.group(1).lower()}"><strong>{m.group(1)}:</strong> {re.sub(r"^> ", "", m.group(2), flags=re.MULTILINE)}</div>', 
              text)

# Convert Markdown to HTML
body = markdown.markdown(text, extensions=['extra', 'tables', 'fenced_code'])

# Post-process mermaid code blocks
body = re.sub(r'<pre><code class="language-mermaid">([\s\S]*?)</code></pre>', r'<div class="mermaid">\1</div>', body)

# Add badges for Confirmed, Proposed, To Be Verified
body = body.replace('<td>Confirmed</td>', '<td><span class="badge badge-confirmed">Confirmed</span></td>')
body = body.replace('<td>Proposed</td>', '<td><span class="badge badge-proposed">Proposed</span></td>')
body = body.replace('<td>To Be Verified</td>', '<td><span class="badge badge-verify">To Be Verified</span></td>')
body = body.replace('<strong>Confirmed</strong>', '<span class="badge badge-confirmed">Confirmed</span>')
body = body.replace('<strong>Proposed</strong>', '<span class="badge badge-proposed">Proposed</span>')
body = body.replace('<strong>To Be Verified</strong>', '<span class="badge badge-verify">To Be Verified</span>')

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VELOOP Rewards — Internship Milestone: Days 1–2 Progress Report</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>mermaid.initialize({{startOnLoad:true, theme: 'neutral'}});</script>
<style>
  :root {{
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --slate-800: #1e293b;
    --slate-600: #475569;
    --slate-100: #f1f5f9;
    --slate-50: #f8fafc;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.65;
    color: #1e293b;
    background: #f1f5f9;
    margin: 0;
    padding: 30px 15px;
  }}
  .container {{
    max-width: 1000px;
    margin: 0 auto;
    background: #ffffff;
    padding: 50px 60px;
    border-radius: 12px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
  }}
  .header-banner {{
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 20px;
    margin-bottom: 30px;
  }}
  .badge-classification {{
    display: inline-block;
    background: #fef3c7;
    color: #92400e;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 4px 10px;
    border-radius: 9999px;
    margin-bottom: 12px;
    border: 1px solid #fde68a;
  }}
  h1 {{
    color: #0f172a;
    font-size: 26px;
    margin-top: 0;
    margin-bottom: 6px;
    font-weight: 800;
  }}
  h2 {{
    color: #1e293b;
    font-size: 20px;
    margin-top: 36px;
    margin-bottom: 14px;
    padding-bottom: 8px;
    border-bottom: 1px solid #e2e8f0;
  }}
  h3 {{
    color: #334155;
    font-size: 16px;
    margin-top: 24px;
    margin-bottom: 10px;
  }}
  p, li {{
    color: #334155;
    font-size: 14.5px;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 22px 0;
    font-size: 13px;
    border-radius: 6px;
    overflow: hidden;
  }}
  th, td {{
    border: 1px solid #cbd5e1;
    padding: 10px 14px;
    text-align: left;
    vertical-align: top;
  }}
  th {{
    background: #f8fafc;
    color: #0f172a;
    font-weight: 700;
  }}
  tr:nth-child(even) {{
    background: #f8fafc;
  }}
  code {{
    background: #f1f5f9;
    color: #0f172a;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 12.5px;
  }}
  pre {{
    background: #0f172a;
    color: #f8fafc;
    padding: 16px 20px;
    border-radius: 8px;
    overflow-x: auto;
  }}
  pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
  }}
  .badge {{
    display: inline-block;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
    white-space: nowrap;
  }}
  .badge-confirmed {{
    background: #dcfce7;
    color: #166534;
    border: 1px solid #bbf7d0;
  }}
  .badge-proposed {{
    background: #e0f2fe;
    color: #0369a1;
    border: 1px solid #bae6fd;
  }}
  .badge-verify {{
    background: #fee2e2;
    color: #991b1b;
    border: 1px solid #fecaca;
  }}
  .alert {{
    padding: 14px 18px;
    border-radius: 8px;
    margin: 20px 0;
    font-size: 13.5px;
  }}
  .alert-important {{
    background: #fffbeb;
    border-left: 4px solid #f59e0b;
    color: #92400e;
  }}
  .alert-note {{
    background: #eff6ff;
    border-left: 4px solid #3b82f6;
    color: #1e40af;
  }}
  .mermaid {{
    text-align: center;
    margin: 25px 0;
    background: #f8fafc;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
  }}
  .footer {{
    margin-top: 50px;
    padding-top: 20px;
    border-top: 1px solid #e2e8f0;
    font-size: 12px;
    color: #64748b;
    text-align: center;
  }}
  @media print {{
    body {{ background: #fff; padding: 0; }}
    .container {{ box-shadow: none; padding: 0; max-width: 100%; }}
    .mermaid {{ break-inside: avoid; }}
    table {{ break-inside: avoid; }}
  }}
</style>
</head>
<body>
<div class="container">
  <div class="header-banner">
    <div class="badge-classification">SIMULATED DATA — CREATED FOR ANALYTICAL TESTING</div>
    <h1>VELOOP REWARDS — DATA ANALYST INTERNSHIP</h1>
    <div style="font-size: 16px; font-weight: 600; color: #475569;">TASK 01 PROGRESS REPORT: DAYS 1–2 DELIVERABLES</div>
    <div style="font-size: 13px; color: #64748b; margin-top: 4px;">Schedule Reference: Section 31 (Product Documentation Review & Source & Verification Register)</div>
  </div>
  {body}
  <div class="footer">
    VELOOP Rewards Analytics Internship &bull; Task 01: Product Analytics & Data Readiness &bull; Days 1–2 Progress Submission
  </div>
</div>
</body>
</html>"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print("Generated VELOOP_DAY_1_2_SUBMISSION.html successfully!")
