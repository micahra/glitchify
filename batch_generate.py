import os
import random

# Change this to 20 if you want exactly 20 copies
TOTAL_COVERS = 20

print(f"🚀 Starting categorized batch generation of {TOTAL_COVERS} unique covers...\n")

for i in range(1, TOTAL_COVERS + 1):
    # 1. Randomly decide which distortions to combine
    ripples_flag = random.choice(["", "--ripples"])
    kaleidoscope_flag = random.choice(["", "--kaleidoscope"])
    
    # 2. Determine the correct subfolder based on active flags
    if ripples_flag and kaleidoscope_flag:
        folder_name = "combined_distortions"
    elif ripples_flag:
        folder_name = "ripples_only"
    elif kaleidoscope_flag:
        folder_name = "kaleidoscope_only"
    else:
        folder_name = "raw_fractals"
        
    # Create the subfolder if it doesn't exist yet
    os.makedirs(folder_name, exist_ok=True)
    
    # 3. Define the destination path inside the folder
    filename = os.path.join(folder_name, f"album_art_alt_{i:02d}.jpg")
    
    # 4. Randomize the scaling factor
    scale = round(random.uniform(0.4, 1.6), 2)
    
    # 5. Construct and execute the command string pointing to your script.py engine
    command = f'python script.py -o "{filename}" -s {scale} {ripples_flag} {kaleidoscope_flag}'
    
    print(f"Generating [{i}/{TOTAL_COVERS}] -> Saving to '{folder_name}/'")
    print(f"👉 Running: {command}")
    
    os.system(command)

print(f"\n✨ Done! All {TOTAL_COVERS} covers have been generated, embedded with seeds, and sorted.")
