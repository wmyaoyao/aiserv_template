import asyncio
import os
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

app = FastAPI()


class ReportStatus(BaseModel):
    status: str
    progress: int

@app.post("/start_report/", response_model=ReportStatus)
async def start_report():
    # Check if there's an existing report task running
    if hasattr(start_report, 'report_task') and not start_report.report_task.done():
        return {"status": "Report task already running"}

    # Run the get_report task asynchronously
    start_report.report_task = asyncio.ensure_future(run_get_report())
    return {"status": "Report task started"}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)