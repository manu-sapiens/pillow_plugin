# --------------- SHARED ---------------------------------------------------
import sys
from typing import List, Any
sys.path.append('.')  # Add the current directory to the sys path
sys.path.append('utils')  # Add the utils directory to the sys path

from utils.omni_utils_http import CdnResponse, ImageMeta, create_api_route, plugin_main, init_plugin
from pydantic import BaseModel
endpoints = []
app, router = init_plugin()
# ---------------------------------------------------------------------------
plugin_module_name = "Plugins.pillow_plugin.pillow" 

# ---------------------------------------------------
# --------------- PILLOW RESIZE ---------------------
# ---------------------------------------------------
ENDPOINT_PILLOW_RESIZE = "/pillow/resize"

class PillowResize_Input(BaseModel):
    images: List[CdnResponse]
    width: int
    height: int
    resample_method: str
    nearest_64: bool
    limit: bool

    class Config:
        schema_extra = {
            "title": "Pillow: Resize an Image"
        }

class PillowResize_Response(BaseModel):
    media_array: List[CdnResponse]
    width_array: List[int]
    height_array: List[int]
    json_array: List[ImageMeta]

    class Config:
        schema_extra = {
            "title": "Resize Output"
        }

PillowResize_Post = create_api_route(
    app=app,
    router=router,
    context=__name__,
    endpoint=ENDPOINT_PILLOW_RESIZE,
    input_class=PillowResize_Input,
    response_class=PillowResize_Response,
    handle_post_function="PillowResize_HandlePost",
    plugin_module_name=plugin_module_name,
)

# ---------------------------------------------------
# --------------- PILLOW FILTER ---------------------
# ---------------------------------------------------
ENDPOINT_PILLOW_FILTER = "/pillow/filter"

class PillowFilter_Input(BaseModel):
    images: List[CdnResponse]
    filter: str

    class Config:
        schema_extra = {
            "title": "Pillow: Apply a filter to an Image"
        }

class PillowFilter_Response(BaseModel):
    media_array: List[CdnResponse]
    class Config:
        schema_extra = {
            "title": "Media Response"
        }        

PillowFilter_Post = create_api_route(
    app=app,
    router=router,
    context=__name__,
    endpoint=ENDPOINT_PILLOW_FILTER,
    input_class=PillowFilter_Input,
    response_class=PillowFilter_Response,
    handle_post_function="PillowFilter_HandlePost",
    plugin_module_name=plugin_module_name,
)


# ---------------------------------------------------
# --------------- PILLOW TEXT - ---------------------
# ---------------------------------------------------
ENDPOINT_PILLOW_TEXT = "/pillow/text"

class PillowText_Input(BaseModel):
    images: List[CdnResponse]
    coordinate_x: int
    coordinate_y: int
    text: str
    fill_color: str
    horizontal_anchor_alignment: str
    vertical_anchor_alignment: str
    font_name: str
    font_size: int
    mode: str

    class Config:

        schema_extra = {
            "title": "Pillow: Generate a text in an image"
        }

class PillowText_Response(BaseModel):
    media_array: List[CdnResponse]
    class Config:
        schema_extra = {
            "title": "Images"
        }

PillowText_Post = create_api_route(
    app=app,
    router=router,
    context=__name__,
    endpoint=ENDPOINT_PILLOW_TEXT,
    input_class=PillowText_Input,
    response_class=PillowText_Response,
    handle_post_function="PillowText_HandlePost",
    plugin_module_name=plugin_module_name,
)

# ---------------------------------------------------
# --------------- PILLOW REMOVE ALPHA ---------------------
# ---------------------------------------------------
ENDPOINT_PILLOW_REMOVE_ALPHA = "/pillow/remove_alpha"

class PillowRemoveAlpha_Input(BaseModel):
    images: List[CdnResponse]
    mode: str
    fill_color: str
    threshold: int

    class Config:
        schema_extra = {
            "title": "Pillow: Remove Alpha from an Image"
        }

class PillowRemoveAlpha_Response(BaseModel):
    media_array: List[CdnResponse]
    
    class Config:
        schema_extra = {
            "title": "Media Response"
        }        

PillowRemoveAlpha_Post = create_api_route(
    app=app,
    router=router,
    context=__name__,
    endpoint=ENDPOINT_PILLOW_REMOVE_ALPHA,
    input_class=PillowRemoveAlpha_Input,
    response_class=PillowRemoveAlpha_Response,
    handle_post_function="PillowRemoveAlpha_HandlePost",
    plugin_module_name=plugin_module_name,
)

endpoints = [ENDPOINT_PILLOW_RESIZE, ENDPOINT_PILLOW_FILTER, ENDPOINT_PILLOW_TEXT, ENDPOINT_PILLOW_REMOVE_ALPHA]

# --------------- SHARED ---------------------------------------------------
plugin_main(app, __name__, __file__)
# --------------------------------------------------------------------------