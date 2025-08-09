# utils.py
import os

def is_image_file(path):
    supported_exts = [
        ".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".tif", ".webp", ".ico", ".ppm", ".pgm", ".pbm", ".svg"
    ]
    return os.path.splitext(path)[1].lower() in supported_exts