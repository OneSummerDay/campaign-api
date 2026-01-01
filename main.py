from datetime import datetime
from fastapi import FastAPI, HTTPException


app = FastAPI(root_path="/api/v1")

data = [
    {
        "campaing_id": 1,
        "name": "Campaign 1",
        "due_date": datetime.now(),
        "created_at": datetime.now(),
    },
    {
        "campaing_id": 2,
        "name": "Campaign 2",
        "due_date": datetime.now(),
        "created_at": datetime.now(),
    },
]


@app.get("/campaigns")
async def read_campaigns():
    return {"message": data}


@app.get("/campaigns/{id}")
async def read_campaign(id: int):
    for campaign in data:
        if campaign.get("campaign_id") == id:
            return {"message": id}
    raise HTTPException(status_code=404, detail="Campaign not found")
        
    