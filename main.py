from flask import Flask, request, jsonify
from rq import Queue
from redis import Redis

from app.job_queue_callbacks import (
    on_success_callback,
    on_failure_callback,
    on_stopped_callback,
)
from app.heavy_task import time_taking_task

#  Let's setup the flask app

app = Flask(__name__)
app.config.from_pyfile("settings.py")  # Load settings from settings.py


# Let's setup redis queue

redis_conn = Redis(
    host=app.config["REDIS_HOST"],
    port=app.config["REDIS_PORT"],
    db=app.config["REDIS_DB"],
    password=app.config["REDIS_PASSWORD"],
)

queues = {
    "default": Queue(connection=redis_conn),
    "MEDIUM": Queue(
        name="MEDIUM",
        connection=redis_conn,
        default_timeout=app.config["CUSTOM_QUEUES"]["MEDIUM"]["default_timeout"],
    ),
}

q = queues.get("MEDIUM")



# Let's setup Flask routes

@app.route("/ping")
def ping():
    return "This python-flask server is up and running!"



# This is the problematic route where a task is taking too much time and where the tasks need to be queued

@app.route("/heavy-task", methods=["GET", "POST"])
def heavy_task():
    if request.method == "POST":
        # Extract values from Post Formdata
        query_arg1 = request.form.get("query_arg1", "default_value")
        query_arg2 = request.form.get("query_arg2", 1)
        
    elif request.method == "GET":
        # Extract values from QueryParams -  site.com?query_arg1=skdf&query_arg2=300
        query_arg1 = request.args.get("query_arg1")
        query_arg2 = request.args.get("query_arg2")
        
    else:
        return jsonify({"error": "Unsupported HTTP method"}), 400

    # Before this heavy task was running without a job queue
    # heavy_task(query_arg1, query_arg2)


    # Now let's enqueue 'time_taking_task' in our redis job queue so that it's executed by a Job worker
    
    job = q.enqueue(
        time_taking_task,
        result_ttl=app.config["RESULT_TTL_MEDIUM"],
        on_success=on_success_callback,
        on_failure=on_failure_callback,
        on_stopped=on_stopped_callback,
        query_arg1=query_arg1,
        query_arg2=query_arg2
    )
    
    return jsonify(
        status=200,
        query_arg1=query_arg1,
        query_arg2=query_arg2,
        
        message=f"Job is queued and result can be collected by a GET request at '/jobs/{job.id}' once the job is completed",
        job_id=job.id,
        job_status=job.get_status(),
    )


@app.route("/jobs/<job_id>", methods=["GET"])
def get_job_info(job_id):
    try:
        job = q.fetch_job(job_id)
        if job is None:
            return jsonify({"error": "Job not found"}), 404
        return jsonify(
            {
                "id": job.id,
                "func_name": job.func_name,
                "args": job.args,
                "kwargs": job.kwargs,
                "status": job.get_status(),
                "result": job.result,
                "enqueued_at": str(job.enqueued_at),
                "started_at": str(job.started_at),
                "ended_at": str(job.ended_at),
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug="on", host="0.0.0.0", port=5000)
