from fastapi import APIRouter
from fastapi import File
from fastapi import UploadFile


meme_router = APIRouter()


@meme_router.get("")
def get_memes():
    return []


@meme_router.get("/{id:str}")
def get_meme(id: str):
    return {}


@meme_router.post("")
async def post_meme(file: UploadFile = File(...)):
    return file.filename


@meme_router.put("/{id:str}")
def put_meme(id: str, meme):
    return meme


@meme_router.delete("/{id:str}")
def delete_meme(id: str):
    return {}
