import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By

os.makedirs('screenshots', exist_ok=True)

options = EdgeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1600,1100')
options.add_argument('--hide-scrollbars')

driver = webdriver.Edge(options=options)

def safe_log(msg):
    sys.stdout.buffer.write((msg + '\n').encode('utf-8'))
    sys.stdout.flush()

try:
    safe_log("Navigating to http://localhost:8501...")
    driver.get("http://localhost:8501")
    time.sleep(5)

    # Click on Full Internal Audit mode
    labels = driver.find_elements(By.TAG_NAME, 'label')
    for l in labels:
        if 'Full Internal Audit' in l.text:
            safe_log("Selecting Full Internal Audit mode...")
            driver.execute_script("arguments[0].click();", l)
            time.sleep(2)
            break

    # Helper function to click a sidebar view
    def select_view(keyword):
        labels = driver.find_elements(By.TAG_NAME, 'label')
        for l in labels:
            if keyword in l.text:
                safe_log(f"Selecting view matching: {keyword}")
                driver.execute_script("arguments[0].click();", l)
                time.sleep(3)
                return True
        safe_log(f"Warning: Could not find view matching: {keyword}")
        return False

    # Helper function to click a tab inside the page
    def select_tab(tab_name):
        tabs = driver.find_elements(By.CSS_SELECTOR, "button[data-baseweb='tab']")
        for t in tabs:
            if tab_name.lower() in t.text.lower():
                safe_log(f"Clicking tab: {tab_name}")
                driver.execute_script("arguments[0].click();", t)
                time.sleep(2)
                return True
        return False

    # 1. Capture View 2: Executive Cockpit
    select_view("2. Executive Cockpit")
    time.sleep(3)
    driver.save_screenshot("screenshots/01_executive_cockpit.png")
    safe_log("Captured 01_executive_cockpit.png")

    # 2. Capture View 3: User Lifecycle & Growth (Main Overview)
    select_view("3. User Lifecycle")
    time.sleep(3)
    driver.save_screenshot("screenshots/02_user_lifecycle_overview.png")
    safe_log("Captured 02_user_lifecycle_overview.png")

    # 3. Capture View 3 Tab 5: Referral Funnel & Viral Growth (WP E)
    select_tab("Referral Funnel")
    time.sleep(3)
    driver.save_screenshot("screenshots/03_referral_viral_growth_wpe.png")
    safe_log("Captured 03_referral_viral_growth_wpe.png")

    # 4. Capture View 4: Task & Feature Engagement (Main)
    select_view("4. Task & Feature")
    time.sleep(3)
    driver.save_screenshot("screenshots/04_task_engagement_overview.png")
    safe_log("Captured 04_task_engagement_overview.png")

    # 5. Capture View 4 Tab 2: Anti-Farming & Bot Defense Simulator (WP C)
    select_tab("Anti-Farming")
    time.sleep(3)
    driver.save_screenshot("screenshots/05_anti_farming_bot_defense_wpc.png")
    safe_log("Captured 05_anti_farming_bot_defense_wpc.png")

    # 6. Capture View 5: Data Quality Forensic Audit
    select_view("5. Data Quality")
    time.sleep(3)
    driver.save_screenshot("screenshots/06_data_quality_audit.png")
    safe_log("Captured 06_data_quality_audit.png")

    # 7. Capture View 6: Live Wallet & Payout Simulator (Double Entry Ledger)
    select_view("6. Live Wallet")
    time.sleep(3)
    driver.save_screenshot("screenshots/07_wallet_double_entry_ledger.png")
    safe_log("Captured 07_wallet_double_entry_ledger.png")

    # 8. Capture View 7: 21 Deliverables Verification Matrix
    select_view("7. 21 Deliverables")
    time.sleep(3)
    driver.save_screenshot("screenshots/08_21_deliverables_matrix.png")
    safe_log("Captured 08_21_deliverables_matrix.png")

    safe_log("All screenshots captured successfully!")

except Exception as e:
    safe_log(f"Error during capture: {e}")
finally:
    driver.quit()
