from green.celery import app


@app.task(ignore_result=True)
def poll_records():
    pass
