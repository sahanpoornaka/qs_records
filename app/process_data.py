import PIL.Image as Image
import io
import traceback

from deta import Deta
from fastapi import UploadFile
from starlette.responses import StreamingResponse
from .Pin import Pin

# initialize with a project key
deta = Deta("c06xk2uq_YSXPpiHNhKPBNHBG9EDdkCHWGDfDrGhL")
drive = deta.Drive("images")

WIDTH = 1600
HEIGHT = 900

DB_NAME = "records"


# def convert_to_image(binary_data):
#     img = Image.open(io.BytesIO(binary_data))
#     resized_img = img.resize((WIDTH, HEIGHT))
#     return resized_img
#     # resized_img.show()


def add_record_to_db(img_name, width, height, project_name: str, level_name: str, element_name: str):
    try:
        db = deta.Base(DB_NAME)

        project_name = project_name.lower().strip()
        level_name = level_name.lower().strip()
        element_name = element_name.lower().strip()

        rec_key = project_name + "_" + level_name + "_" + element_name

        db.insert({
            "key": rec_key,
            "project_name": project_name,
            "level_name": level_name,
            "element_name": element_name,
            "img_name": img_name,
            "img_dims": {"width": width, "height": height},
            "pins": [],
        })

    except Exception as e:
        print("Oops!", e.__class__, "occurred.")
        print(traceback.format_exc())
        return {"message": "Error Occurred while adding the Record"}

    return {"message": "Record Added Successfully"}


def get_record_from_db(rec_key: str):
    db = deta.Base(DB_NAME)
    item = db.get(rec_key)

    if item:
        return item

    return {}


def add_pin(rec_key: str, pin: Pin):
    db = deta.Base(DB_NAME)
    existing_data = get_record_from_db(rec_key)

    if len(existing_data["pins"]) > 0:
        existing_data["pins"] = existing_data["pins"] + [pin.dict()]
    else:
        existing_data["pins"] = [pin.dict()]

    print(existing_data)
    db.put(existing_data, rec_key)
    return {"message": "Success"}
