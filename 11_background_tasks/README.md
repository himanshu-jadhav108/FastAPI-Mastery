# 11 — Background Tasks

## Theory

Sometimes an endpoint needs to do something *after* responding — send a
confirmation email, write a log, notify a webhook — where the client
shouldn't have to wait for that extra work to finish.

```python
from fastapi import BackgroundTasks

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(message + "\n")

@app.post("/tasks")
def create_task(title: str, background_tasks: BackgroundTasks):
    # ... create the task ...
    background_tasks.add_task(write_log, f"Task created: {title}")
    return {"message": "Task created"}
```

The response is sent to the client immediately; `write_log` runs *after*
that, in the same process. `add_task(fn, *args, **kwargs)` — args are
passed straight through to the function.

**Important limitation:** background tasks run in the same process as
your app, using the same event loop/thread pool. They're fine for quick
jobs (logging, a fast notification). For anything slow, heavy, or that
must survive a server restart or crash — sending real emails at scale,
image processing, anything that could take seconds+ — use a real task
queue instead (Celery, ARQ, Dramatiq, RQ). `BackgroundTasks` is not a job
queue; it has no retries, no persistence, no distribution across workers.

## Task

Open `starter.py`.

1. Write `write_activity_log(username: str, message: str)` — appends a
   line `"{timestamp} | {username} | {message}"` to `activity.log`.
2. `POST /tasks` → after creating the task, schedule
   `write_activity_log` to record `f"Created task: {title}"`.
3. `DELETE /tasks/{task_id}` → schedule a log entry
   `f"Deleted task: {task_id}"` after deleting.
4. `POST /tasks/{task_id}/notify` → doesn't touch the task; just
   schedules a background task that `time.sleep(2)`s (simulating slow
   work like sending an email) then logs
   `f"Notification sent for task {task_id}"`. Confirm the endpoint
   returns **instantly** even though the background job takes 2 seconds
   — check `activity.log` a moment later to see it landed.
