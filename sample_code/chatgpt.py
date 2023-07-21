"""
pip install fastapi uvicorn websockets

Now, when you run the FastAPI server with uvicorn main:app, you will have two endpoints:

GET /get_report/: This endpoint will start the long-running task in the background. 
If the task is already running, it will return an error response.

WebSocket /ws/: This endpoint will allow the client to connect via a WebSocket and monitor 
the status of the running task. If the task is done, it will send the result, and if the task 
is canceled, it will send a cancellation message.

You can use the WebSocket endpoint to establish a connection from the client and monitor 
the status of the task or receive the final result. 
Additionally, you can use the GET /get_report/ endpoint to start the task and receive a 
response if it was successfully started or if it's already running. If needed, you can 
modify the ReportTask class to handle more complex scenarios, but this basic implementation 
should serve as a good starting point.
"""
from fastapi import FastAPI, BackgroundTasks, WebSocket
from fastapi.responses import JSONResponse
import asyncio
import websockets


class ReportTask:
    _instance = None
    _task = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ReportTask, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    async def get_report(self):
        # Simulate a long-running task
        await asyncio.sleep(10)
        return {"status": "completed"}

    def start_task(self):
        self._task = asyncio.create_task(self.get_report())

    def cancel_task(self):
        if self._task:
            self._task.cancel()

app = FastAPI()
report_task = ReportTask()

@app.get("/get_report/")
async def get_report(background_tasks: BackgroundTasks):
    if report_task._task and not report_task._task.done():
        return JSONResponse(content={"status": "Task already running"}, status_code=400)

    # Start the long-running task in the background
    background_tasks.add_task(report_task.start_task)
    return {"status": "Task started"}

@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        try:
            # Check the status of the running task
            if report_task._task and report_task._task.done():
                result = report_task._task.result()
                await websocket.send_text(f"Task status: {result['status']}")
                break

            await asyncio.sleep(1)
        except asyncio.CancelledError:
            await websocket.send_text("Task canceled")
            break

        except Exception as e:
            await websocket.send_text(f"Error occurred: {str(e)}")
            break


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
