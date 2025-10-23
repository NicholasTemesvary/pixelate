import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class PixelateApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Live Pixelator")
        self.master.geometry("800x700")
        self.image = None
        self.original_image = None
        self.tk_img = None
        self.image_path = None

        # === UI Setup ===
        self.frame_controls = tk.Frame(master)
        self.frame_controls.pack(side=tk.TOP, pady=10)

        self.btn_load = tk.Button(self.frame_controls, text="Load Image", command=self.load_image)
        self.btn_load.grid(row=0, column=0, padx=10)

        tk.Label(self.frame_controls, text="Pixel Size:").grid(row=0, column=1)
        self.pixel_slider = tk.Scale(self.frame_controls, from_=2, to=100, orient=tk.HORIZONTAL, command=self.update_preview)
        self.pixel_slider.set(16)
        self.pixel_slider.grid(row=0, column=2, padx=10)

        tk.Label(self.frame_controls, text="Aspect Width:").grid(row=0, column=3)
        self.aspect_w = tk.Scale(self.frame_controls, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, command=self.update_preview)
        self.aspect_w.set(1.0)
        self.aspect_w.grid(row=0, column=4, padx=10)

        tk.Label(self.frame_controls, text="Aspect Height:").grid(row=0, column=5)
        self.aspect_h = tk.Scale(self.frame_controls, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, command=self.update_preview)
        self.aspect_h.set(1.0)
        self.aspect_h.grid(row=0, column=6, padx=10)

        self.btn_save = tk.Button(self.frame_controls, text="Save Pixelated", command=self.save_image)
        self.btn_save.grid(row=0, column=7, padx=10)

        self.canvas = tk.Label(master)
        self.canvas.pack(pady=20)

    def load_image(self):
        path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if not path:
            return
        self.image_path = path
        self.original_image = Image.open(path).convert("RGB")
        self.update_preview()

    def update_preview(self, event=None):
        if not self.original_image:
            return
        pixel_size = self.pixel_slider.get()
        aspect_x = self.aspect_w.get()
        aspect_y = self.aspect_h.get()
        self.image = self.pixelate_image(self.original_image, pixel_size, (aspect_x, aspect_y))
        self.display_image(self.image)

    def pixelate_image(self, img, pixel_size, aspect_ratio):
        width, height = img.size
        new_width = int(width * aspect_ratio[0])
        new_height = int(height * aspect_ratio[1])
        img = img.resize((new_width, new_height))

        # Downscale & upscale for pixelation
        small = img.resize(
            (max(1, new_width // pixel_size), max(1, new_height // pixel_size)),
            resample=Image.BILINEAR
        )
        result = small.resize((new_width, new_height), Image.NEAREST)
        return result

    def display_image(self, img):
        # Resize for window preview
        max_size = (700, 500)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.config(image=self.tk_img)

    def save_image(self):
        if not self.image or not self.image_path:
            messagebox.showwarning("No image", "Please load and pixelate an image first.")
            return
        base, ext = os.path.splitext(self.image_path)
        output_path = f"{base}_pixelated{ext}"
        self.image.save(output_path)
        messagebox.showinfo("Saved", f"Pixelated image saved as:\n{output_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PixelateApp(root)
    root.mainloop()
