### How to run it from your Terminal

1. **Standard Run** (Default zoom, no extra distortions):
   ```bash
   python script.py
   ```

2. **Zoomed In** (Scale down to `0.5` to look closely at details) with **Ripples** enabled:
   ```bash
   python script.py --scaling 0.5 --ripples
   ```

3. **Zoomed Out** (Scale up to `1.5` to see massive outer structures) with **both distortions** on, saved to a custom file:
   ```bash
   python script.py -s 1.5 --ripples --kaleidoscope -o psych_artwork_01.jpg
   ```

