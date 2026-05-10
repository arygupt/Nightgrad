from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import imagetens
a = imagetens.ImageTens()

print(a.load_image_to_tiny('/Users/aryangupta/programming/blackguard/nightgrad/compinf/dark.avif'))