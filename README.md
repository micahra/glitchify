# glitchify
Digital Art for a Digital Age

This program will automatically generate fractal-based artwork, colorize and modify it, then output in a square format for use in Album Artwork.

### Instructions

### Summary of All Commands

Now that everything is bundled into a single script (`script.py`), you can manage your entire workflow directly using the following terminal commands:

1. **Read a Seed from an Existing Image:**
   ```bash
   python script.py --read ripples_only/album_art_alt_05.jpg
   ```

2. **Recreate an Exact Design Using a Extracted Seed:**
   ```bash
   python script.py --cr -0.744340 --ci 0.121330 -s 1.2 --ripples -o perfect_recreation.jpg
   ```

3. **Generate a Single, New Random Artwork Manually:**
   ```bash
   python script.py -s 0.8 --ripples --kaleidoscope -o my_new_art.jpg
   ```

4. **Brainstorm dozens of randomized, sorted variations automatically:**
   ```bash
   python batch_generate.py
   ```

### Using Custom Resolution Flags

You can specify the custom canvas size flag directly using `-r` or `--resolution` followed by your desired width/height value:

* **Generate a high-res print master (3000x3000px):**
  ```bash
  python script.py -r 3000 -o print_master.jpg
  ```

* **Generate a lightweight thumbnail layout (800x800px) with distortions:**
  ```bash
  python script.py -r 800 --ripples --kaleidoscope -o thumbnail.jpg
  ```


### Folder Architecture Created
Once you run `python batch_generate.py`, your workspace directory will instantly look like this:

```text
📁 Your_Project_Directory/
│
├── 📜 script.py                  # Your main fractal engine
├── 📜 batch_generate.py          # The automation file above
│
├── 📁 raw_fractals/              # Standard psychedelic fractals
│   └── album_art_alt_04.jpg
│
├── 📁 ripples_only/              # Concentric color wave variations
│   └── album_art_alt_01.jpg
│
├── 📁 kaleidoscope_only/         # Mirrored symmetry variations
│   └── album_art_alt_02.jpg
│
└── 📁 combined_distortions/      # Chaos zone (Both ripples & mirror on)
    └── album_art_alt_03.jpg
```
