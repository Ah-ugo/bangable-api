from datetime import datetime

from DB.db import videos_db
from fastapi import HTTPException, UploadFile
from typing import List
from models import Video, ObjectId
from utils.cloudinary_upload import uploadVideoToCloud, uploadPosterToCloud

def getAllVideos():
    vid_query = videos_db.find({})
    vid_arr = []

    for video in vid_query:
        vid_arr.append(Video(**video))
    return vid_arr

def getVideoById(id):
    vid_query = videos_db.find_one({"_id": ObjectId(id)})
    if vid_query:
        vid_query["_id"] = str(vid_query["_id"])
        return vid_query
    else:
        raise HTTPException(status_code=404, detail=f"Video with id {id} not found")

def getVideoByTitle(title):
    vid_query = videos_db.find({"title": {"$regex": title, "$options": "i"}})
    vid_arr = []

    for video in vid_query:
        if vid_query:
            vid_query["_id"] = str(vid_query["_id"])
            vid_arr.append(Video(**video))
            return vid_arr
        else:
            raise HTTPException(status_code=404, detail=f"Video with title {title} not found")


async def AddVideo(title: str, video: UploadFile, poster: UploadFile, description: str, category: str, tags: List[str]):

    video_url = await uploadVideoToCloud(video)
    poster_url = await uploadPosterToCloud(poster)


    add_dict = {
        "title": title,
        "video": video_url,
        "poster": poster_url,
        "description": description,
        "category": category,
        "tags": tags
    }


    add_query = videos_db.insert_one(add_dict)
    get_inserted_video = videos_db.find_one({"_id": ObjectId(add_query.inserted_id)})

    get_inserted_video["_id"] = str(get_inserted_video["_id"])

    return get_inserted_video

def UpdateVideo(id, body):
    update_data = {k: v for k, v in body.dict().items() if v is not None}
    vid_query = videos_db.find_one({"_id": ObjectId(id)})

    if vid_query:
        if "tags" not in update_data:
            update_data["tags"] = vid_query.get("tags", [])
        update_data["last_modified"] = datetime.utcnow()
        videos_db.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        updated_vid = videos_db.find_one({"_id": ObjectId(id)})
        updated_vid["_id"] = str(updated_vid["_id"])
        return updated_vid
    else:
        raise HTTPException(status_code=404, detail=f"Video with id {id} not found")