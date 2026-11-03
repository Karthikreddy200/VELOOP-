import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Set Page Config
st.set_page_config(
    page_title="VELOOP Rewards — Analytics & Deployment Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 28px;
        font-weight: 800;
        color: #1E293B;
        margin-bottom: 4px;
    }
    .sub-header {
        font-size: 14px;
        color: #64748B;
        margin-bottom: 20px;
    }
    .badge-simulated {
        display: inline-block;
        background-color: #FEF3C7;
        color: #92400E;
        font-weight: 600;
        font-size: 12px;
        padding: 4px 12px;
        border-radius: 12px;
        border: 1px solid #F59E0B;
        margin-bottom: 12px;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Cache data loading
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    f1_path = os.path.join(base_dir, "data", "VELoop_Rewards_Data_01.xlsx")
    f2_path = os.path.join(base_dir, "data", "VELOOP_Simulated_User_Behavior_1000.xlsx")
    
    xl1 = pd.ExcelFile(f1_path)
    xl2 = pd.ExcelFile(f2_path)
    
    users_clean = xl1.parse('Users_1000_Clean')
    users_messy = xl1.parse('Users_Messy_Audit')
    
    sessions = xl2.parse('02_Sessions')
    events = xl2.parse('03_Feature_Events')
    daily = xl2.parse('04_Daily_Activity')
    tasks = xl2.parse('05_Task_Activity')
    feature_usage = xl2.parse('07_Feature_Usage')
    events_messy = xl2.parse('10_Event_Data_Quality_Audit')
    
    # Preprocessing
    daily['activity_date'] = pd.to_datetime(daily['activity_date'])
    events['event_datetime'] = pd.to_datetime(events['event_datetime'])
    users_clean['registration_datetime'] = pd.to_datetime(users_clean['registration_datetime'])
    
    # Task duration calculation
    tasks['task_completed_at'] = pd.to_datetime(tasks['task_completed_at'])
    tasks['task_started_at'] = pd.to_datetime(tasks['task_started_at'])
    tasks['task_viewed_at'] = pd.to_datetime(tasks['task_viewed_at'])
    tasks['duration_seconds'] = (tasks['task_completed_at'] - tasks['task_started_at']).dt.total_seconds()
    tasks['duration_seconds'] = tasks['duration_seconds'].fillna((tasks['task_completed_at'] - tasks['task_viewed_at']).dt.total_seconds())
    
    return {
        "users_clean": users_clean,
        "users_messy": users_messy,
        "sessions": sessions,
        "events": events,
        "daily": daily,
        "tasks": tasks,
        "feature_usage": feature_usage,
        "events_messy": events_messy
    }

data = load_data()

# Sidebar Navigation
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135706.png", width=60)
st.sidebar.title("VELOOP Analytics")
st.sidebar.markdown("**Task 01: Live Interactive Platform**")

menu = st.sidebar.radio(
    "Select Exploration View:",
    [
        "📋 1. Days 1–2: Product Spec & Source Register",
        "📊 2. Executive Cockpit",
        "👥 3. User Lifecycle & Growth",
        "🎯 4. Task & Feature Engagement",
        "🔍 5. Data Quality Forensic Audit",
        "💰 6. Live Wallet & Payout Simulator"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Data Authenticity Policy:**  
All metrics are computed from the simulated internship dataset.  
`SIMULATED DATA — CREATED FOR ANALYTICAL TESTING`
""")

# ==========================================
# VIEW 1: DAYS 1–2: PRODUCT SPEC & SOURCE REGISTER
# ==========================================
if menu == "📋 1. Days 1–2: Product Spec & Source Register":
    st.markdown('<div class="badge-simulated">SIMULATED DATA — CREATED FOR ANALYTICAL TESTING</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-header">Days 1–2: Product Documentation Review & Source Register</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Systematic review across 15 features, evidence discipline, and technical ambiguity verification.</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Documented Modules", "15 Features", "100% Scoped")
    with col2:
        st.metric("Cataloged Items", "26 Items", "Sections 6 & 25")
    with col3:
        st.metric("Confirmed Facts", "11 Items", "Verified in Data")
    with col4:
        st.metric("Proposed Designs", "8 Items", "Analyst Models")
    with col5:
        st.metric("To Be Verified", "7 Items", "Requires Eng. Sign-off")
        
    tab1, tab2, tab3, tab4 = st.tabs([
        "📱 15 Functional Modules", 
        "📑 Source & Verification Register", 
        "⚖️ Facts vs. Assumptions (Sec 6)", 
        "❓ Engineering Discovery Backlog"
    ])
    
    with tab1:
        st.subheader("Comprehensive Review of the 15 Functional Modules")
        st.markdown("Every product feature identified in the VELOOP specification was audited against existing dataset evidence:")
        
        modules_data = [
            {"#": "01", "Module": "User Accounts & Auth", "Category": "Core Auth", "Action": "User registers / logs in", "Dataset Evidence": "Users_1000_Clean (1,000 users)", "Status": "Confirmed"},
            {"#": "02", "Module": "Watch Ads", "Category": "Earning", "Action": "Watches 30s rewarded video", "Dataset Evidence": "03_Feature_Events ('Watch Ads')", "Status": "Confirmed"},
            {"#": "03", "Module": "Tap & Earn", "Category": "Earning", "Action": "High-frequency canvas tapping", "Dataset Evidence": "03_Feature_Events ('Tap & Earn')", "Status": "Confirmed"},
            {"#": "04", "Module": "Mining Rewards", "Category": "Earning", "Action": "Starts passive yield timer", "Dataset Evidence": "03_Feature_Events ('Mining Rewards')", "Status": "Confirmed"},
            {"#": "05", "Module": "Missions & Tasks", "Category": "Earning", "Action": "Completes multi-step challenges", "Dataset Evidence": "05_Task_Activity (9,846 records)", "Status": "Confirmed"},
            {"#": "06", "Module": "Follow & Earn", "Category": "Earning", "Action": "Follows social media account", "Dataset Evidence": "03_Feature_Events ('Follow & Earn')", "Status": "Confirmed"},
            {"#": "07", "Module": "Spin the Wheel", "Category": "Gamification", "Action": "Executes daily RNG spin", "Dataset Evidence": "03_Feature_Events ('Spin the Wheel')", "Status": "Confirmed"},
            {"#": "08", "Module": "Daily Rewards", "Category": "Gamification", "Action": "Claims consecutive daily reward", "Dataset Evidence": "03_Feature_Events ('Daily Rewards')", "Status": "Confirmed"},
            {"#": "09", "Module": "Streak Rewards", "Category": "Gamification", "Action": "Maintains daily habit streak", "Dataset Evidence": "Users_1000_Clean ('streak_days')", "Status": "Confirmed"},
            {"#": "10", "Module": "Badges & Levels", "Category": "Gamification", "Action": "Accumulates XP to tier up", "Dataset Evidence": "Users_1000_Clean ('level', 'badges')", "Status": "Confirmed"},
            {"#": "11", "Module": "CAPTCHA Security", "Category": "Security", "Action": "Solves anti-bot challenge", "Dataset Evidence": "03_Feature_Events ('CAPTCHA')", "Status": "Confirmed"},
            {"#": "12", "Module": "Wallet & Ledger", "Category": "Financial", "Action": "Views XP/Gem/Token balance", "Dataset Evidence": "Users_1000_Clean (Static balances)", "Status": "Confirmed"},
            {"#": "13", "Module": "Exchange Center", "Category": "Financial", "Action": "Swaps XP for convertible Tokens", "Dataset Evidence": "03_Feature_Events ('Exchange Center')", "Status": "Confirmed"},
            {"#": "14", "Module": "Withdrawals & Payouts", "Category": "Financial", "Action": "Requests external cash-out", "Dataset Evidence": "Absent from data; proposed state machine", "Status": "Proposed"},
            {"#": "15", "Module": "Referral Engine", "Category": "Growth", "Action": "Invites friends via custom code", "Dataset Evidence": "Users_1000_Clean ('referred_by')", "Status": "Confirmed"}
        ]
        df_mod = pd.DataFrame(modules_data)
        
        cat_filter = st.selectbox("Filter Modules by Category:", ["All", "Core Auth", "Earning", "Gamification", "Financial", "Security", "Growth"])
        if cat_filter != "All":
            df_mod = df_mod[df_mod['Category'] == cat_filter]
        st.dataframe(df_mod, use_container_width=True, hide_index=True)
        
    with tab2:
        st.subheader("Official Source & Verification Register (Deliverable 21a)")
        st.markdown("Cataloging every technical capability into **Confirmed**, **Proposed**, or **To Be Verified** in strict compliance with Section 6 & 25:")
        
        svr_data = [
            {"ID": "SVR-001", "Information Found": "15 distinct feature events tracked in telemetry stream", "Source": "03_Feature_Events", "Type": "Simulated", "Status": "Confirmed", "Notes": "Watch Ads, Tap & Earn, Mining, Missions, etc."},
            {"ID": "SVR-002", "Information Found": "User balances stored as mutable scalar numbers without ledger", "Source": "Users_1000_Clean", "Type": "Simulated", "Status": "Confirmed", "Notes": "Critical financial risk; missing double-entry ledger."},
            {"ID": "SVR-003", "Information Found": "9,846 task activities tracked with completion duration", "Source": "05_Task_Activity", "Type": "Simulated", "Status": "Confirmed", "Notes": "Task payout amount is omitted in raw events."},
            {"ID": "SVR-004", "Information Found": "7,913 session records logged with start/end timestamps", "Source": "02_Sessions", "Type": "Simulated", "Status": "Confirmed", "Notes": "Session ID not propagated to feature events."},
            {"ID": "SVR-005", "Information Found": "Profile data contains duplicates, negative balances, future dates", "Source": "Users_Messy_Audit", "Type": "Simulated", "Status": "Confirmed", "Notes": "14 duplicate IDs, 18 negative balances discovered."},
            {"ID": "SVR-006", "Information Found": "Feature event names contain inconsistent casing and whitespace", "Source": "10_Event_Data_Quality_Audit", "Type": "Simulated", "Status": "Confirmed", "Notes": "'watch ads', 'WATCH ADS', 'Watch Ads '."},
            {"ID": "SVR-007", "Information Found": "Referral relationship stored as single referred_by string", "Source": "Users_1000_Clean", "Type": "Simulated", "Status": "Confirmed", "Notes": "Missing activation milestone and commission link."},
            {"ID": "SVR-008", "Information Found": "Withdrawal requests and settlement logs completely missing", "Source": "Full Dataset Review", "Type": "Simulated", "Status": "Confirmed", "Notes": "#1 Critical business gap for platform liquidity."},
            {"ID": "SVR-009", "Information Found": "Three virtual currencies exist: Points (XP), Gems, and Tokens", "Source": "Product Context Brief", "Type": "Official", "Status": "Confirmed", "Notes": "XP = micro-earning, Gems = gamification, Tokens = redemption."},
            {"ID": "SVR-010", "Information Found": "Double-entry ledger (fact_wallet_transactions) required", "Source": "Specification Sec 10", "Type": "Official", "Status": "Proposed", "Notes": "Enforces running_balance_after reconciliation."},
            {"ID": "SVR-011", "Information Found": "6-stage finite state machine for withdrawal processing", "Source": "Specification Sec 10", "Type": "Official", "Status": "Proposed", "Notes": "Requested -> Review -> Processing -> Completed/Rejected."},
            {"ID": "SVR-012", "Information Found": "UUIDv4 idempotency_key on client event mutation payloads", "Source": "Analytics Architecture", "Type": "Internal", "Status": "Proposed", "Notes": "Prevents network retry double-crediting."},
            {"ID": "SVR-013", "Information Found": "Relational referral attribution bridge (fact_referral_conversions)", "Source": "Growth Spec Sec 11", "Type": "Official", "Status": "Proposed", "Notes": "Tracks Registered -> Activated -> Monetized funnel."},
            {"ID": "SVR-014", "Information Found": "SHA-256 PII masking for user email in analytical lake", "Source": "Governance Sec 22", "Type": "Official", "Status": "Proposed", "Notes": "GDPR and DPDP Act compliance."},
            {"ID": "SVR-015", "Information Found": "Unified Event Tracking Plan standardizing 28 production events", "Source": "Tracking Plan Sec 12", "Type": "Official", "Status": "Proposed", "Notes": "Typed JSON schema with payload validators."},
            {"ID": "SVR-016", "Information Found": "DAU defined by explicit user actions, not background pings", "Source": "KPI Catalogue Sec 15", "Type": "Official", "Status": "Proposed", "Notes": "Eliminates push notification refresh inflation."},
            {"ID": "SVR-017", "Information Found": "Backend service emits real-time events vs direct SQL writes", "Source": "Core Architecture", "Type": "Internal", "Status": "To Be Verified", "Notes": "Determines CDC vs Pub/Sub pipeline requirements."},
            {"ID": "SVR-018", "Information Found": "Mobile JWT session expiration timeout window", "Source": "API Specs", "Type": "Internal", "Status": "To Be Verified", "Notes": "Defines sessionization boundary parameters."},
            {"ID": "SVR-019", "Information Found": "Ad network postbacks verified via cryptographic HMAC SHA-256", "Source": "Ad Partner Docs", "Type": "External", "Status": "To Be Verified", "Notes": "Critical security defense against spoofed completions."},
            {"ID": "SVR-020", "Information Found": "Payment gateway automated webhook retries on failed delivery", "Source": "Gateway Docs", "Type": "External", "Status": "To Be Verified", "Notes": "Dictates auto-requeue vs manual ops intervention."},
            {"ID": "SVR-021", "Information Found": "Database automated archival or retention purging policies", "Source": "DBA Policy", "Type": "Internal", "Status": "To Be Verified", "Notes": "Determines raw event lake independence."},
            {"ID": "SVR-022", "Information Found": "Device fingerprinting and MAC hashing at signup", "Source": "Fraud Docs", "Type": "Internal", "Status": "To Be Verified", "Notes": "Prevents emulator farm multi-accounting."},
            {"ID": "SVR-023", "Information Found": "CAPTCHA failure logs retained for supervised ML training", "Source": "Security Docs", "Type": "Internal", "Status": "To Be Verified", "Notes": "Required for bot attack detection."},
            {"ID": "SVR-024", "Information Found": "Dynamic exchange rate configuration supported in backend", "Source": "Tokenomics Engine", "Type": "Internal", "Status": "To Be Verified", "Notes": "Allows dynamic margin protection against eCPM drops."},
            {"ID": "SVR-025", "Information Found": "Database PRIMARY KEY and UNIQUE constraints enforced on IDs", "Source": "Production DDL", "Type": "Internal", "Status": "To Be Verified", "Notes": "Audit found 14 duplicates in simulated logs."},
            {"ID": "SVR-026", "Information Found": "Client IP addresses preserved at gateway load balancer", "Source": "DevOps Config", "Type": "Internal", "Status": "To Be Verified", "Notes": "Determines GeoIP warehouse enrichment feasibility."}
        ]
        df_svr = pd.DataFrame(svr_data)
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            status_filter = st.selectbox("Filter by Verification Status:", ["All", "Confirmed", "Proposed", "To Be Verified"])
        with col_f2:
            search_query = st.text_input("Search Register:", "")
            
        if status_filter != "All":
            df_svr = df_svr[df_svr['Status'] == status_filter]
        if search_query:
            df_svr = df_svr[df_svr['Information Found'].str.contains(search_query, case=False, na=False) | df_svr['Notes'].str.contains(search_query, case=False, na=False)]
            
        st.dataframe(df_svr, use_container_width=True, hide_index=True)
        
    with tab3:
        st.subheader("Source & Evidence Discipline: Facts vs. Assumptions (Section 6)")
        st.warning("⚠️ **Strict Rule:** The analyst must not silently convert assumptions into facts. Every technical capability must be grounded in verified evidence.")
        
        comp_data = [
            {
                "Operational Area": "Session Identifiers",
                "❌ Incorrect (Silent Assumption)": "VELOOP currently stores a unique session ID for every active user interaction.",
                "✅ Correct (Professional Data Analyst)": "A session identifier is proposed as an essential analytics field. Current implementation requires engineering verification.",
                "Verification Path": "Inspect Mobile SDK network headers and client telemetry dispatcher."
            },
            {
                "Operational Area": "Wallet Ledger",
                "❌ Incorrect (Silent Assumption)": "User wallet balances in the database are fully backed by an immutable transaction ledger.",
                "✅ Correct (Professional Data Analyst)": "Simulated data contains static balance fields without ledger transactions. A double-entry ledger (fact_wallet_transactions) is proposed.",
                "Verification Path": "Review production PostgreSQL/MySQL schema DDL and wallet mutation endpoints."
            },
            {
                "Operational Area": "Withdrawal Processing",
                "❌ Incorrect (Silent Assumption)": "Withdrawal requests are processed automatically within 24 hours via integrated payment gateways.",
                "✅ Correct (Professional Data Analyst)": "Withdrawal data is entirely absent from available datasets. A 6-stage withdrawal state machine is proposed, pending gateway API verification.",
                "Verification Path": "Inspect Payment Gateway API credentials, webhook listeners, and finance review policies."
            },
            {
                "Operational Area": "Ad Network Postbacks",
                "❌ Incorrect (Silent Assumption)": "Ad rewards are only credited after verified third-party completion postbacks from AdMob.",
                "✅ Correct (Professional Data Analyst)": "Simulated events record ad completions without callback IDs. Verification is required to determine whether rewards issue on client triggers or server postbacks.",
                "Verification Path": "Inspect ad integration SDK, server-side callback endpoints, and HMAC validation."
            }
        ]
        st.table(pd.DataFrame(comp_data))
        
    with tab4:
        st.subheader("Engineering Discovery Backlog (Work Package S)")
        st.markdown("Actionable technical discovery questions structured by engineering owner:")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 1. Lead Backend Engineer")
            st.info("""
            * **Q-B1 (Event Pipeline):** Does the backend emit real-time event payloads to Pub/Sub/Kafka, or does analytics require a CDC connector?
            * **Q-B2 (Database Constraints):** Are `PRIMARY KEY` and `UNIQUE` constraints actively enforced in production SQL DDL?
            * **Q-B3 (Atomic Transactions):** Does the backend enforce ACID transactions on XP-to-Token exchange conversions?
            """)
            st.markdown("#### 2. Platform & Security Architect")
            st.info("""
            * **Q-S1 (Ad Postbacks):** Are AdMob/Unity rewarded video callbacks cryptographically verified with HMAC SHA-256?
            * **Q-S2 (Device Fingerprinting):** Does the mobile app capture hardware hashes/IDFV to detect emulator bot farms?
            * **Q-S3 (CAPTCHA Logs):** Are CAPTCHA challenge failure logs and latencies stored for fraud detection model training?
            """)
        with c2:
            st.markdown("#### 3. Payments & Gateway Lead")
            st.info("""
            * **Q-P1 (Payout Webhooks):** When external payouts fail, does the payment gateway dispatch automated webhook callbacks?
            * **Q-P2 (Manual Review Gates):** Is there an admin review gate for high-value withdrawal requests before dispatch?
            """)
            st.markdown("#### 4. DevOps & Infrastructure Lead")
            st.info("""
            * **Q-D1 (IP Preservation):** Are raw user IPs preserved via `X-Forwarded-For` or stripped at the reverse proxy?
            * **Q-D2 (Data Retention):** What is the transactional database retention lifecycle before archival?
            """)

# ==========================================
# VIEW 2: EXECUTIVE COCKPIT
# ==========================================
elif menu == "📊 2. Executive Cockpit":
    st.markdown('<div class="badge-simulated">SIMULATED DATA — CREATED FOR ANALYTICAL TESTING</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-header">Executive Overview Cockpit</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Macro platform performance, audience scale, and operational health.</div>', unsafe_allow_html=True)
    
    # Metric KPI Scorecards
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Acquired Users", f"{len(data['users_clean']):,}", "100% Retained")
    with col2:
        st.metric("Total Sessions", f"{len(data['sessions']):,}", "1.14 / day avg")
    with col3:
        st.metric("Telemetry Events", f"{len(data['events']):,}", "15 Features")
    with col4:
        completed_tasks = (data['tasks']['task_status'] == 'Completed').sum()
        st.metric("Completed Tasks", f"{completed_tasks:,}", f"{(completed_tasks/len(data['tasks'])*100):.1f}% TCR")
    with col5:
        total_xp = data['users_clean']['xp_balance'].sum()
        st.metric("Total XP In Circulation", f"{total_xp:,.0f} XP", "$ Liability")
        
    st.markdown("---")
    
    # Visual Row 1: Daily Trend & Feature Distribution
    col_left, col_right = st.columns([6, 4])
    
    with col_left:
        st.subheader("Daily Active Engagement Volume")
        daily_trend = data['daily'].groupby('activity_date')['user_id'].nunique().reset_index()
        daily_trend.columns = ['activity_date', 'active_users']
        fig_trend = px.line(daily_trend, x='activity_date', y='active_users', 
                            title="Daily Active Users (Simulated 30-Day Window)",
                            markers=True, line_shape="spline", color_discrete_sequence=["#2563EB"])
        fig_trend.update_layout(template="plotly_white", xaxis_title="Date", yaxis_title="Active Users")
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_right:
        st.subheader("Feature Activity Share")
        top_features = data['events']['feature_name'].value_counts().head(8).reset_index()
        top_features.columns = ['feature_name', 'total_events']
        fig_feats = px.bar(top_features, x='total_events', y='feature_name', orientation='h',
                           title="Top 8 Features by Interaction Count",
                           labels={'total_events': 'Logged Events', 'feature_name': 'Feature'},
                           color='total_events', color_continuous_scale="Blues")
        fig_feats.update_layout(template="plotly_white", coloraxis_showscale=False)
        st.plotly_chart(fig_feats, use_container_width=True)

# ==========================================
# VIEW 3: USER LIFECYCLE & GROWTH
# ==========================================
elif menu == "👥 3. User Lifecycle & Growth":
    st.markdown('<div class="badge-simulated">SIMULATED DATA — CREATED FOR ANALYTICAL TESTING</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-header">User Lifecycle, Acquisition & Cohort Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Customer acquisition channel mix, demographic distributions, and account statuses.</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Customer Acquisition by Channel")
        channel_df = data['users_clean']['acquisition_source'].value_counts().reset_index()
        channel_df.columns = ['Channel', 'User Count']
        fig_chan = px.pie(channel_df, values='User Count', names='Channel', hole=0.4,
                          color_discrete_sequence=px.colors.qualitative.Prism,
                          title="Acquisition Channel Distribution")
        st.plotly_chart(fig_chan, use_container_width=True)
        
    with col2:
        st.subheader("Account Lifecycle Status Distribution")
        status_df = data['users_clean']['account_status'].value_counts().reset_index()
        status_df.columns = ['Status', 'Count']
        fig_stat = px.bar(status_df, x='Status', y='Count', color='Status',
                          color_discrete_map={
                              'Active': '#10B981',
                              'Inactive': '#6B7280',
                              'Pending Verification': '#F59E0B',
                              'Suspended': '#EF4444'
                          },
                          title="Account Status Breakdown")
        fig_stat.update_layout(template="plotly_white", showlegend=False)
        st.plotly_chart(fig_stat, use_container_width=True)
        
    st.subheader("User Age & Demographic Profile")
    col_demo1, col_demo2 = st.columns(2)
    with col_demo1:
        fig_age = px.histogram(data['users_clean'], x='age', nbins=15,
                               title="User Age Distribution (Range: 18 - 55)",
                               color_discrete_sequence=['#6366F1'])
        fig_age.update_layout(template="plotly_white")
        st.plotly_chart(fig_age, use_container_width=True)
    with col_demo2:
        top_states = data['users_clean']['state'].value_counts().head(10).reset_index()
        top_states.columns = ['State', 'Users']
        fig_state = px.bar(top_states, x='Users', y='State', orientation='h',
                           title="Top 10 Geographic States",
                           color='Users', color_continuous_scale="Purples")
        fig_state.update_layout(template="plotly_white", yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_state, use_container_width=True)

# ==========================================
# VIEW 4: TASK & FEATURE ENGAGEMENT
# ==========================================
elif menu == "🎯 4. Task & Feature Engagement":
    st.markdown('<div class="badge-simulated">SIMULATED DATA — CREATED FOR ANALYTICAL TESTING</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-header">Task Earning & Feature Engagement Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Evaluating micro-task completion funnels, conversion rates, and friction points.</div>', unsafe_allow_html=True)
    
    # Filter by task category
    categories = ["All"] + list(data['tasks']['task_category'].unique())
    selected_cat = st.selectbox("Filter by Task Category:", categories)
    
    filtered_tasks = data['tasks'] if selected_cat == "All" else data['tasks'][data['tasks']['task_category'] == selected_cat]
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Task Completion Status Distribution")
        task_status_df = filtered_tasks['task_status'].value_counts().reset_index()
        task_status_df.columns = ['Status', 'Count']
        fig_ts = px.bar(task_status_df, x='Status', y='Count', color='Status',
                        color_discrete_map={
                            'Completed': '#10B981',
                            'In Progress': '#3B82F6',
                            'Abandoned': '#EF4444',
                            'Failed': '#F59E0B'
                        },
                        title=f"Task Completion Breakdown ({selected_cat})")
        fig_ts.update_layout(template="plotly_white")
        st.plotly_chart(fig_ts, use_container_width=True)
        
    with col2:
        st.subheader("Completion Time (Seconds) by Category")
        completed_tasks_duration = data['tasks'].dropna(subset=['duration_seconds'])
        fig_box = px.box(completed_tasks_duration, x='task_category', y='duration_seconds', 
                         color='task_category', title="Task Duration Spread (Friction Analysis - Completed Tasks)")
        fig_box.update_layout(template="plotly_white", showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)
        
    st.subheader("Hourly Feature Engagement Heatmap")
    events_copy = data['events'].copy()
    events_copy['hour'] = events_copy['event_datetime'].dt.hour
    hourly_counts = events_copy.groupby(['hour', 'feature_name']).size().reset_index(name='event_count')
    fig_heat = px.density_heatmap(hourly_counts, x='hour', y='feature_name', z='event_count',
                                  title="Engagement Density Across 24-Hour Day",
                                  color_continuous_scale="Viridis")
    fig_heat.update_layout(template="plotly_white")
    st.plotly_chart(fig_heat, use_container_width=True)

# ==========================================
# VIEW 5: DATA QUALITY FORENSIC AUDIT
# ==========================================
elif menu == "🔍 5. Data Quality Forensic Audit":
    st.markdown('<div class="badge-simulated">SIMULATED DATA — CREATED FOR ANALYTICAL TESTING</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-header">Data Quality Forensic Audit & Cleaning Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Evaluating messy simulated telemetry, duplicate primary keys, casing issues, and dirty data.</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🔴 Dirty Data Profiler", "📋 Issue Severity Matrix", "🧹 Live Cleaning Pipeline"])
    
    messy_u = data['users_messy']
    messy_e = data['events_messy']
    
    with tab1:
        st.subheader("Detected Anomalies in Raw Ingestion Tables")
        c1, c2, c3, c4 = st.columns(4)
        
        dup_users = messy_u['user_id'].duplicated().sum()
        null_reg = messy_u['registration_datetime'].isnull().sum()
        dup_events = messy_e['event_id'].duplicated().sum()
        bad_casing = messy_e['feature_name'].str.islower().sum()
        
        with c1:
            st.metric("Duplicate User IDs", f"{dup_users}", "High Risk", delta_color="inverse")
        with c2:
            st.metric("Missing Reg Dates", f"{null_reg}", "Schema Violation", delta_color="inverse")
        with c3:
            st.metric("Duplicate Event IDs", f"{dup_events}", "Cartesian Fan-out", delta_color="inverse")
        with c4:
            st.metric("Unsanitized Strings", f"{bad_casing}", "Dirty Casing", delta_color="inverse")
            
        st.markdown("#### Sample Dirty Telemetry Events")
        st.dataframe(messy_e.head(8), use_container_width=True)
        
    with tab2:
        st.subheader("Data Quality Issue Log (from Work Package K)")
        issues = pd.DataFrame([
            {"Issue ID": "DQI-01", "Table": "Users_Messy_Audit", "Column": "user_id", "Nature": "Duplicate primary keys (14 duplicates)", "Severity": "Critical", "Fix": "Deduplicate keep first; enforce UNIQUE index"},
            {"Issue ID": "DQI-02", "Table": "Users_Messy_Audit", "Column": "registration_datetime", "Nature": "Future dates (2027/2028) & nulls", "Severity": "High", "Fix": "Set future dates to ingestion timestamp"},
            {"Issue ID": "DQI-03", "Table": "Event_Audit", "Column": "feature_name", "Nature": "Inconsistent casing ('watch ads' vs 'Watch Ads')", "Severity": "High", "Fix": "Pre-emission SDK trim and Title Case enforcement"},
            {"Issue ID": "DQI-04", "Table": "Event_Audit", "Column": "event_status", "Nature": "Whitespace padding (' Completed ')", "Severity": "Medium", "Fix": "TRIM() SQL function in bronze dbt model"},
            {"Issue ID": "DQI-05", "Table": "Users_Messy_Audit", "Column": "xp_balance", "Nature": "Negative point balances (-50 to -500)", "Severity": "Critical", "Fix": "Ledger constraint: balance >= 0"}
        ])
        st.dataframe(issues, use_container_width=True, hide_index=True)
        
    with tab3:
        st.markdown("### Interactive Shift-Left Cleaning Engine")
        st.markdown("Click the button below to execute the automated data-cleaning transformations live:")
        if st.button("🚀 Run Shift-Left Data Cleaner"):
            # 1. Clean Users
            cleaned_users = messy_u.drop_duplicates(subset=['user_id'], keep='first').copy()
            cleaned_users['registration_datetime'] = cleaned_users['registration_datetime'].fillna(pd.to_datetime('2026-04-12 00:00:00'))
            
            # 2. Clean Events
            cleaned_events = messy_e.drop_duplicates(subset=['event_id'], keep='first').copy()
            cleaned_events['feature_name'] = cleaned_events['feature_name'].str.title()
            cleaned_events['event_status'] = cleaned_events['event_status'].str.strip().str.title()
            
            st.success("✅ **Cleaning Pipeline Executed Successfully!**")
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Users Table Results:**")
                st.write(f"- Starting rows: {len(messy_u)}")
                st.write(f"- Cleaned unique rows: {len(cleaned_users)}")
                st.write(f"- Remaining duplicate IDs: {cleaned_users['user_id'].duplicated().sum()}")
                st.write(f"- Remaining null registration dates: {cleaned_users['registration_datetime'].isnull().sum()}")
            with c2:
                st.write("**Events Table Results:**")
                st.write(f"- Starting rows: {len(messy_e)}")
                st.write(f"- Cleaned unique rows: {len(cleaned_events)}")
                st.write(f"- Inconsistent casing resolved: Yes (Standardized to Title Case)")
                st.write(f"- Status values after trim: `{list(cleaned_events['event_status'].unique())}`")

# ==========================================
# VIEW 6: LIVE WALLET & PAYOUT SIMULATOR
# ==========================================
elif menu == "💰 6. Live Wallet & Payout Simulator":
    st.markdown('<div class="badge-simulated">SIMULATED DATA — CREATED FOR ANALYTICAL TESTING</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-header">Double-Entry Wallet & Withdrawal Simulator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Interactive demonstration of the proposed Work Package D financial ledger.</div>', unsafe_allow_html=True)
    
    st.info("💡 **Why this simulator exists:** The simulated dataset omitted the financial ledger. This tool demonstrates how the proposed `fact_wallet_transactions` and `fact_withdrawals` models operate in production.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Simulate User Earning Action")
        selected_user = st.selectbox("Select User:", data['users_clean']['user_id'].head(10))
        current_xp = data['users_clean'].loc[data['users_clean']['user_id'] == selected_user, 'xp_balance'].values[0]
        st.write(f"**Current Verified XP Balance:** `{current_xp} XP`")
        
        earn_activity = st.selectbox("Select Earning Task:", ["Watch 30s Ad (+50 XP)", "Complete High-Value Survey (+200 XP)", "Claim Day-7 Streak Bonus (+100 XP)"])
        earn_amount = 50 if "50" in earn_activity else (200 if "200" in earn_activity else 100)
        
        if st.button("💰 Commit Reward Credit to Ledger"):
            new_xp = current_xp + earn_amount
            st.success(f"Atomic Ledger Commit: Added {earn_amount} XP!")
            st.json({
                "transaction_id": "tx_wall_sim_99014",
                "user_id": selected_user,
                "type": "REWARD_CREDIT",
                "direction": "CREDIT",
                "amount": earn_amount,
                "currency_unit": "XP",
                "running_balance_after": new_xp,
                "status": "COMPLETED"
            })
            
    with col2:
        st.subheader("2. Simulate Cash-Out Withdrawal")
        withdraw_amount = st.number_input("Requested Payout Amount ($ USD):", min_value=5.0, max_value=100.0, value=10.0, step=5.0)
        payout_method = st.selectbox("Payout Rail:", ["PayPal", "Bank Transfer (ACH)", "UPI Instant", "Crypto USDT"])
        
        if st.button("🚀 Submit Withdrawal Request"):
            st.warning("State: REQUESTED -> Escrow balance hold placed.")
            st.success(f"Gateway Handshake: Dispatched ${withdraw_amount:.2f} via {payout_method}!")
            st.json({
                "withdrawal_id": "WD_SIM_88102",
                "user_id": selected_user,
                "amount": withdraw_amount,
                "currency": "USD",
                "tokens_debited": withdraw_amount * 10,
                "method": payout_method,
                "status": "COMPLETED",
                "settlement_latency_sec": 1.4,
                "reconciliation_variance": 0.0000
            })
