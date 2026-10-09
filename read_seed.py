import sys
from PIL import Image

def extract_fractal_metadata(image_path):
    try:
        img = Image.open(image_path)
        # Pull the comment block out of the JPEG headers
        comment = img.info.get("comment", b"").decode("utf-8")
        img.close()
        
        if comment:
            print(f"\n🔍 Found parameters for: {image_path}")
            print("-" * 40)
            parts = comment.split("|")
            for part in parts:
                print(f"  {part}")
            print("-" * 40)
        else:
            print("❌ No fractal tracking seed found in this image file.")
    except Exception as e:
        print(f"An error occurred reading the file: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python read_seed.py path/to/your/image.jpg")
    else:
        extract_fractal_metadata(sys.argv[1])
