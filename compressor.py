
from PIL import Image

def compress_image(input_path, output_path, quality=30, format="JPEG"):
    img = Image.open(input_path)
    save_kwargs = {"format": format}
    if format.upper() in ["JPEG", "WEBP"]:
        save_kwargs["quality"] = quality
    img.save(output_path, **save_kwargs)