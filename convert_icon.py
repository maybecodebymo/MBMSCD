from PIL import Image
import os

def convert_to_ico(source, target):
    try:
        img = Image.open(source)
        img.save(target, format='ICO', sizes=[(256, 256)])
        print(f"Successfully converted {source} to {target}")
    except Exception as e:
        print(f"Error converting image: {e}")

if __name__ == "__main__":
    if os.path.exists("logo.png"):
        convert_to_ico("logo.png", "logo.ico")
    else:
        print("logo.png not found!")
