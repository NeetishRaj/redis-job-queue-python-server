# Message Queue | Job Queue | Redis Queue In Python with on_success callbacks
In a Python Flask server if there is an endpoint that's taking too much time then we need that heavy task delegated to a separate Job queue, where dedicated Job workers will take their time executing these time-taking jobs one by one without disturbing the main server.

##### **NOTE**: Once these time-taking functions are executed we can handle the results of those functions in a success callback. 

All the details about Redis Queue can be found on their official documentation page 
https://python-rq.org/docs/


## Get Redis Job Queue status

once a request is made for the job, we will get the `job_id`.
we can then use this `job_id` to poll for the result at `/jobs/<job_id>` until `job_status` changes from `queued` to `finished`.
Or we can notify succuesful job completion using the `on_success_callback` 


Sample /heavy-task GET request 
 `http://localhost:5000/heavy-task?query_arg1=value1&query_arg2=value2`

Response:
```json
{
  "job_id": "d90272c6-f02c-4c8b-9496-536ea5dd2888",
  "job_status": "queued",
  "message": "Job is queued and result can be collected by a GET request at '/jobs/d90272c6-f02c-4c8b-9496-536ea5dd2888' once the job is completed",
  "query_arg1": "value1",
  "query_arg2": "value2",
  "status": 200
}
```


Check Job status in the queue
HTTP GET for jobs
`/jobs/d90272c6-f02c-4c8b-9496-536ea5dd2888`

Response:
```json
{
  "args": [],
  "ended_at": "2024-02-29 04:42:17.052463",
  "enqueued_at": "2024-02-29 04:42:07.025638",
  "func_name": "app.heavy_task.time_taking_task",
  "id": "d90272c6-f02c-4c8b-9496-536ea5dd2888",
  "kwargs": {
    "query_arg1": "value1",
    "query_arg2": "value2"
  },
  "result": {
    "message": "Job Worker: Heavy task completed after 10 seconds. query_arg1: 'value1', query_arg2: 'value2'",
    "query_arg1": "value1",
    "query_arg2": "value2"
  },
  "started_at": "2024-02-29 04:42:07.036312",
  "status": "finished"
}
```

## Running on a pipenv 
```sh
pipenv install rq
pipenv install redis
pipenv install flask
pipenv shell
python3 main.py

```

## Setup Redis Queue Server
```sh
# install pip dependencies
pip3 install rq
pip3 install redis
pip3 install flask

# Install redis server if not already done
sudo apt-get install redis-server

# to check if redis server is installed and run , we should get pong for ping
redis-cli ping

# install rq jobs worker
sudo apt-get install python3-rq

# now keep the rq job worker service running in a separate thread
tmux new -s rq_worker

# start the job service and leave it running for the interested queues
rq worker MEDIUM

# detach from the console press ctrl + b then d

```