import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors mcolors
import random
import argparse

def apply_kaleidoscope(data):
    """
    Applies an 8-way kaleidoscope mirror effect to a 2D square matrix.
    """
    size = data.shape[0]
    half = size // 2
    
    # Extract the top-left quadrant
    quad = data[0:half, 0:half]
    
    # Create an 8-way symmetry by mirroring across horizontal, vertical, and diagonal axes
    top_left = np.tril(quad) + np.triu(quad.T, 1)
    top_right = np.fliplr(top_left)
    top_half = np.hstack((top_left, top_right))
    bottom_half = np.flipud(top_half)
    
    return np.vstack((top_half, bottom_half))

def generate_psychedelic_artwork(output_filename="album_art.jpg", size=1600, scaling=1.0, ripples=False, kaleidoscope=False):
    """
    Generates a 1600x1600 JPEG of a randomized Julia Set fractal with custom distortions and scaling.
    """
    # 1. Randomize the fractal shape parameters
    c_real = random.uniform(-0.85, 0.4)
    c_imag = random.uniform(-0.65, 0.65)
    c = complex(c_real, c_imag)
    
    # 2. Set up the exact grid size incorporating user-defined scaling (zoom out/in)
    # Higher scaling values zoom out to show more fractal structure, lower zooms in
    bound = 1.5 * scaling
    x = np.linspace(-bound, bound, size)
    y = np.linspace(-bound, bound, size)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y
    
    # Track iterations before escape
    max_iter = 120
    output = np.zeros(Z.shape, dtype=float)
    mask = np.ones(Z.shape, dtype=bool)
    
    # 3. Compute fractal using vectorized operations
    for i in range(max_iter):
        Z[mask] = Z[mask]**2 + c
        escaped = (np.abs(Z) > 2.0) & mask
        output[escaped] = i
        mask[escaped] = False
        
    output[mask] = max_iter

    # 4. Optional Distortion: Concentric color wave ripples
    if ripples:
        # Calculate distance matrix from center to create waves
        dist_from_center = np.sqrt(X**2 + Y**2)
        # Apply a high-frequency sine wave modulation to the raw iteration data
        output = (np.sin(output * 0.4 + dist_from_center * 5.0) + 1.0) * (max_iter / 2.0)

    # 5. Optional Distortion: Kaleidoscope mirror effect
    if kaleidoscope:
        output = apply_kaleidoscope(output)

    # 6. Generate a highly randomized, electric psychedelic palette
    base_colors = [
        (random.uniform(0.7, 1.0), random.uniform(0.0, 0.3), random.uniform(0.7, 1.0)), # Electric Fuchsia
        (random.uniform(0.0, 0.3), random.uniform(0.8, 1.0), random.uniform(0.8, 1.0)), # Neon Cyan
        (random.uniform(0.8, 1.0), random.uniform(0.7, 1.0), random.uniform(0.0, 0.2)), # Acid Yellow
        (random.uniform(0.5, 0.9), random.uniform(0.0, 0.2), random.uniform(0.9, 1.0)), # Deep Purple
        (0.0, 0.0, 0.0) # High-contrast black core
    ]
    random.shuffle(base_colors)
    psychedelic_cmap = mcolors.LinearSegmentedColormap.from_list("psych", base_colors, N=256)
    
    # 7. Render and save as a 1600x1600 JPEG
    fig, ax = plt.subplots(figsize=(16, 16), dpi=100)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1) # Strip borders
    ax.axis('off')
    
    ax.imshow(output, cmap=psychedelic_cmap, extent=[-bound, bound, -bound, bound], origin='lower')
    
    plt.savefig(output_filename, format='jpg', pil_kwargs={'quality': 95}, bbox_inches='tight', pad_inches=0, dpi=100)
    plt.close()
    
    print(f"Success! Saved: '{output_filename}' (1600x1600 JPG)")
    print(f"Settings -> Scaling: {scaling} | Ripples: {ripples} | Kaleidoscope: {kaleidoscope}")

if __name__ == "__main__":
    # Command line argument parser setup
    parser = argparse.ArgumentParser(description="Generate psychedelic fractal album artwork.")
    
    parser.add_argument("-o", "--output", type=str, default="album_art.jpg", 
                        help="Output filename (default: album_art.jpg)")
    
    parser.add_argument("-s", "--scaling", type=float, default=1.0, 
                        help="Fractal view scaling factor. >1.0 zooms out, <1.0 zooms in. (default: 1.0)")
    
    parser.add_argument("--ripples", action="store_true", 
                        help="Enable concentric color wave ripple distortion")
    
    parser.add_argument("--kaleidoscope", action="store_true", 
                        help="Enable 8-way kaleidoscope mirroring effect")
    
    args = parser.parse_args()
    
    generate_psychedelic_artwork(
        output_filename=args.output,
        scaling=args.scaling,
        ripples=args.ripples,
        kaleidoscope=args.kaleidoscope
    )
