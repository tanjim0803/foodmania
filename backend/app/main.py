from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import routers

app = FastAPI(
    title="FoodMania", description="A Food Delivery Management App", version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
 )


@app.get("/")
async def root():
    return {"message": "Welcome to FoodMania App"}


app.include_router(routers)
