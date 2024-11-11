import cloudinary
import cloudinary.uploader
from fastapi import HTTPException, UploadFile
import os
from io import BytesIO

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)

async def uploadVideoToCloud(video: UploadFile):
    if video:
        video_content = BytesIO(await video.read())
        try:
            vidQuery = cloudinary.uploader.upload_large(
                video_content,
                folder="Shops",
                resource_type="video",
                filename=video.filename
            )
            return vidQuery.get("url")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Video upload failed: {e}")
    else:
        raise HTTPException(status_code=400, detail="No video file provided")

async def uploadPosterToCloud(img: UploadFile):
    if img:
        img_content = BytesIO(await img.read())
        try:
            posterQuery = cloudinary.uploader.upload(
                img_content,
                folder="Shops",
                filename=img.filename
            )
            return posterQuery.get("url")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Poster upload failed: {e}")
    else:
        raise HTTPException(status_code=400, detail="No poster file provided")
