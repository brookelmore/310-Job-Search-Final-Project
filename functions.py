
import re

def search_jobs(query="", remote_only=False):
    from jobs.export import normalize_jobicy, normalize_postman, normalize_remoteok
    from jobs.jobicy import fetch_jobicy_rss
    from jobs.postman import fetch_postman_rss
    from jobs.remoteok import fetch_remoteok_jobs

    jobicy_raw = fetch_jobicy_rss() or []
    postman_raw = fetch_postman_rss() or []
    remoteok_raw = fetch_remoteok_jobs() or []

    jobicy = [normalize_jobicy(j) for j in jobicy_raw if j]
    postman = [normalize_postman(j) for j in postman_raw if j]
    remoteok = [normalize_remoteok(j) for j in remoteok_raw if j]

    all_jobs = jobicy + postman + remoteok

    company_keywords = [
        "llc", "inc", "gmbh", "partners", "group", "limited", "corporation"
    ]
    locations = [
        "munich", "new york", "london", "berlin", "frankfurt",
        "usa", "uk", "germany", "italy", "remote"
    ]

    cleaned_jobs = []
    for job in all_jobs:
        title = job.get("title") or ""
        # Remove parenthesis and their contents
        title = re.sub(r"\(.*?\)", "", title)
        # Take only first part before "-" or ":"
        title = title.split(" - ")[0].split(" : ")[0].strip()
        title_lower = title.lower()

        # Skip if title contains company keywords
        if any(word in title_lower for word in company_keywords):
            continue
        # Skip if title contains locations
        if any(word in title_lower for word in locations):
            continue
        # Skip if too short or too long
        if len(title) < 3 or len(title.split()) > 10:
            continue

        job["title"] = title
        cleaned_jobs.append(job)

    filtered = []
    q = query.lower().strip()

    for job in cleaned_jobs:
        title = (job.get("title") or "").lower()
        desc = (job.get("description") or "").lower()

        if q and q not in title and q not in desc:
            continue

        if remote_only and not job.get("remote"):
            continue

        filtered.append(job)

    # Deduplicate by URL
    seen = set()
    deduped = []
    for job in filtered:
        url = (job.get("url") or "").strip()
        if url and url not in seen:
            deduped.append(job)
            seen.add(url)

    return deduped
