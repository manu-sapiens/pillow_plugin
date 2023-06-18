# --------------- SHARED -------------------------------------------
print(f"RUNNING: {__name__} ")
import sys
sys.path.append('.')  # Add the current directory to the sys path
sys.path.append('utils')  # Add the current directory to the sys path
from utils.omni_utils_misc import omni_get_env
from utils.omni_utils_http import CdnHandler, CdnResponse, ImageMeta, route_commands
routes_info = {}
cdn = CdnHandler()
# ------------------------------------------------------------------
OMNI_TEMP_FOLDER = omni_get_env("OMNI_TEMP_FOLDER")

from PIL import Image, ImageFilter, ImageDraw, ImageFont
import os
from fastapi import HTTPException
import json
# --------------- PILLOW RESIZE ---------------------
from Plugins.pillow_plugin.pillow_plugin import PillowResize_Input,  PillowResize_Response, ENDPOINT_PILLOW_RESIZE 
async def PillowResize_HandlePost(input: PillowResize_Input):
    if True: #try:
        print("------------- resize_image ------------------")
        cdn.announcement()

        if False:
            write_fd = int(serialized_write_pipe.strip())
            print(f"write_fd = {write_fd}")

            input = PillowResize_Input.parse_raw(serialized_input)
            print(f"input = {input}")

        width = input.width
        height = input.height
        resample_method = input.resample_method
        nearest_64 = input.nearest_64
        limit = input.limit

        images = input.images
        print(f"width = {width}")
        print(f"height = {height}")
        print(f"resample_method = {resample_method}")
        print(f"nearest_64 = {nearest_64}")
        print(f"limit = {limit}")       
        print(f"images = {images}")

        cdn_results = await cdn.process(pillow_resize, images, width, height, resample_method, nearest_64,limit)
        print(f"results = {cdn_results}")
        print("\n-----------------------\n")

        width_array = []
        height_array = []
        json_array = []

        for cdn_result in cdn_results:

            size = cdn_result["size"]
            fileName = cdn_result["fileName"]
            mimeType = cdn_result["mimeType"] 
            url = cdn_result["url"]
            ticket = cdn_result["ticket"]
            print(f"ticket = {ticket}")
            meta = cdn_result["meta"]
            print(f"meta = {meta}")

            fid = ticket["fid"]         
            new_width = meta["width"]
            new_height = meta["height"]

            img_data = ImageMeta(
                fid = fid,
                width = new_width,
                height = new_height,
                size = size,
                url = url,
                fileName = fileName,
                mimeType = mimeType
            )

            json_array.append(img_data)

            width_array.append(new_width)
            height_array.append(new_height)

        #

        response = PillowResize_Response(media_array=cdn_results, width_array=width_array, height_array=height_array, json_array=json_array) 
        print(f"response = {response}")
        print("\n-----------------------\n")
        if False:
            with os.fdopen(write_fd, 'wb') as pipe_write:
                pipe_write.write(json.dumps(response).encode())

        return response
    else: #except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
routes_info[ENDPOINT_PILLOW_RESIZE] = (PillowResize_Input, PillowResize_HandlePost)


async def pillow_resize(input_filename: str, width: int, height: int, resample_method: str, nearest_64: bool, limit: bool):
    print(f"-------- action_resize : f={input_filename}")

    image = Image.open(input_filename)
    original_width, original_height = image.size

    if nearest_64:
        max_dim = max(width, height)
        base = round(max_dim / 64) * 64
        if max_dim == original_width:
            height = round(base * (original_height / original_width))
            width = base
        else:
            width = round(base * (original_width / original_height))
            height = base

    if limit and (original_width <= width and original_height <= height):
        response_filename = input_filename
    else:
        resample_methods = {
            "NEAREST": Image.NEAREST,
            "BOX": Image.BOX,
            "BILINEAR": Image.BILINEAR,
            "HAMMING": Image.HAMMING,
            "BICUBIC": Image.BICUBIC,
            "LANCZOS": Image.LANCZOS
        }

        if resample_method not in resample_methods:
            resample_method = "BICUBIC"

        image = image.resize((width, height), resample=resample_methods[resample_method])

        filename, extension = os.path.splitext(os.path.basename(input_filename))
        print(f"filename: {filename}")  # Output: filename: test
        print(f"extension: {extension}")  # Output: extension: .img

        response_filename = os.path.join(OMNI_TEMP_FOLDER, f"{filename}_resized.png")
        image.save(response_filename)  # Save the image before returning

    return response_filename

# --------------- PILLOW FILTER ---------------------
from Plugins.pillow_plugin.pillow_plugin import PillowFilter_Input,  PillowFilter_Response, ENDPOINT_PILLOW_FILTER
async def PillowFilter_HandlePost(input: PillowFilter_Input):
    if True:
        cdn.announcement()
        print("------------- filter ------------------")
        print(f"input = {input}")

        filter_name = input.filter
        input_cdns = input.images
        print(f"filter = {filter_name}")
        input_filenames = await cdn.download_files_from_cdn(input_cdns)
        print(f"input_filenames = {input_filenames}")

        result_filenames = []
        results_cdns = []
        for input_filename in input_filenames:
            result_filename = await pillow_filter(input_filename, filter_name)
            result_filenames.append(result_filename)
            print(f"result_filename = {result_filename}")
        #
        print(f"result_filenames = {result_filenames}")
        if result_filenames != None:  
            results_cdns = await cdn.upload_files_to_cdn(result_filenames)

        # delete the results files from the local storage
        cdn.delete_temp_files(result_filenames)

        return PillowFilter_Response(media_array=results_cdns) 
routes_info[ENDPOINT_PILLOW_FILTER] = (PillowFilter_Input, PillowFilter_HandlePost)

async def pillow_filter(input_filename: str, filter_name: str):
    print(f"-------- action_filter : f={input_filename} filter_name={filter_name}")

    image = Image.open(input_filename)
    # --------------------------------
    if filter_name == "BLUR":
        image = image.filter(ImageFilter.BLUR)
    elif filter_name == "CONTOUR":
        image = image.filter(ImageFilter.CONTOUR)
    elif filter_name == "DETAIL":
        image = image.filter(ImageFilter.DETAIL)
    elif filter_name == "EDGE_ENHANCE":
        image = image.filter(ImageFilter.EDGE_ENHANCE)
    elif filter_name == "EDGE_ENHANCE_MORE":
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    elif filter_name == "EMBOSS":
        image = image.filter(ImageFilter.EMBOSS)
    elif filter_name == "FIND_EDGES":
        image = image.filter(ImageFilter.FIND_EDGES)
    elif filter_name == "SHARPEN":
        image = image.filter(ImageFilter.SHARPEN)
    elif filter_name == "SMOOTH":
        image = image.filter(ImageFilter.SMOOTH)
    elif filter_name == "SMOOTH_MORE":
        image = image.filter(ImageFilter.SMOOTH_MORE)
    else:
        return {"error": "Invalid filter name"}
        
    filename, extension = os.path.splitext(os.path.basename(input_filename))    
    response_filename = os.path.join(OMNI_TEMP_FOLDER, f"{filename}_{filter_name}{extension}")
    image.save(response_filename)  # Save the image before returning

    return response_filename

# --------------- PILLOW TEXT - ---------------------
PILLOW_TEXT_MODE_CREATE_MASK = "CREATE_MASK"
PILLOW_TEXT_MODE_CREATE_ALPHA_TEXT = "CREATE_ALPHA_TEXT"
PILLOW_TEXT_MODE_ADD_TEXT = "ADD_TEXT"
FONTS_DIRECTORY = "integrations/pillow_files/Tests/fonts/"

async def pillow_text(input_filename: str, coordinate_x, coordinate_y, text, fill_color, horizontal_anchor_alignment, vertical_anchor_alignment, font_name, font_size, mode):
    print(f"-------- PillowText_Action : f={input_filename}")

    original_image = Image.open(input_filename).convert("RGBA")
    response_filename = os.path.join(OMNI_TEMP_FOLDER, f"{input_filename}_text.png")
    print(f"response_filename = {response_filename}")
    new_image = None

    if mode == PILLOW_TEXT_MODE_CREATE_MASK:
        fill_color = "white"
        new_image = Image.new("RGBA", original_image.size)

        draw = ImageDraw.Draw(new_image)
        font = ImageFont.truetype(font_name, font_size)
        anchor = horizontal_anchor_alignment + vertical_anchor_alignment
        coordinates = (coordinate_x, coordinate_y)
        draw.text(coordinates, text, fill_color, anchor=anchor, font=font)           
        alpha = new_image.convert("L")
        new_image.putalpha(alpha)               

    elif mode ==  PILLOW_TEXT_MODE_CREATE_ALPHA_TEXT:

        font = ImageFont.truetype(font_name, font_size)
        anchor = horizontal_anchor_alignment + vertical_anchor_alignment
        coordinates = (coordinate_x, coordinate_y)

        mask_fill_color = "white"        
        new_mask = Image.new("RGBA", original_image.size)
        mask_draw = ImageDraw.Draw(new_mask)
        mask_draw.text(coordinates, text, mask_fill_color, anchor=anchor, font=font)    
        alpha = new_mask.convert("L")

        new_image = original_image.copy()
        image_draw = ImageDraw.Draw(new_image) 
        image_draw.text(coordinates, text, fill_color, anchor=anchor, font=font)    
        new_image.putalpha(alpha)
  
    else:
        new_image = original_image.copy()
        draw = ImageDraw.Draw(new_image)
        font = ImageFont.truetype(font_name, font_size)
        anchor = horizontal_anchor_alignment + vertical_anchor_alignment
        coordinates = (coordinate_x, coordinate_y)
        draw.text(coordinates, text, fill_color, anchor=anchor, font=font)    
    #

    new_image.save(response_filename)
    return response_filename

from Plugins.pillow_plugin.pillow_plugin import PillowText_Input,  PillowText_Response, ENDPOINT_PILLOW_TEXT
async def PillowText_HandlePost(input: PillowText_Input):
    if True:
        cdn.announcement()
        print("------------- text ------------------")
        print(f"input = {input}")

        coordinate_x = input.coordinate_x
        coordinate_y = input.coordinate_y
        text = input.text
        fill_color = input.fill_color
        horizontal_anchor_alignment = input.horizontal_anchor_alignment[0]
        vertical_anchor_alignment = input.vertical_anchor_alignment[0]
        font_name = os.path.join(FONTS_DIRECTORY, input.font_name)
        font_size = input.font_size
        mode = input.mode

        # if mode == PILLOW_TEXT_MODE_CREATE_ALPHA_TEXT:
        #     if fill_color == "black": 
        #         fill_color = "white"    
        #         print("[WARNING] Adjusting fill color")

        images = input.images
        print(f"coordinate_x = {coordinate_x}")
        print(f"coordinate_y = {coordinate_y}")
        print(f"text = {text}")
        print(f"fill_color = {fill_color}")
        print(f"horizontal_anchor_alignment = {horizontal_anchor_alignment}")
        print(f"vertical_anchor_alignment = {vertical_anchor_alignment}")
        print(f"font_name = {font_name}")
        print(f"font_size = {font_size}")
        print(f"mode = {mode}")
        print(f"images = {images}")

        cdn_results = await cdn.process(pillow_text, images, coordinate_x, coordinate_y, text, fill_color, horizontal_anchor_alignment, vertical_anchor_alignment, font_name, font_size, mode)
        print(f"results = {cdn_results}")
        print("\n-----------------------\n")

        return PillowText_Response(media_array=cdn_results) 
routes_info[ENDPOINT_PILLOW_TEXT] = (PillowText_Input, PillowText_HandlePost)
# --------------- PILLOW REMOVE ALPHA ---------------------

PILLOW_REMOVEALPHA_MODE_CLIP = "CLIP"
PILLOW_REMOVEALPHA_MODE_REMOVE = "REMOVE"


async def pillow_remove_alpha(input_filename: str, mode: str, fill_color: str, threshold: int):
    print(f"-------- PillowRemoveAlpha_Action : mode={mode}")

    image = Image.open(input_filename)

    if mode == PILLOW_REMOVEALPHA_MODE_REMOVE:
        
        if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
            alpha = image.convert('RGBA').split()[-1]  # Get alpha channel
            bg = Image.new('RGBA', image.size, fill_color)  # Ensure fill_color is RGBA
            bg.paste(image, mask=alpha)  # Paste the image using alpha channel as mask
            image = bg.convert('RGB')  # Convert back to RGB
        #
    elif mode == PILLOW_REMOVEALPHA_MODE_CLIP:
        if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
            image = image.convert('RGBA')
            datas = image.getdata()

            newData = []
            for item in datas:
                if item[3] < threshold:
                    newData.append((item[0], item[1], item[2], 0))
                else:
                    newData.append((item[0], item[1], item[2], 255))
                #
            image.putdata(newData)
        #    
    else:
        return {"error": "Invalid mode"}
    #

    response_filename = os.path.join(OMNI_TEMP_FOLDER, f"{input_filename}_filtered.png")
    image.save(response_filename)  # Save the image before returning

    return response_filename


from Plugins.pillow_plugin.pillow_plugin import PillowRemoveAlpha_Input,  PillowRemoveAlpha_Response, ENDPOINT_PILLOW_REMOVE_ALPHA
async def PillowRemoveAlpha_HandlePost(input: PillowRemoveAlpha_Input):
    if True:
        cdn.announcement()
        print("------------- Remove Alpha ------------------")
        print(f"input = {input}")
        mode = input.mode
        fill_color = input.fill_color
        images = input.images
        threshold = input.threshold
        print(f"fill_color = {fill_color}")
        print(f"mode = {mode}")
        print(f"images = {images}")

        cdn_results = await cdn.process(pillow_remove_alpha, images, mode, fill_color, threshold)
        print(f"results = {cdn_results}")
        print("\n-----------------------\n")

        response = PillowRemoveAlpha_Response(media_array=cdn_results) 
        print(f"response = {response}")
        print("\n-----------------------\n")
        return response
    #
routes_info[ENDPOINT_PILLOW_REMOVE_ALPHA] = (PillowRemoveAlpha_Input, PillowRemoveAlpha_HandlePost)

# --------------- SHARED -------------------------------------------
if __name__ == '__main__':
    route_commands(routes_info, sys.argv)
# ------------------------------------------------------------------