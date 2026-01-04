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

class CampaignCreate(SQLModel):
    name: str
    due_date: datetime | None = None    

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
async def read_campaigns(session: SessionDependency):
    data = session.exec(select(Campaign)).all()
    return {"campaigns": data}


@app.get("/campaigns/{id}")
async def read_campaign(id: int, session: SessionDependency):
    data = session.get(Campaign, id)
    if not data:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return {"campaign": data}


@app.post("/campaigns", status_code=201)
async def create_campaign(campaign: CampaignCreate, session: SessionDependency):
    db_campaign = Campaign.model_validate(campaign)
    session.add(db_campaign)
    session.commit()
    session.refresh(db_campaign)
    return {"message": db_campaign}

@app.put("/campaigns/{id}")
async def update_campaign(id: int, campaign: CampaignCreate, session: SessionDependency):
    data = session.get(Campaign, id)
    if not data:
        raise HTTPException(status_code=404, detail="Campaign not found")
    data.name = campaign.name
    data.due_date = campaign.due_date
    session.add(data)
    session.commit()
    session.refresh(data)
    return {"campaign": data}


@app.delete("/campaigns/{id}", status_code=204)
async def delete_campaign(id: int, session: SessionDependency):
    data = session.get(Campaign, id)
    if not data:
        raise HTTPException(status_code=404, detail="Campaign not found")
    session.delete(data)
    session.commit()
    
   