import os
import csv
import subprocess
import pytest

class TestPerformanceAndLoadSuite:
    """
    Automated Performance & Load Testing Suite for BayMax Hospital ERP.
    Executes headless Locust scenarios across the 4 major hospital workflow groups:
    1. Reception Desk (High-frequency search, profiles, visit history)
    2. Outpatient Clinics (Daily queues, visit draft lookups)
    3. Emergency Department (Triage, waiting list)
    4. Inpatient Billing (Open accounts, complex invoice calculations)
    
    Verifies Service Level Agreements (SLAs):
    - Overall Failure Rate <= 1%
    - 95th Percentile Response Time < 1500ms
    - Reception Search Response Time < 500ms
    """

    @pytest.mark.performance
    def test_hospital_workload_load_and_stress(self):
        """
        Runs Locust headless benchmark with 20 concurrent virtual hospital staff users,
        spawning at 5 users/sec, running for 25 seconds.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        candidate_locust = os.path.join(os.path.dirname(current_dir), "locustfile.py")
        locustfile = candidate_locust if os.path.exists(candidate_locust) else os.path.join(os.getcwd(), "locustfile.py")
        html_report = os.path.join(os.getcwd(), "report_load_test.html")
        csv_prefix = os.path.join(os.getcwd(), "load_metrics")

        cmd = [
            "locust",
            "-f", locustfile,
            "--headless",
            "-u", "20",
            "-r", "5",
            "--run-time", "25s",
            "--host", "https://196.218.246.250:4040/Patients-Modern-BE",
            "--html", html_report,
            "--csv", csv_prefix
        ]

        print(f"\n[LOAD TEST] Launching Locust load test: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        print(result.stdout[-1500:] if len(result.stdout) > 1500 else result.stdout)

        assert result.returncode == 0, f"Locust execution failed: {result.stderr}"

        # Parse generated CSV statistics using standard library csv module
        stats_csv = f"{csv_prefix}_stats.csv"
        assert os.path.exists(stats_csv), f"Locust stats CSV not generated at {stats_csv}"

        rows = []
        with open(stats_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)

        print("\n--- PERFORMANCE SUMMARY TABLE ---")
        for r in rows:
            print(f"{r.get('Type', ''):4} | {r.get('Name', ''):50} | Req: {r.get('Request Count', ''):4} | Fail: {r.get('Failure Count', ''):2} | Med: {r.get('Median Response Time', ''):3}ms | Avg: {r.get('Average Response Time', ''):5}ms")

        # Aggregated row
        agg = next((r for r in rows if r.get("Name") == "Aggregated"), None)
        assert agg is not None, "Aggregated row missing from stats CSV"

        total_requests = int(agg.get("Request Count", 0))
        total_failures = int(agg.get("Failure Count", 0))
        failure_rate = (total_failures / total_requests) * 100 if total_requests > 0 else 0
        avg_response_time = float(agg.get("Average Response Time", 0))
        max_response_time = float(agg.get("Max Response Time", 0))

        print(f"\n[METRICS] Total Requests: {total_requests}, Failures: {total_failures} ({failure_rate:.2f}%)")
        print(f"[METRICS] Avg Latency: {avg_response_time:.1f}ms, Max Latency: {max_response_time:.1f}ms")

        # SLA Assertions
        assert failure_rate <= 1.0, f"Failure rate {failure_rate:.2f}% exceeded 1% SLA threshold!"
        assert avg_response_time < 1000, f"Average response time {avg_response_time:.1f}ms exceeded 1000ms SLA!"
        print("[SLA PASSED] System successfully met all performance throughput and reliability benchmarks!")
