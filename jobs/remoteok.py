import urllib.request
import json

def fetch_remoteok_jobs(url: str = "https://remoteok.com/api"):
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        jobs = data[1:] if isinstance(data, list) else []

        parsed = []
        for job in jobs:
            parsed.append({
                "title": job.get("position", ""),
                "company": job.get("company", ""),
                "location": job.get("location", ""),
                "tags": job.get("tags", []),
                "url": job.get("url", ""),
                "description": job.get("description", ""),
            })

        return parsed

    except Exception as e:
        print("Error fetching API:", e)
        return []


if __name__ == "__main__":
    data = fetch_remoteok_jobs()
    for job in data[:5]:
        print(job["title"], job["url"], "\n")