import urllib.request
import json

def fetch_postman_rss(url: str = "https://arbeitnow.com/api/job-board-api"):
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        jobs = data.get("data", [])

        parsed = []
        for job in jobs:
            parsed.append({
                "title": job.get("title", ""),
                "company": job.get("company_name", ""),
                "location": job.get("location", ""),
                "remote": job.get("remote", False),
                "url": job.get("url", ""),
                "description": job.get("description", "")
            })

        return parsed

    except Exception as e:
        print("Error fetching API:", e)
        return []


if __name__ == "__main__":
    data = fetch_postman_rss()
    for job in data[:5]:
        print(job["title"], job["url"], "\n")