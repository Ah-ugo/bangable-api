from fastapi import APIRouter, Form, UploadFile, File
from typing import List
from Services.video_service import getAllVideos, getVideoById, getVideoByTitle, AddVideo, UpdateVideo
from models import VideoBase
router = APIRouter()

@router.get("/")
def get_all_videos():
    return getAllVideos()

@router.get("/{id}")
def get_video_by_id(id: str):
    return getVideoById(id)

@router.get("/videos/{title}")
def get_video_by_title(title: str):
    return getVideoByTitle(title)

@router.post("/")
async def add_video(
    title: str = Form(...),
    video: UploadFile = File(...),
    poster: UploadFile = File(...),
    description: str = Form(...),
    category: str = Form(...),
    tags: List[str] = Form(...)
):
    return await AddVideo(title, video, poster, description, category, tags)


@router.patch("/{id}")
def update_video(id: str, body: VideoBase):
    return UpdateVideo(id, body)
