"""Export the generated galaxy as a GitHub avatar and a seamless README loop."""
from pathlib import Path
from math import sin, tau
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont

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

# Fixed editorial copy and a right-aligned galaxy fill the README width.
font_root = Path("C:/Windows/Fonts") if Path("C:/Windows/Fonts").exists() else Path("/usr/share/fonts/truetype/dejavu")
font = ImageFont.truetype(str(font_root / ("segoeui.ttf" if font_root.name == "Fonts" else "DejaVuSans.ttf")), 36)
small = ImageFont.truetype(str(font_root / ("segoeui.ttf" if font_root.name == "Fonts" else "DejaVuSans.ttf")), 14)
banner = Image.new("RGB", (960, 240), "#0B1018")
draw = ImageDraw.Draw(banner)
draw.line((40, 42, 102, 42), fill="#7DD3FC", width=2)
draw.text((40, 59), "Curiosity into code.", font=font, fill="#F8FAFC")
draw.text((40, 106), "Data into decisions.", font=font, fill="#CBD5E1")
draw.text((40, 181), "AI  /  DATA SCIENCE  /  FULL STACK", font=small, fill="#7DD3FC")
footer_frames = []
for frame in frames:
    footer = banner.copy()
    tile = frame.resize((240, 240), Image.Resampling.LANCZOS)
    # Blend the black sky into the banner without a visible square edge.
    tile = ImageChops.lighter(tile, Image.new("RGB", tile.size, "#0B1018"))
    footer.paste(tile, (700, 0))
    footer_frames.append(footer)
footer_frames[0].save(assets / "observatory.gif", save_all=True,
                      append_images=footer_frames[1:], duration=100, loop=0, optimize=True)
with Image.open(assets / "observatory.gif") as footer:
    assert footer.n_frames == 120 and footer.size == (960, 240)
print("Verified: 500px avatar; 120-frame galaxy and full-width observatory loops")
