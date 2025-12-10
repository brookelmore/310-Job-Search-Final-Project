from flask import Flask, render_template, request, abort
from functions import search_jobs

app = Flask(__name__)

# Global store for search results
jobs_cache = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def results():
    query = request.args.get("query", "").strip()
    remote_only = request.args.get("remote_only") == "on"

    results_list = search_jobs(query=query, remote_only=remote_only)

    global jobs_cache
    jobs_cache = results_list

    return render_template(
        "results.html",
        jobs=results_list,
        query=query,
        remote_only=remote_only
    )

@app.route("/job/<int:job_id>")
def job_detail(job_id):
    if job_id < 0 or job_id >= len(jobs_cache):
        abort(404, description="Job not found")
    job = jobs_cache[job_id]
    return render_template("job_detail.html", job=job)

if __name__ == "__main__":
    app.run(debug=True)