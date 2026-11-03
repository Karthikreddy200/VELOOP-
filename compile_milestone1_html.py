import markdown
import os

md_path = r"C:\Users\ckart\.gemini\antigravity\scratch\veloop_analytics_task01\VELOOP_DAYS_1_TO_4_PROGRESS_SUBMISSION.md"
html_path = r"C:\Users\ckart\.gemini\antigravity\scratch\veloop_analytics_task01\VELOOP_DAYS_1_TO_4_PROGRESS_SUBMISSION.html"

with open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

body = markdown.markdown(text, extensions=['extra', 'tables', 'fenced_code'])

full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>VELOOP Milestone 1 (Days 1-4) Progress Report</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #1e293b; background: #f8fafc; padding: 40px; }}
.container {{ max-width: 920px; margin: auto; background: #fff; padding: 40px 60px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
h1, h2, h3 {{ color: #0f172a; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; }}
table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 13px; }}
th, td {{ border: 1px solid #cbd5e1; padding: 9px 12px; text-align: left; }}
th {{ background: #f1f5f9; color: #334155; }}
tr:nth-child(even) {{ background: #f8fafc; }}
code {{ background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 12px; }}
@media print {{ body {{ background: #fff; padding: 0; }} .container {{ box-shadow: none; padding: 0; }} }}
</style>
</head>
<body>
<div class="container">
{body}
</div>
</body>
</html>"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print("Generated Milestone 1 HTML report successfully!")
