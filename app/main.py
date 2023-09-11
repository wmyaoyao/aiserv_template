import asyncio
import os
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

app = FastAPI()


class ReportStatus(BaseModel):
    status: str
    progress: int

# Demo functions
@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q = list[str]):
    q.append(item_id)
    return {"item_id": item_id, "q": q}


# Work in Progress.
@app.post("/start_report/", response_model=ReportStatus)
async def start_report():
    # Check if there's an existing report task running
    if hasattr(start_report, 'report_task') and not start_report.report_task.done():
        return {"status": "Report task already running"}

    # Run the get_report task asynchronously
    start_report.report_task = asyncio.ensure_future(run_get_report())
    return {"status": "Report task started"}

@app.get("/report_status/", response_model=ReportStatus)
async def report_status():
    # Check if the report task is running
    if hasattr(start_report, 'report_task') and not start_report.report_task.done():
        return {"status": "Report task in progress"}
    else:
        return {"status": "No report task running"}

@app.post("/cancel_report/", response_model=ReportStatus)
async def cancel_report():
    # Check if the report task is running and cancel it
    if hasattr(start_report, 'report_task') and not start_report.report_task.done():
        start_report.report_task.cancel()
        return {"status": "Report task canceled"}
    else:
        return {"status": "No report task running"}

async def run_get_report():
    try:
        # Simulating a long-running task (replace this with your actual get_report implementation)
        await asyncio.sleep(10)

        # Write the result to a CSV file named "output.csv" (you can customize this path)
        with open("output.csv", "w") as file:
            file.write("This is a sample report.")

        return {"status": "Report generated successfully"}

    except asyncio.CancelledError:
        # Clean up any resources or tasks if the task is canceled
        return {"status": "Report task canceled"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)