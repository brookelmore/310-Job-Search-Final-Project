from jobs.jobicy import fetch_jobicy_rss, normalize_jobicy
from jobs.postman import fetch_postman_rss, normalize_postman
from jobs.remoteok import fetch_remoteok_jobs, normalize_remoteok

def search_jobs(query="", remote_only=False):
    """
    Fetches, normalizes, filters, and deduplicates job listings.
    Returns a list of cleaned job dictionaries.
    """

    # --- Fetch data ---
    jobicy_raw = fetch_jobicy_rss() or []
    postman_raw = fetch_postman_rss() or []
    remoteok_raw = fetch_remoteok_jobs() or []

    # --- Normalize ---
    jobicy = [normalize_jobicy(j) for j in jobicy_raw if j]
    postman = [normalize_postman(j) for j in postman_raw if j]
    remoteok = [normalize_remoteok(j) for j in remoteok_raw if j]

    # Combine all
    all_jobs = jobicy + postman + remoteok

    # --- Filter by query + remote flag ---
    filtered = []
    q = query.lower().strip()

    for job in all_jobs:
        title = (job.get("title") or "").lower()
        desc = (job.get("description") or "").lower()

        # Keyword filter
        if q and q not in title and q not in desc:
            continue

        # Remote-only filter
        if remote_only and not job.get("remote"):
            continue

        filtered.append(job)

    # --- Deduplicate by URL ---
    seen = set()
    deduped = []

    for job in filtered:
        url = (job.get("url") or "").strip()
        if url and url not in seen:
            deduped.append(job)
            seen.add(url)

    return deduped
