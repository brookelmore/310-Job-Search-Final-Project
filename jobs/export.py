from .jobicy import fetch_jobicy_rss
from .postman import fetch_postman_rss
from .remoteok import fetch_remoteok_jobs

def normalize_jobicy(job):
    return {
        "title": job.get("title", ""),
        "company": "N/A",
        "location": "Remote",
        "remote": True,
        "url": job.get("link", ""),
        "description": job.get("description", ""),
    }

def normalize_postman(job):
    return {
        "title": job.get("title", ""),
        "company": job.get("company", ""),
        "location": job.get("location", ""),
        "remote": job.get("remote", False),
        "url": job.get("url", ""),
        "description": job.get("description", ""),
    }

def normalize_remoteok(job):
    return {
        "title": job.get("position", ""),
        "company": job.get("company", ""),
        "location": job.get("location", ""),
        "remote": True,
        "url": job.get("url", ""),
        "description": job.get("description", ""),
    }

def save_to_csv(filename="jobs_output.csv"):
    jobicy_rss = fetch_jobicy_rss()
    postman_rss = fetch_postman_rss()
    remoteok_data = fetch_remoteok_jobs()

    jobicy_clean = [normalize_jobicy(j) for j in jobicy_rss]
    postman_clean = [normalize_postman(j) for j in postman_rss]
    remoteok_clean = [normalize_remoteok(j) for j in remoteok_data]

    combined = jobicy_clean + postman_clean + remoteok_clean

    unique = {}
    for job in combined:
        unique[job["url"]] = job

    combined = list(unique.values())

    fieldnames = ["title", "company", "location", "remote", "url", "description"]

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(combined)

    print(f"Saved {len(combined)} unique jobs to {filename}")


if __name__ == "__main__":
    from .export import save_to_csv
    save_to_csv()