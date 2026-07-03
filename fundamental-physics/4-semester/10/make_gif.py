import os
import glob
import subprocess
from PIL import Image
from pathlib import Path

def build_and_show(dir_name='frames', out_file='simulation.gif'):
  base_dir = Path(__file__).parent.absolute()
  frames_dir = base_dir / dir_name
  output_path = base_dir / out_file
  
  ps_files = sorted(glob.glob(str(frames_dir / 'frame_*.ps')))
  
  if not ps_files:
    return

  imgs = []
  for f_path in ps_files:
    ps_path = Path(f_path)
    temp_png = ps_path.with_suffix('.png')

    print(f"Processing {ps_path.name}...")
    
    cmd = [
      'convert', 
      '-density', '150', 
      str(ps_path), 
      '-rotate', '90',
      '-background', 'white', 
      '-alpha', 'remove', 
      str(temp_png)
    ]
    
    try:
      subprocess.run(cmd, check=True)
      if temp_png.exists():
        img = Image.open(temp_png).convert("RGB")
        imgs.append(img)
        os.remove(temp_png)
    except:
      continue

  if not imgs:
    return

  imgs[0].save(
    output_path,
    save_all=True,
    append_images=imgs[1:],
    duration=60,
    loop=0
  )

if __name__ == "__main__":
  build_and_show()