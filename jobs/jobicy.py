import urllib.request
import json

def fetch_jobicy_rss(url: str = "https://jobicy.com/api/v2/remote-jobs"):
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}  # Needed or Jobicy blocks it
        )

        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())

        return data.get("jobs", [])

    except Exception as e:
        print("Error fetching API:", e)
        return []


if __name__ == "__main__":
    data = fetch_jobicy_rss()

    for job in data[:5]:
        print(
            job.get("jobTitle", ""),   # ← THIS IS THE CORRECT KEY
            job.get("url", ""),
            "\n"
        )

def normalize_jobicy(job: dict) -> dict:
    """Normalize Jobicy job fields so the Flask app can use them consistently."""

    return {
        "title": job.get("jobTitle", "No title"),
        "company": job.get("companyName", "Unknown company"),
        "location": job.get("jobGeo", "Remote"),
        "type": job.get("jobType", "N/A"),
        "description": job.get("jobExcerpt", ""),
        "full_description": job.get("jobDescription", ""),
        "url": job.get("url", "#"),
        "source": "Jobicy",
    }
