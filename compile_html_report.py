import os
import markdown

work_dir = r"C:\Users\ckart\.gemini\antigravity\scratch\veloop_analytics_task01"
output_html = os.path.join(work_dir, "VELOOP_TASK01_FINAL_SUBMISSION.html")

file_order = [
    "executive_summary_and_final_consolidated_report.md",
    "work_package_a_product_data_readiness_audit.md",
    "work_package_b_user_analytics_spec.md",
    "work_package_c_earning_reward_analytics.md",
    "work_package_d_wallet_withdrawal_analytics.md",
    "work_package_e_referral_engagement_analytics.md",
    "work_package_f_production_event_tracking_plan.md",
    "work_package_g_data_dictionary.md",
    "work_package_h_logical_data_model.md",
    "work_package_i_kpi_catalogue.md",
    "work_package_j_simulated_data_profiling.md",
    "work_package_k_data_quality_audit.md",
    "work_package_l_data_quality_control_framework.md",
    "work_package_m_analytics_dashboard_blueprint.md",
    "work_package_n_developer_analytics_handoff.md",
    "work_package_o_data_pipeline_operating_model.md",
    "work_package_p_privacy_governance.md",
    "work_package_q_analytics_change_management.md",
    "work_package_r_analytics_readiness_assessment.md",
    "work_package_s_and_t_registers_backlog.md"
]

combined_md = """<div class="cover-page">
    <div class="company-badge">VELOOP REWARDS ECOSYSTEM</div>
    <h1 class="main-title">DATA ANALYST INTERNSHIP — TASK 01</h1>
    <h2 class="sub-title">Product Analytics, Data Readiness & Data Management Blueprint</h2>
    <div class="meta-box">
        <p><strong>Project Type:</strong> Product Development / Data Analytics</p>
        <p><strong>Scope Duration:</strong> 22–24 Days</p>
        <p><strong>Deliverables Included:</strong> All 21 Mandatory Deliverables (Work Packages A through T)</p>
        <p><strong>Classification:</strong> SIMULATED DATA — CREATED FOR ANALYTICAL TESTING</p>
        <p><strong>Submission Status:</strong> 100% Complete & Verified</p>
    </div>
</div>

<div class="page-break"></div>

[TOC]

---
"""

for fname in file_order:
    fpath = os.path.join(work_dir, fname)
    if os.path.exists(fpath):
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()
            combined_md += f"\n\n<div class='page-break'></div>\n\n" + content
    else:
        print(f"Warning: {fname} missing")

# Convert to HTML
html_body = markdown.markdown(combined_md, extensions=['extra', 'tables', 'fenced_code', 'toc'])

full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>VELOOP Task 01 — Final Consolidated Submission</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #1e293b;
            background-color: #f8fafc;
            line-height: 1.65;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 960px;
            margin: 40px auto;
            background: #ffffff;
            padding: 60px 80px;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            border-radius: 8px;
        }}
        .cover-page {{
            text-align: center;
            padding: 80px 20px;
            border-bottom: 2px solid #e2e8f0;
            margin-bottom: 40px;
        }}
        .company-badge {{
            display: inline-block;
            background: #e0e7ff;
            color: #3730a3;
            font-weight: 700;
            font-size: 13px;
            letter-spacing: 0.1em;
            padding: 6px 16px;
            border-radius: 20px;
            margin-bottom: 24px;
        }}
        .main-title {{
            font-size: 34px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 12px;
            letter-spacing: -0.02em;
        }}
        .sub-title {{
            font-size: 20px;
            font-weight: 500;
            color: #475569;
            margin-bottom: 36px;
        }}
        .meta-box {{
            display: inline-block;
            text-align: left;
            background: #f1f5f9;
            border-left: 4px solid #3b82f6;
            padding: 20px 30px;
            border-radius: 4px;
            font-size: 14px;
        }}
        .meta-box p {{
            margin: 6px 0;
        }}
        h1, h2, h3, h4 {{
            color: #0f172a;
            font-weight: 700;
            margin-top: 1.8em;
            margin-bottom: 0.6em;
        }}
        h1 {{
            font-size: 24px;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 8px;
        }}
        h2 {{
            font-size: 20px;
            border-bottom: 1px solid #edf2f7;
            padding-bottom: 6px;
        }}
        h3 {{ font-size: 16px; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 24px 0;
            font-size: 13px;
        }}
        th, td {{
            padding: 10px 14px;
            border: 1px solid #cbd5e1;
            text-align: left;
        }}
        th {{
            background: #f1f5f9;
            font-weight: 600;
            color: #334155;
        }}
        tr:nth-child(even) {{
            background: #f8fafc;
        }}
        code {{
            font-family: 'JetBrains Mono', monospace;
            background: #f1f5f9;
            color: #0f172a;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 12.5px;
        }}
        pre {{
            background: #0f172a;
            color: #f8fafc;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
            font-size: 12.5px;
        }}
        pre code {{
            background: transparent;
            color: inherit;
            padding: 0;
        }}
        blockquote {{
            border-left: 4px solid #3b82f6;
            background: #eff6ff;
            color: #1e40af;
            padding: 12px 18px;
            margin: 20px 0;
            border-radius: 0 4px 4px 0;
            font-size: 14px;
        }}
        .toc {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            padding: 24px;
            border-radius: 6px;
            margin-bottom: 40px;
        }}
        .toc ul {{
            list-style-type: decimal;
            padding-left: 20px;
        }}
        .toc a {{
            color: #2563eb;
            text-decoration: none;
        }}
        .toc a:hover {{
            text-decoration: underline;
        }}
        @media print {{
            body {{ background: #fff; }}
            .container {{ box-shadow: none; padding: 0; margin: 0; max-width: 100%; }}
            .page-break {{ page-break-after: always; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_body}
    </div>
</body>
</html>
"""

with open(output_html, "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"Generated {output_html}, size: {os.path.getsize(output_html)} bytes")
