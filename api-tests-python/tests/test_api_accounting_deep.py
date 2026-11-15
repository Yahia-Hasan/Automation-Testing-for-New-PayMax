"""
Deep API Test Suite: Accounting, Invoices, Financial Integrity, and Date Edge Cases.
Covers:
- SQL Server DateTime overflow (0001-01-01 returning 500)
- Missing query parameters leading to NullReferenceException (500)
- Reversed date ranges (fromDate > toDate silent 200 vs 400 validation)
- Negative financial values, negative days count, and DOM/API tampering risks
- Math integrity (Total == Cash + Credit)
- High-concurrency race condition and DbContext thread safety
"""
import pytest
from concurrent.futures import ThreadPoolExecutor
from client.api_client import BayMaxApiClient

class TestApiAccountingDeep:

    def test_01_sql_datetime_overflow_crash(self, auth_client: BayMaxApiClient):
        """
        [DEFECT DETECTED]
        Sending .NET DateTime.MinValue ('0001-01-01') causes SQL Server SqlDateTime overflow,
        producing an unhandled HTTP 500 Internal Server Error instead of HTTP 400 Bad Request.
        """
        params = {"fromDate": "0001-01-01", "toDate": "0001-12-31"}
        resp = auth_client.get("/api/accountant/invoices", params=params)
        print(f"\n[DATETIME OVERFLOW] Status: {resp.status_code}")
        
        # Document the bug
        if resp.status_code == 500:
            print("  [DEFECT CONFIRMED] Backend threw 500 due to unhandled SqlDateTime overflow.")
        assert resp.status_code != 500, (
            f"Backend crashed with 500 on 0001-01-01 date range (SqlDateTime overflow): {resp.text}"
        )

    def test_02_physical_therapy_missing_dates_nullref(self, auth_client: BayMaxApiClient):
        """
        [DEFECT DETECTED]
        Calling /api/physical-therapy/waiting-list without required fromDate/toDate query params
        triggers an unhandled NullReferenceException resulting in HTTP 500 instead of HTTP 400.
        """
        resp = auth_client.get("/api/physical-therapy/waiting-list")
        print(f"\n[MISSING PARAMS] Physical Therapy waiting-list status: {resp.status_code}")
        
        if resp.status_code == 500:
            print("  [DEFECT CONFIRMED] Missing fromDate/toDate causes 500 crash rather than 400 validation.")
        assert resp.status_code != 500, (
            f"Backend threw 500 when query params are omitted: {resp.text}"
        )

    def test_03_inverted_date_range_silent_behavior(self, auth_client: BayMaxApiClient):
        """
        [DEFECT / LOGIC ISSUE]
        When fromDate is AFTER toDate, the API silently returns HTTP 200 with an empty list
        instead of validating inputs and returning HTTP 400 (fromDate cannot be greater than toDate).
        """
        params = {"fromDate": "2026-10-17", "toDate": "2026-01-01"}
        resp = auth_client.get("/api/accountant/invoices", params=params)
        print(f"\n[INVERTED DATES] Status: {resp.status_code}, Payload length: {len(resp.json())}")
        
        is_empty_200 = resp.status_code == 200 and isinstance(resp.json(), list) and len(resp.json()) == 0
        if is_empty_200:
            print("  [LOGIC DEFECT] Inverted dates accepted silently (HTTP 200 with empty array) without validation error.")
        assert resp.status_code in [400, 422], (
            f"Expected HTTP 400/422 for inverted date range, but API returned {resp.status_code}."
        )

    def test_04_negative_amounts_and_days_in_invoices(self, auth_client: BayMaxApiClient):
        """
        [CRITICAL FINANCIAL DEFECT]
        Audits live database invoices for negative totals, negative cash values, or negative daysCount.
        Demonstrates that lack of server-side validation allowed negative daysCount (-1) to produce
        negative accommodation values (-5,000 EGP) and negative invoice totals.
        """
        resp = auth_client.get("/api/accountant/invoices", params={"fromDate": "2020-01-01", "toDate": "2026-10-17"})
        assert resp.status_code == 200, f"Failed to retrieve invoices: {resp.status_code}"
        
        invoices = resp.json()
        neg_totals = [i for i in invoices if (i.get("total") or 0) < 0]
        neg_cash = [i for i in invoices if (i.get("totalCash") or 0) < 0]

        print(f"\n[FINANCIAL AUDIT] Analyzed {len(invoices)} invoices.")
        print(f"  Negative Total Invoices: {len(neg_totals)}")
        print(f"  Negative Cash Invoices:  {len(neg_cash)}")

        for inv in neg_totals:
            print(f"  [NEGATIVE INVOICE] ID: {inv.get('invoiceId')}, Res: {inv.get('reservationId')}, Total: {inv.get('total')}, Cash: {inv.get('totalCash')}")

        assert len(neg_totals) == 0 and len(neg_cash) == 0, (
            f"CRITICAL DEFECT: Found {len(neg_totals)} negative total invoices and {len(neg_cash)} negative cash invoices in DB!"
        )

    def test_05_math_consistency_cash_credit_total(self, auth_client: BayMaxApiClient):
        """
        [FINANCIAL INTEGRITY]
        Validates that for all invoices: Total == TotalCash + TotalCredit.
        Detects database records where totals were manipulated or updated out of sync.
        """
        resp = auth_client.get("/api/accountant/invoices", params={"fromDate": "2025-01-01", "toDate": "2026-10-17"})
        assert resp.status_code == 200
        
        invoices = resp.json()
        mismatches = []
        for i in invoices:
            total = round(i.get("total") or 0, 2)
            components = round((i.get("totalCash") or 0) + (i.get("totalCredit") or 0), 2)
            if total != components:
                mismatches.append({
                    "invoiceId": i.get("invoiceId"),
                    "total": total,
                    "components": components,
                    "diff": round(total - components, 2)
                })

        print(f"\n[MATH AUDIT] Analyzed {len(invoices)} invoices. Mismatches found: {len(mismatches)}")
        for m in mismatches[:5]:
            print(f"  [MISMATCH] Invoice #{m['invoiceId']}: Total={m['total']} vs (Cash+Credit)={m['components']} (Diff: {m['diff']})")

        assert len(mismatches) == 0, (
            f"Found {len(mismatches)} invoices where Total does not equal Cash + Credit."
        )

    def test_06_overpaid_invoices_integrity(self, auth_client: BayMaxApiClient):
        """
        [ACCOUNTING AUDIT]
        Identifies open or completed invoices where totalPaidAmount exceeds total without change settlement.
        """
        resp = auth_client.get("/api/accountant/invoices", params={"fromDate": "2026-01-01", "toDate": "2026-10-17"})
        assert resp.status_code == 200
        
        invoices = resp.json()
        overpaid = [i for i in invoices if (i.get("totalPaidAmount") or 0) > (i.get("total") or 0)]
        print(f"\n[OVERPAID INVOICES] Found {len(overpaid)} out of {len(invoices)} invoices where totalPaidAmount > total.")
        
        # Informational check
        assert len(invoices) > 0

    def test_07_concurrent_invoice_access_stress(self, auth_client: BayMaxApiClient):
        """
        [RAPID CLICK / CONCURRENCY STRESS]
        Fires 15 simultaneous requests against /api/invoice-details/{id} to verify
        thread safety of Entity Framework Core DbContext under burst load.
        """
        test_res_id = 12780

        def fetch_details(index):
            return auth_client.get(f"/api/invoice-details/{test_res_id}")

        with ThreadPoolExecutor(max_workers=15) as executor:
            futures = [executor.submit(fetch_details, i) for i in range(15)]
            responses = [f.result() for f in futures]

        statuses = [r.status_code for r in responses]
        print(f"\n[CONCURRENCY BURST] 15 parallel requests to invoice-details/{test_res_id}. Statuses: {set(statuses)}")
        
        failures = [r for r in responses if r.status_code != 200]
        assert len(failures) == 0, f"Some concurrent requests failed: {[r.status_code for r in failures]}"
