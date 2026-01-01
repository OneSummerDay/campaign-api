from datetime import datetime
from typing import Any
from fastapi import FastAPI, HTTPException, Request


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
            return {"message": campaign}
    raise HTTPException(status_code=404, detail="Campaign not found")


@app.post("/campaign")
async def create_campaign(body: dict[str, Any]):

    new_campaign = {
        "campaing_id": len(data) + 1,
        "name": body.get("name"),
        "due_date": datetime.now(),
        "created_at": datetime.now(),
    }

    data.append(new_campaign)
    return {"message": new_campaign}


@app.put("/campaign/{id}")
async def update_campaign(id: int, body: dict[str, Any]):
    for index, campaign in enumerate(data):
        if campaign.get("campaing_id") == id:
            
            update_campaign = {
                "campaing_id": id,
                "name": body.get("name"),
                "due_date": datetime.now(),
                "created_at": campaign.get("created_at"),
            }

            data[index] = update_campaign
            return {"message": update_campaign}
    raise HTTPException(status_code=404, detail="Campaign not found")