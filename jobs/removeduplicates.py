import csv

def save_to_csv(filename="jobs_output.csv"):
    jobicy_rss = fetch_jobicy_rss() or []
    postman_rss = fetch_postman_rss() or []
    remoteok_data = fetch_remoteok_jobs() or []

    jobicy_clean = [normalize_jobicy(j) for j in jobicy_rss if j]
    postman_clean = [normalize_postman(j) for j in postman_rss if j]
    remoteok_clean = [normalize_remoteok(j) for j in remoteok_data if j]

    # Combine all
    all_jobs = jobicy_clean + postman_clean + remoteok_clean

    # Remove duplicates by URL
    seen = set()
    deduped = []
    for job in all_jobs:
        url = job.get("url", "").strip()
        if url and url not in seen:
            deduped.append(job)
            seen.add(url)

    fieldnames = ["title", "company", "location", "remote", "url", "description"]

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(deduped)

    print(f"Saved {len(deduped)} unique jobs to {filename}")
