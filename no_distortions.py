import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random

def generate_psychedelic_artwork(output_filename="album_art.jpg", size=1600):
    """
    Generates a 1600x1600 JPEG of a randomized Julia Set fractal
    with a vibrant, custom psychedelic color palette.
    """
    # 1. Randomize the fractal shape parameters
    c_real = random.uniform(-0.85, 0.4)
    c_imag = random.uniform(-0.65, 0.65)
    c = complex(c_real, c_imag)
    
    # 2. Set up the exact grid size
    x = np.linspace(-1.5, 1.5, size)
    y = np.linspace(-1.5, 1.5, size)
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

    # 4. Generate a highly randomized, electric psychedelic palette
    # We mix high-saturation neon colors dynamically
    base_colors = [
        (random.uniform(0.7, 1.0), random.uniform(0.0, 0.3), random.uniform(0.7, 1.0)), # Electric Fuchsia/Pink
        (random.uniform(0.0, 0.3), random.uniform(0.8, 1.0), random.uniform(0.8, 1.0)), # Neon Cyan/Teal
        (random.uniform(0.8, 1.0), random.uniform(0.7, 1.0), random.uniform(0.0, 0.2)), # Acid Yellow/Green
        (random.uniform(0.5, 0.9), random.uniform(0.0, 0.2), random.uniform(0.9, 1.0)), # Deep Purple/Violet
        (0.0, 0.0, 0.0) # Deep black core for trippy contrast
    ]
    # Shuffle order to create chaotic color transitions
    random.shuffle(base_colors)
    psychedelic_cmap = mcolors.LinearSegmentedColormap.from_list("psych", base_colors, N=256)
    
    # 5. Render and save as a 1600x1600 JPEG
    # DPI * Inches must equal exactly 1600 (e.g., 16 inches at 100 DPI)
    fig, ax = plt.subplots(figsize=(16, 16), dpi=100)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1) # Remove all borders
    ax.axis('off')
    
    # Render fractal with our custom trippy palette
    ax.imshow(output, cmap=psychedelic_cmap, extent=[-1.5, 1.5, -1.5, 1.5], origin='lower')
    
    # Save as high-quality JPEG (95% quality minimizes compression artifacts)
    plt.savefig(output_filename, format='jpg', pil_kwargs={'quality': 95}, bbox_inches='tight', pad_inches=0, dpi=100)
    plt.close()
    
    print(f"Psychedelic artwork saved as '{output_filename}' (1600x1600 JPG)")
    print(f"Seed Constant c = {c}")

if __name__ == "__main__":
    generate_psychedelic_artwork()
