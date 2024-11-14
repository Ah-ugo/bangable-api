from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Routers import video_route, auth_route

app = FastAPI(
    title="Bangable",
    description="Bangable API documentation developed by Ahuekwe Prince Ugochukwu.",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video_route.router, prefix="/video", tags=["Videos"])
app.include_router(auth_route.router, prefix="/user", tags=["Manage User"])
