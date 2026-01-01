from fastapi import FastAPI


app = FastAPI(root_path="/api/v1")

@app.get("/campaigns")
async def read_campaigns():
    return {"message": "List of campaigns"}



