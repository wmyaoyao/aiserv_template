## Fast API server for long-run (async) task

## Ask ChatGPT or Bard
Prompt:
"
I need to implement a python api server. The server needs to support an async "get_report" task, which needs to run for very long time. 
We can only run one get_report task in the api server.
Obviously, the api server needs to provide a way for user to monitor the status or cancle the current get_report task.
How do I implement this in python with FastAPI?
"