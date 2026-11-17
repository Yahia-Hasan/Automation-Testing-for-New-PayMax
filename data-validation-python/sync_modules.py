"""
Module sync script for PayMax portal.
Reads 'PayMax Modules and Sub-Modules.xlsx' and updates the PayMax product modules.
Run with '--apply' to actually send the PUT request to the server.
"""

import openpyxl
import requests
import urllib3
import json
import sys
import argparse

sys.stdout.reconfigure(encoding='utf-8')
urllib3.disable_warnings()

BASE_URL = "https://196.218.246.252:2027/BE/api"

def load_excel_modules(file_path):
    wb = openpyxl.load_workbook(file_path)
    ws = wb['الموديولات']
    modules_dict = {}
    for r in range(2, ws.max_row + 1):
        mod = ws.cell(r, 2).value
        sub = ws.cell(r, 3).value
        if mod:
            mod = str(mod).strip()
            if mod not in modules_dict:
                modules_dict[mod] = []
            if sub:
                sub = str(sub).strip()
                if sub and sub not in modules_dict[mod]:
                    modules_dict[mod].append(sub)
    
    result = []
    for mod_name, subs in modules_dict.items():
        result.append({
            "name": mod_name,
            "submodules": subs
        })
    return result

def main():
    parser = argparse.ArgumentParser(description="Sync modules to PayMax portal")
    parser.add_argument("--apply", action="store_true", help="Send actual PUT request to portal")
    parser.add_argument("--keep-khazina-separate", action="store_true", help="Keep 'خزينه' as separate module instead of mapping to 'الخزينة (Finance)'")
    args = parser.parse_args()

    print("==================================================")
    print("1. Loading Excel file...")
    excel_modules = load_excel_modules("PayMax Modules and Sub-Modules.xlsx")
    print(f"Loaded {len(excel_modules)} modules with {sum(len(m['submodules']) for m in excel_modules)} submodules.")

    session = requests.Session()
    session.verify = False

    print("\n2. Initializing session and fetching CSRF...")
    session.get(f"{BASE_URL}/auth/csrf", headers={"X-Requested-With": "XMLHttpRequest"})
    xsrf_token = session.cookies.get("XSRF-TOKEN")
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }
    if xsrf_token:
        headers["X-XSRF-TOKEN"] = xsrf_token

    print("3. Logging in as Ma3nAdmin...")
    login_resp = session.post(
        f"{BASE_URL}/auth/login",
        json={"userName": "Ma3nAdmin", "password": "123456", "rememberMe": True},
        headers=headers
    )
    if login_resp.status_code != 200:
        print(f"Login failed! Status: {login_resp.status_code}, Response: {login_resp.text}")
        return

    print("Login successful!")
    if session.cookies.get("XSRF-TOKEN"):
        headers["X-XSRF-TOKEN"] = session.cookies.get("XSRF-TOKEN")

    print("\n4. Getting PayMax product ID...")
    prod_resp = session.get(f"{BASE_URL}/products", headers=headers)
    products = prod_resp.json().get("items", [])
    paymax = next((p for p in products if p.get("name") == "PayMax"), None)
    if not paymax:
        print("PayMax product not found!")
        return

    paymax_id = paymax["id"]
    print(f"Found PayMax: ID = {paymax_id}")

    print("\n5. Checking existing modules in database...")
    existing_mods_resp = session.get(f"{BASE_URL}/products/{paymax_id}/modules", headers=headers)
    existing_mods = existing_mods_resp.json()
    print(f"Found {len(existing_mods)} existing module/submodule items:")
    for m in existing_mods:
        print(f" - ID: {m.get('id')} | Name: '{m.get('name')}' | Tickets: {m.get('ticketsCount')} | Parent: {m.get('parentId')}")

    khazina_id = None
    for m in existing_mods:
        if m.get("name") == "خزينه" and m.get("parentId") is None:
            khazina_id = m.get("id")
            break

    final_modules = []

    # If keep-khazina-separate is requested, keep 'خزينه' as an inactive or active module
    if args.keep_khazina_separate and khazina_id:
        print(f"\nKeeping original 'خزينه' (ID: {khazina_id}) separate (as inactive).")
        final_modules.append({
            "id": khazina_id,
            "name": "خزينه",
            "nameEn": None,
            "isActive": False
        })

    for mod in excel_modules:
        mod_name = mod["name"]
        mod_id = None
        if not args.keep_khazina_separate and "الخزينة" in mod_name and khazina_id:
            mod_id = khazina_id
            print(f"Mapping existing 'خزينه' (ID: {khazina_id}) -> '{mod_name}' to preserve ticket links.")

        mod_entry = {
            "id": mod_id,
            "name": mod_name,
            "nameEn": None,
            "isActive": True
        }
        if mod["submodules"]:
            mod_entry["children"] = [
                {
                    "id": None,
                    "name": sub_name,
                    "nameEn": None,
                    "isActive": True
                }
                for sub_name in mod["submodules"]
            ]
        final_modules.append(mod_entry)

    payload = {"modules": final_modules}
    print(f"\nTotal modules to send: {len(final_modules)}")
    
    if not args.apply:
        print("\n[DRY RUN MODE] Run with '--apply' to submit changes to the portal.")
        return

    print("\n6. Sending PUT request to portal...")
    update_resp = session.put(
        f"{BASE_URL}/products/{paymax_id}/modules",
        json=payload,
        headers=headers
    )
    print(f"Update response status: {update_resp.status_code}")
    if update_resp.status_code in (200, 204):
        print(" SUCCESS! Modules and submodules saved successfully to PayMax!")
    else:
        print(f"Failed to update! Status: {update_resp.status_code}, Response: {update_resp.text}")

if __name__ == "__main__":
    main()
