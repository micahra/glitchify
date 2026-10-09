import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random
import argparse
import os
import sys
from PIL import Image

def apply_kaleidoscope(data):
    """Applies an 8-way kaleidoscope mirror effect to a 2D square matrix."""
    size = data.shape[0]
    half = size // 2
    quad = data[0:half, 0:half]
    top_left = np.tril(quad) + np.triu(quad.T, 1)
    top_right = np.fliplr(top_left)
    top_half = np.hstack((top_left, top_right))
    bottom_half = np.flipud(top_half)
    return np.vstack((top_half, bottom_half))

def read_metadata_from_file(image_path):
    """Reads and parses the embedded fractal parameters from a JPEG file comment."""
    try:
        img = Image.open(image_path)
        comment = img.info.get("comment", b"").decode("utf-8")
        img.close()
        
        if comment:
            print(f"\n🔍 Decoded parameters for: {image_path}")
            print("-" * 50)
            parts = comment.split("|")
            for part in parts:
                print(f"  {part}")
            print("-" * 50)
            print(f"\n💡 To recreate this layout exactly, copy the variables above into your command flags.")
        else:
            print(f"❌ No fractal tracking seed found in '{image_path}'.")
    except Exception as e:
        print(f"An error occurred reading the file: {e}")

def generate_psychedelic_artwork(output_filename="album_art.jpg", size=1600, scaling=1.0, 
                                 ripples=False, kaleidoscope=False, forced_cr=None, forced_ci=None):
    """Generates a square JPEG at custom dimensions, injecting math strings directly into its metadata."""
    
    # 1. Shape Parameters: Check if user provided a specific mathematical seed
    if forced_cr is not None and forced_ci is not None:
        c_real = forced_cr
        c_imag = forced_ci
        print(f"🔮 Recreating design from fixed seed: c = {complex(c_real, c_imag)}")
    else:
        c_real = random.uniform(-0.85, 0.4)
        c_imag = random.uniform(-0.65, 0.65)
        print(f"🎲 Generated new random seed: c = {complex(c_real, c_imag)}")
        
    c = complex(c_real, c_imag)
    
    # 2. Set up the grid canvas structure based on user scaling values
    bound = 1.5 * scaling
    x = np.linspace(-bound, bound, size)
    y = np.linspace(-bound, bound, size)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    max_iter = 120
    output = np.zeros(Z.shape, dtype=float)
    mask = np.ones(Z.shape, dtype=bool)
    
    # 3. Compute fractal structure
    for i in range(max_iter):
        Z[mask] = Z[mask]**2 + c
        escaped = (np.abs(Z) > 2.0) & mask
        output[escaped] = i
        mask[escaped] = False
    output[mask] = max_iter

    # 4. Optional Distortion: Ripples
    if ripples:
        dist_from_center = np.sqrt(X**2 + Y**2)
        output = (np.sin(output * 0.4 + dist_from_center * 5.0) + 1.0) * (max_iter / 2.0)

    # 5. Optional Distortion: Kaleidoscope
    if kaleidoscope:
        output = apply_kaleidoscope(output)

    # 6. Generate a randomized psychedelic color palette
    base_colors = [
        (random.uniform(0.7, 1.0), random.uniform(0.0, 0.3), random.uniform(0.7, 1.0)), 
        (random.uniform(0.0, 0.3), random.uniform(0.8, 1.0), random.uniform(0.8, 1.0)), 
        (random.uniform(0.8, 1.0), random.uniform(0.7, 1.0), random.uniform(0.0, 0.2)), 
        (random.uniform(0.5, 0.9), random.uniform(0.0, 0.2), random.uniform(0.9, 1.0)), 
        (0.0, 0.0, 0.0) 
    ]
    random.shuffle(base_colors)
    psychedelic_cmap = mcolors.LinearSegmentedColormap.from_list("psych", base_colors, N=256)
    
    # 7. Render temporary image canvas mapping layout size dynamically
    temp_filename = "temp_render.jpg"
    dpi = 100
    inches = size / dpi
    
    fig, ax = plt.subplots(figsize=(inches, inches), dpi=dpi)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.axis('off')
    ax.imshow(output, cmap=psychedelic_cmap, extent=[-bound, bound, -bound, bound], origin='lower')
    plt.savefig(temp_filename, format='jpg', pil_kwargs={'quality': 95}, bbox_inches='tight', pad_inches=0, dpi=dpi)
    plt.close()
    
    # 8. Re-open with Pillow to append metadata recipes to the file comment block
    metadata_string = f"c_real={c_real:.6f}|c_imag={c_imag:.6f}|scaling={scaling}|ripples={ripples}|kaleidoscope={kaleidoscope}|resolution={size}"
    
    img = Image.open(temp_filename)
    img.save(output_filename, "JPEG", quality=95, comment=metadata_string.encode('utf-8'))
    img.close()
    
    if os.path.exists(temp_filename):
        os.remove(temp_filename)
        
    print(f"✨ Artwork saved successfully: '{output_filename}' ({size}x{size})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate psychedelic fractal album artwork.")
    
    # Read action flag
    parser.add_argument("--read", type=str, default=None, help="Path to an existing image file to read its embedded seed values.")
    
    # Generation configuration flags
    parser.add_argument("-o", "--output", type=str, default="album_art.jpg", help="Output filename")
    parser.add_argument("-r", "--resolution", type=int, default=1600, help="Resolution dimension for square canvas (e.g. 1600 for 1600x1600)")
    parser.add_argument("-s", "--scaling", type=float, default=1.0, help="Fractal view scaling factor.")
    parser.add_argument("--ripples", action="store_true", help="Enable concentric color wave ripple distortion")
    parser.add_argument("--kaleidoscope", action="store_true", help="Enable 8-way kaleidoscope mirroring effect")
    
    # Re-generation positioning flags
    parser.add_argument("--cr", type=float, default=None, help="Force a manual complex seed real component")
    parser.add_argument("--ci", type=float, default=None, help="Force a manual complex seed imaginary component")
    
    args = parser.parse_args()
    
    # If the user targets an execution check to read metadata, do that and stop
    if args.read is not None:
        read_metadata_from_file(args.read)
        sys.exit(0)
        
    generate_psychedelic_artwork(
        output_filename=args.output,
        size=args.resolution,
        scaling=args.scaling,
        ripples=args.ripples,
        kaleidoscope=args.kaleidoscope,
        forced_cr=args.cr,
        forced_ci=args.ci
    )
