import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import sys
from compressor import compress_image
from settings import DEFAULT_QUALITY

if sys.platform == "darwin":
    from ctypes import cdll

    try:
        appkit = cdll.LoadLibrary("/System/Library/Frameworks/AppKit.framework/AppKit")
        appkit.NSApplication.sharedApplication().setApplicationName_("QuickPress")
    except Exception:
        pass

class ImageCompressorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("QuickPress")
        self.root.geometry("500x450")
        self.image_path = None
        self.image_preview = None

        # Title
        title = tk.Label(self.root, text="QuickPress", font=("Arial", 18, "bold"))
        title.pack(pady=10)

        # Image preview
        self.preview_label = tk.Label(self.root, text="No image selected", width=40, height=10, bg="#eee",
                                      relief="sunken")
        self.preview_label.pack(pady=10)

        # Select image button
        select_btn = tk.Button(self.root, text="Select Image", command=self.select_image)
        select_btn.pack(pady=5)

        # Output format picker
        format_frame = tk.Frame(self.root)
        format_frame.pack(pady=5)
        tk.Label(format_frame, text="Output format:").pack(side=tk.LEFT)
        self.format_var = tk.StringVar(value="JPEG")
        format_options = ["JPEG", "PNG", "WebP", "BMP", "TIFF", "GIF", "ICO"]
        if sys.platform == "darwin":  # macOS
            format_options.remove("WebP")
        format_menu = ttk.OptionMenu(format_frame, self.format_var, format_options[0], *format_options)
        format_menu.pack(side=tk.LEFT)

        # Quality slider
        slider_frame = tk.Frame(self.root)
        slider_frame.pack(pady=5)
        tk.Label(slider_frame, text="Compression Quality:").pack(side=tk.LEFT)
        self.quality_var = tk.IntVar(value=DEFAULT_QUALITY)
        quality_slider = tk.Scale(slider_frame, from_=10, to=100, orient=tk.HORIZONTAL, variable=self.quality_var)
        quality_slider.pack(side=tk.LEFT)

        # Compress & Save button
        compress_btn = tk.Button(self.root, text="Compress & Save", command=self.compress_and_save)
        compress_btn.pack(pady=15)

    def select_image(self):
        # file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")]) // Crashes on Mac, so not using it
        # file_path = filedialog.askopenfile(mode="r", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
        file_path = filedialog.askopenfilename(filetypes=[
            ("JPEG", "*.jpg"), ("PNG", "*.png"), ("WebP", "*.webp"), ("GIF", "*.gif"),
            ("BMP", "*.bmp"), ("TIFF", "*.tiff"), ("ICO", "*.ico")
        ])
        if not file_path:
            return
        self.image_path = file_path
        try:
            img = Image.open(file_path)
            target_height = 150
            original_width, original_height = img.size
            new_width = int(original_width * (target_height / original_height))
            img = img.resize((new_width, target_height))
            self.image_preview = ImageTk.PhotoImage(img)  # type: ignore
            self.preview_label.config(image=self.image_preview, text="", width=350, height=150)
        except Exception as e:
            self.preview_label.config(text="Failed to load image")
            messagebox.showerror("Error", f"Image preview failed: {e}")

    def compress_and_save(self):
        if not self.image_path:
            messagebox.showwarning("No image", "Please select an image first.")
            return
        output_format = self.format_var.get()
        ext_map = {
            "JPEG": ".jpg",
            "PNG": ".png",
            "BMP": ".bmp",
            "GIF": ".gif",
            "TIFF": ".tiff",
            "WebP": ".webp",
            "ICO": ".ico"
        }
        ext = ext_map.get(output_format, ".jpg")
        filetypes = [
            (f"{output_format} files", f"*{ext}"),
            ("All Images", "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.tiff;*.tif;*.webp;*.ico")
        ]
        save_path = filedialog.asksaveasfilename(defaultextension=ext, filetypes=filetypes)
        if not save_path:
            return
        try:
            compress_image(self.image_path, save_path, quality=self.quality_var.get(), format=output_format)
            messagebox.showinfo("Success", f"Image saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run(self):
        self.root.mainloop()
