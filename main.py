from datetime import datetime
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
async def create_campaign(request: Request):
    body = await request.json()

    new_campaign = {
        "campaing_id": len(data) + 1,
        "name": body.get("name"),
        "due_date": datetime.now(),
        "created_at": datetime.now(),
    }

    data.append(new_campaign)
    return {"message": new_campaign}
    