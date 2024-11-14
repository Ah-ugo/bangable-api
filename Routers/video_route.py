from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException
from typing import List
from Services.video_service import getAllVideos, getVideoById, getVideoByTitle, AddVideo, UpdateVideo, deleteVideo
from models import VideoBase, User
from Services.auth_service import get_current_user, verify_admin
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
    tags: List[str] = Form(...),
current_user: User = Depends(get_current_user)

):
    return await AddVideo(title, video, poster, description, category, tags, uploader= current_user.id)


@router.patch("/{id}")
async def update_video(
    id: str,
    body: VideoBase,
    current_user: User = Depends(get_current_user)
):
    try:
        updated_video = UpdateVideo(id=id, body=body, current_user=current_user)
        return {"message": "Video updated successfully", "video": updated_video}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id}")
def delete_video(id:str, current_user: User = Depends(get_current_user)):
    return deleteVideo(id, current_user=current_user)