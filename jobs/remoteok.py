import urllib.request
import json

def fetch_remoteok_jobs(url="https://remoteok.com/api"):
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())

        return [job for job in data if isinstance(job, dict) and job.get("position")]

    except Exception as e:
        print("Error fetching RemoteOK API:", e)
        return []

