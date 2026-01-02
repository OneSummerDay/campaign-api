from contextlib import asynccontextmanager
from datetime import datetime
from typing import Annotated, Any
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, SQLModel, Session, create_engine, select


class Campaign(SQLModel, table=True):
    campaing_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    due_date: datetime | None = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.now, index=True)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)   


def get_session():
    with Session(engine) as session:
        yield session

SessionDependency = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
        if not session.exec(select(Campaign)).first():
            session.add_all([
                Campaign(name="Campaign 1", due_date=datetime.now()),
                Campaign(name="Campaign 2", due_date=datetime.now()),
            ])
            session.commit()
            
    yield


app = FastAPI(root_path="/api/v1", lifespan=lifespan)

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


@app.post("/campaigns")
async def create_campaign(body: dict[str, Any]):

    new_campaign = {
        "campaing_id": len(data) + 1,
        "name": body.get("name"),
        "due_date": datetime.now(),
        "created_at": datetime.now(),
    }

    data.append(new_campaign)
    return {"message": new_campaign}


@app.put("/campaigns/{id}")
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


@app.delete("/campaigns/{id}")
async def delete_campaign(id: int):
    for index, campaign in enumerate(data):
        if campaign.get("campaing_id") == id:
            data.pop(index)
            return {"message": "Campaign deleted successfully"}
    raise HTTPException(status_code=404, detail="Campaign not found")