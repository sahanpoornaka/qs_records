from fastapi import FastAPI, File, Form, UploadFile
from starlette.responses import HTMLResponse, StreamingResponse

from .Pin import Pin
from deta import Deta
import PIL.Image as Image

# import uvicorn

from fastapi.middleware.cors import CORSMiddleware
from .process_data import add_record_to_db, get_record_from_db, add_pin

from tempfile import TemporaryFile

app = FastAPI()

# initialize with a project key
deta = Deta("c06xk2uq_YSXPpiHNhKPBNHBG9EDdkCHWGDfDrGhL")
drive = deta.Drive("images")

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000/*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/")
# async def root():
# return {"message": "API is Working"}


@app.get("/", response_class=HTMLResponse)
def render():
    return """
    <form action="/upload" enctype="multipart/form-data" method="post">
        <div>Project Name:<input id="project_name" name="project_name" type="text"></div>
        <div>Level Name:<input id="level_name" name="level_name" type="text"></div>
        <div>Element Name:<input id="element_name" name="element_name" type="text"></div>
        <div>Drawing:<input name="file" type="file"></div>
        <div><input type="submit"></div>
    </form>
    """


#
# fp = TemporaryFile()
#
# img = Image.new("RGB", (100, 100))
# img.save(fp, "PNG")

@app.post("/upload")
def upload_img(project_name: str = Form(), level_name: str = Form(), element_name: str = Form(),
               file: UploadFile = File(...)):
    name = file.filename
    # f = file.file

    img = Image.open(file.file)
    width, height = img.size

    fp = TemporaryFile()
    img.save(fp, "PNG")
    fp.seek(0)
    res = drive.put(name, fp)
    fp.close()

    add_record_to_db(name, width, height, project_name, level_name, element_name)
    return res
    # return "Success"


@app.get("/download/{name}")
def download_img(name: str):
    res = drive.get(name)
    return StreamingResponse(res.iter_chunks(1024), media_type="image/png")


@app.get("/get_data/{key}")
def get_data(key: str):
    return get_record_from_db(key)


@app.post("/add_pin/{rec_key}")
def add_pin_api(rec_key: str, pin: Pin):
    return add_pin(rec_key, pin)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
