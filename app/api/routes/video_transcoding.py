import os
import jinja2
from io import BytesIO
from typing import List
from app.core.config import settings
from app.common.utils.files import upload_file
from starlette.templating import Jinja2Templates
from app.api.models.ffmpeg import ExportQualities
from app.api.services.ffmpeg.multimedia import Multiplexer
from fastapi import APIRouter, File, UploadFile, Query, Request
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse

templates = Jinja2Templates(directory="templates")
playlist_template = jinja2.Environment(loader=jinja2.PackageLoader('data', 'playlist'), )

router = APIRouter(tags=['ffmpeg'])


def server_bytes_as_file(contents: bytes) -> StreamingResponse:
    response = BytesIO()
    response.write(contents)
    response.seek(0)
    return StreamingResponse(response)


@router.get("/playlists/{video_name}.m3u8")
async def get_playlist(video_name: str):
    try:
        template = playlist_template.get_template(f"{video_name}.m3u8")
    except jinja2.exceptions.TemplateNotFound:
        return HTMLResponse(status_code=404)
    formatted_template = template.render(video_path=f"../video/{video_name}")
    return server_bytes_as_file(formatted_template.encode("utf-8"))


@router.get("/video/{video_name}/{segment_number}.ts", response_class=FileResponse)
async def get_segment(video_name: str, segment_number: int):

    segment = os.path.join(settings.BASE_PATH.parent, 'data', 'video', video_name, f"{segment_number}.ts")
    if not segment:
        return HTMLResponse(status_code=404)
    return segment


@router.get("/{video_name}.html", response_class=HTMLResponse)
def get_item(request: Request, video_name: str):
    try:
        playlist_template.get_template(f"{video_name}.m3u8")
    except jinja2.exceptions.TemplateNotFound:
        return templates.TemplateResponse(request=request, name='404_form.html')

    return templates.TemplateResponse(
        request=request, name='video.html', context={
            "request": request, "video_name": video_name, 'api_version': settings.API_V1_STR
        }
    )


@router.post("/transcode")
def convert_to_all_formats(quality: List[ExportQualities] = Query(), file: UploadFile = File(...)):
    _qualities = [q.value for q in quality]
    upload_file(file, settings.UPLOAD_DIR)
    mm = Multiplexer()
    mm.input_file_name = os.path.join(settings.UPLOAD_DIR, file.filename)
    mm.output_file_name = os.path.join(settings.OUTPUT_DIR, file.filename)
    mm.transcode(_qualities)
    return {"status": "file uploaded successfully"}
