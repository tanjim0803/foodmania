from fastapi import FastAPI
from app.api.routes import routers

app = FastAPI(
    title="FoodMania", description="A Food Delivery Management App", version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "Welcome to FoodMania App"}


app.include_router(routers)
