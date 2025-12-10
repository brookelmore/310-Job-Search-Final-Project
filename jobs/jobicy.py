import urllib.request
import json

def fetch_jobicy_rss(url: str = "https://jobicy.com/api/v2/remote-jobs"):
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
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
            job.get("jobTitle", ""),
            job.get("url", ""),
            "\n"
        )