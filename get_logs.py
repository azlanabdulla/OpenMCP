import urllib.request
import json
import zipfile
import io
import os

req = urllib.request.Request("https://api.github.com/repos/azlanabdulla/OpenMCP/actions/runs")
req.add_header("User-Agent", "Mozilla/5.0")
try:
    with urllib.request.urlopen(req) as response:
        runs = json.loads(response.read()).get("workflow_runs", [])
        if not runs:
            exit()
        latest_run = runs[0]
        run_id = latest_run["id"]
        
        logs_url = f"https://api.github.com/repos/azlanabdulla/OpenMCP/actions/runs/{run_id}/logs"
        req_logs = urllib.request.Request(logs_url)
        req_logs.add_header("User-Agent", "Mozilla/5.0")
        with urllib.request.urlopen(req_logs) as logs_response:
            zip_content = logs_response.read()
            with zipfile.ZipFile(io.BytesIO(zip_content)) as z:
                for filename in z.namelist():
                    if "Lint and Test Backend" in filename:
                        print(f"--- LOG: {filename} ---")
                        print(z.read(filename).decode('utf-8'))
except Exception as e:
    print("Error:", e)
