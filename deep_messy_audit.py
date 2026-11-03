import pandas as pd

file1 = r"C:\Users\ckart\.gemini\antigravity\scratch\veloop_analytics_task01\data\VELoop_Rewards_Data_01.xlsx"
file2 = r"C:\Users\ckart\.gemini\antigravity\scratch\veloop_analytics_task01\data\VELOOP_Simulated_User_Behavior_1000.xlsx"

xl1 = pd.ExcelFile(file1)
messy_u = xl1.parse('Users_Messy_Audit')
clean_u = xl1.parse('Users_1000_Clean')

print("--- USERS MESSY DETAILS ---")
dup_ids = messy_u[messy_u['user_id'].duplicated(keep=False)]
print("Duplicate user rows count:", len(dup_ids))
print("Sample duplicate user IDs:", dup_ids['user_id'].unique())
print("Null counts in messy users vs clean:")
for c in messy_u.columns:
    if c in clean_u.columns:
        diff = messy_u[c].isnull().sum() - clean_u[c].isnull().sum()
        if diff != 0 or messy_u[c].isnull().sum() > 0:
            print(f"  {c}: messy nulls={messy_u[c].isnull().sum()}, clean nulls={clean_u[c].isnull().sum()}")

xl2 = pd.ExcelFile(file2)
messy_e = xl2.parse('10_Event_Data_Quality_Audit')
clean_e = xl2.parse('03_Feature_Events')

print("\n--- EVENTS MESSY DETAILS ---")
dup_evts = messy_e[messy_e['event_id'].duplicated(keep=False)]
print("Duplicate event rows count:", len(dup_evts))
print("Sample duplicate event IDs:", dup_evts['event_id'].unique()[:5])

print("\nCasing mismatches in feature_name:")
print(messy_e['feature_name'].value_counts())

print("\nWhitespace issues in event_status:")
print(repr(messy_e['event_status'].value_counts()))

print("\nDevice distribution:")
print(messy_e['device'].value_counts())
print("\nPlatform distribution:")
print(messy_e['platform'].value_counts())
