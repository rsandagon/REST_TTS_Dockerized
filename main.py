from typing import Union
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
import torch
import re
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("xtts_v2.0.2").to(device)

app = FastAPI(
    title="REST_TTS_Dockerized",
    description="TTS REST API wrapper with FastAPI and Docker, for your text-to-speech needs🤖",
    summary="TTS REST API Dockerized",
    version="0.0.1",
    terms_of_service="https://github.com/rsandagon/REST_TTS_Dockerized/README.md",
    contact={
        "name": "rsandagon",
        "url": "https://github.com/rsandagon",
        "email": "rsandagon.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

class Item(BaseModel):
    name: str
    message: str 

def remove_between_asterisks(text):
  pattern = r"\*.*?\*"
  return re.sub(pattern, "", text)

@app.get("/")
def read_root():
    return {"Hello": "I'm alive!"}


@app.get(
    path="/api/snd"
)
async def post_media_file(name:str='default'):
    return FileResponse("audio/outputs/"+name, media_type="audio/mpeg")

@app.post("/api/tts")
async def post_tts(item: Item):
    now = datetime.now()
    nowstr = now.strftime("%m%d%Y_%H%M%S")
    outname = item.name+nowstr+".wav"
    srcname = item.name+".wav"

    tts.tts_to_file(text=remove_between_asterisks(item.message), speaker_wav="audio/voices/"+srcname, language="en", file_path="audio/outputs/"+outname)
    # or return FileResponse of the wav if machine is fast enough
    # return FileResponse("audio/outputs/"+outname, media_type="audio/mpeg")
    return {"file":outname}