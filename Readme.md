# API Server for AI Model Inference

This API server uses the FastAPI framework to provide a RESTful interface for AI model inference. The server can be used to deploy and run AI models in production.

The API server exposes the following endpoints:

/predict - This endpoint accepts a JSON payload containing the input data for the model and returns a JSON response containing the model's prediction.
/healthcheck - This endpoint returns a 200 OK response if the server is up and running.



## Ask ChatGPT or Bard
Prompt:
"
I need to implement a Python API server that supports an asynchronous "get_report" task. This task needs to run for a very long time, and we can only run one "get_report" task in the API server at a time. The API server also needs to provide a way for users to monitor the status of the current "get_report" task or cancel it.
"