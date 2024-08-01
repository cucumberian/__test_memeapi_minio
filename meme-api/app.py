import fastapi
import uvicorn
from router.meme import meme_router

app = fastapi.FastAPI()
app.include_router(router=meme_router, prefix="/memes")


if __name__ == "__main__":
    uvicorn.run(app="app:app", host="0.0.0.0", port=8000, reload=True)
