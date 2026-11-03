import pandas as pd
import numpy as np

file1 = r"C:\Users\ckart\.gemini\antigravity\scratch\veloop_analytics_task01\data\VELoop_Rewards_Data_01.xlsx"
file2 = r"C:\Users\ckart\.gemini\antigravity\scratch\veloop_analytics_task01\data\VELOOP_Simulated_User_Behavior_1000.xlsx"

print("="*60)
print("RUNNING AUTOMATED PROFILING & AUDIT (WORK PACKAGES J & K)")
print("="*60)

xl1 = pd.ExcelFile(file1)
xl2 = pd.ExcelFile(file2)

# J1: Profile all sheets in File 1 & File 2
all_dfs = {}
for s in xl1.sheet_names:
    all_dfs[f"F1_{s}"] = xl1.parse(s)
for s in xl2.sheet_names:
    all_dfs[f"F2_{s}"] = xl2.parse(s)

print("\n--- J1. DATASET PROFILES ---")
for name, df in all_dfs.items():
    print(f"\nDataset: {name}")
    print(f"  Rows: {len(df)}, Cols: {len(df.columns)}")
    print(f"  Missing total: {df.isnull().sum().sum()}")
    date_cols = [c for c in df.columns if 'date' in c.lower() or 'time' in c.lower() or 'at' in c.lower()]
    for dc in date_cols:
        try:
            s_dt = pd.to_datetime(df[dc].dropna())
            print(f"  Date col '{dc}' range: {s_dt.min()} to {s_dt.max()}")
        except Exception:
            pass

# J2: Test Relationships (Referential Integrity)
users_clean = all_dfs["F1_Users_1000_Clean"]
user_ids_clean = set(users_clean['user_id'].dropna())

users_b = all_dfs["F2_01_Users_1000"]
user_ids_b = set(users_b['user_id'].dropna())

sessions = all_dfs["F2_02_Sessions"]
events = all_dfs["F2_03_Feature_Events"]
daily = all_dfs["F2_04_Daily_Activity"]
tasks = all_dfs["F2_05_Task_Activity"]
milestones = all_dfs["F2_06_Milestones"]

print("\n--- J2. REFERENTIAL INTEGRITY (RELATIONSHIP TESTS) ---")
print("User IDs in Clean Users:", len(user_ids_clean))
print("User IDs in File 2 Users:", len(user_ids_b))
print("Overlap between File 1 Users & File 2 Users:", len(user_ids_clean.intersection(user_ids_b)))

print("Orphan check Sessions.user_id in Users:", len(set(sessions['user_id']) - user_ids_b))
print("Orphan check Feature_Events.user_id in Users:", len(set(events['user_id']) - user_ids_b))
print("Orphan check Daily_Activity.user_id in Users:", len(set(daily['user_id']) - user_ids_b))
print("Orphan check Task_Activity.user_id in Users:", len(set(tasks['user_id']) - user_ids_b))
print("Orphan check Milestones.user_id in Users:", len(set(milestones['user_id']) - user_ids_b))

print("Orphan check Events.session_id in Sessions:", len(set(events['session_id']) - set(sessions['session_id'])))
print("Orphan check Tasks.session_id in Sessions:", len(set(tasks['session_id'].dropna()) - set(sessions['session_id'])))

# K: Messy Data Audits
print("\n--- K. MESSY DATA AUDIT ---")
messy_users = all_dfs["F1_Users_Messy_Audit"]
print("Messy Users Duplicates on user_id:", messy_users['user_id'].duplicated().sum())
print("Messy Users Duplicate rows exact:", messy_users.duplicated().sum())
print("Messy Users trailing spaces check:")
str_cols = messy_users.select_dtypes(include='object').columns
for sc in str_cols:
    has_trailing = messy_users[sc].dropna().apply(lambda x: isinstance(x, str) and (x != x.strip())).sum()
    if has_trailing > 0:
        print(f"  Field '{sc}' has {has_trailing} values with leading/trailing whitespace!")

messy_events = all_dfs["F2_10_Event_Data_Quality_Audit"]
print("\nMessy Events Duplicates on event_id:", messy_events['event_id'].duplicated().sum())
print("Messy Events Duplicate rows exact:", messy_events.duplicated().sum())
for sc in ['feature_name', 'event_name', 'event_status', 'device', 'platform']:
    if sc in messy_events.columns:
        print(f"  Field '{sc}' unique values:", messy_events[sc].unique().tolist())
        has_trailing = messy_events[sc].dropna().apply(lambda x: isinstance(x, str) and (x != x.strip())).sum()
        if has_trailing > 0:
            print(f"  Field '{sc}' has {has_trailing} values with leading/trailing whitespace!")
