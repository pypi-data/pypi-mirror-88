# fastapi-authenticator

fastapi authenticator for google cloud tasks

## Installation

server:

~~~
pip3 install fastapi-authenticator
~~~

client:

~~~
pip3 install gcp-taskqueue
~~~

## Usage

server:

~~~python
from fastapi import Depends, FastAPI
from fastapi_authenticator import GoogleCloudTask, google_cloud_task, google_cloud_auth

app = FastAPI()

@app.post("/task1")
def task_handler(
    claims: dict = Depends(google_cloud_auth),
    task: GoogleCloudTask: Depends(google_cloud_task)
):
    ...
~~~

client:

~~~python
from gcp_taskqueue import TaskQueue

queue = TaskQueue(queue_id="your-queue-name")

queue.create_http_task("https://url", deadline=300)
~~~

## Deployment

`Service Account User` Role is needed for the client to generate oidc token.
