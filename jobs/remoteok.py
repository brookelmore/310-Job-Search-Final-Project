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

        # Skip metadata rows
        return [job for job in data if isinstance(job, dict) and job.get("position")]

    except Exception as e:
        print("Error fetching RemoteOK API:", e)
        return []


def normalize_remoteok(job: dict) -> dict:
    return {
        "title": job.get("position", "No title"),
        "company": job.get("company", "Unknown company"),
        "location": job.get("location", "Remote"),
        "remote": True,
        "description": job.get("description", "")[:250],
        "full_description": job.get("description", ""),
        "url": job.get("url", "#"),
        "source": "RemoteOK"
    }