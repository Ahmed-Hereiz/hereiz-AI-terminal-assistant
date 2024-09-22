import os
import shutil
from datetime import datetime
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import tkinter as tk


def save_imgs(imgs_dir, new_imgs_dir):
    os.makedirs(new_imgs_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    img_dirs = []

    for index, img_dir in enumerate(imgs_dir):
        file_type = os.path.splitext(img_dir)[1]
        
        if not file_type:
            raise ValueError(f"File {img_dir} has no extension.")

        new_filename = f"generated_{timestamp}_{index}{file_type}"
        new_filepath = os.path.join(new_imgs_dir, new_filename)

        try:
            shutil.move(img_dir, new_filepath)
        except Exception as e:
            print(f"Error moving {img_dir} to {new_filepath}: {e}")
            continue 
        
        img_dirs.append(new_filepath)

    return img_dirs



def show_images_side_by_side(saved_imgs_dir, images_per_row=2, image_scale=1):

    img_files = [f for f in os.listdir(saved_imgs_dir) if os.path.isfile(os.path.join(saved_imgs_dir, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not img_files:
        print("No images found in the directory.")
        return

    images = [Image.open(os.path.join(saved_imgs_dir, img_file)) for img_file in img_files]
    num_images = len(images)

    if num_images == 1:
        plt.figure(figsize=(image_scale * 4, image_scale * 4))
        plt.imshow(images[0])
        plt.axis('off')  
        plt.tight_layout()
        plt.show()
        return

    num_rows = (num_images + images_per_row - 1) // images_per_row  
    fig, axes = plt.subplots(num_rows, images_per_row, figsize=(image_scale * images_per_row * 4, image_scale * num_rows * 4))
    axes = axes.flatten() if num_images > 1 else [axes]
    
    for i, img in enumerate(images):
        axes[i].imshow(img)
        axes[i].axis('off')  

    for j in range(i + 1, len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()


def sketch_window(output_filename="sketch.png", width=400, height=400):    
    root = tk.Tk()
    root.title("Sketch Window")
    
    canvas = tk.Canvas(root, width=width, height=height, bg="white")
    canvas.pack()

    draw_color = "black"
    drawing = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(drawing)
    
    def paint(event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        canvas.create_line(x1, y1, x2, y2, fill=draw_color, width=3)
        draw.line([x1, y1, x2, y2], fill=draw_color, width=3)

    canvas.bind("<B1-Motion>", paint)

    def save_drawing():
        drawing.save(output_filename)
        root.destroy()

    save_button = tk.Button(root, text="Save Drawing", command=save_drawing)
    save_button.pack()

    root.mainloop()
    
    return output_filename 