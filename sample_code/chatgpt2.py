"""
uvicorn main:app --host 0.0.0.0 --port 8000

POST /start_report/: This endpoint starts the "get_report" task.
GET /report_status/: This endpoint checks the status of the current "get_report" task.
POST /cancel_report/: This endpoint cancels the running "get_report" task.
"""
import asyncio
import os
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel


app = FastAPI()


class ReportStatus(BaseModel):
    status: str

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