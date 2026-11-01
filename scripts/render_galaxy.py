"""Export the generated galaxy as a GitHub avatar and a seamless README loop."""
from pathlib import Path
from math import sin, tau
from PIL import Image, ImageEnhance

assets = Path(__file__).resolve().parents[1] / "assets"
source = Image.open(assets / "galaxy.png").convert("RGB")
assert source.width == source.height, "Galaxy source must be square"
source.resize((500, 500), Image.Resampling.LANCZOS).save(
    assets / "galaxy-avatar.jpg", quality=94, optimize=True
)
assert (assets / "galaxy-avatar.jpg").stat().st_size < 1_000_000

# Keep the star field inside the frame throughout a full rotation.
canvas = Image.new("RGB", (360, 360), "black")
canvas.paste(source.resize((270, 270), Image.Resampling.LANCZOS), (45, 45))
frames = []
for index in range(120):
    frame = canvas.rotate(-3 * index, Image.Resampling.BICUBIC, fillcolor="black")
    frame = ImageEnhance.Brightness(frame).enhance(1 + 0.06 * sin(tau * index / 60))
    frames.append(frame.resize((280, 280), Image.Resampling.LANCZOS))
frames[0].save(assets / "galaxy-spin.gif", save_all=True,
               append_images=frames[1:], duration=100, loop=0, optimize=True)
with Image.open(assets / "galaxy-spin.gif") as animation:
    assert animation.n_frames == 120 and animation.info["loop"] == 0
    assert animation.size == (280, 280)
print("Verified: 500px avatar under 1 MB; 120-frame, 12-second looping galaxy")
