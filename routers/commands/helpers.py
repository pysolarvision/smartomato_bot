import os
from PIL import Image


def create_folder(base_directory: str, user_id: int) -> None:
    target_folder: str = f'{base_directory}/{user_id}'
    if not os.path.isdir(target_folder):
        os.mkdir(target_folder)


def image_resizer(image_data: str, cut_top: int, cut_bottom: int, new_width: int, new_height: int) -> Image.Image:
    image = Image.open(image_data)
    width, height = image.size
    cropped_image = image.crop((0, cut_top, width, height - cut_bottom))

    resized_image = cropped_image.resize((new_width, new_height))

    return resized_image
