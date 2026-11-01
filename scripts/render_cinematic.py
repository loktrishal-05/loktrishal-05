"""Compose the supplied orbital footage into README motion and project artwork.

Usage: python scripts/render_cinematic.py [path-to-ffmpeg]
Requires FFmpeg and Pillow. The source MP4 is retained without audio in assets.
"""
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

assets = Path(__file__).resolve().parents[1] / "assets"
ffmpeg = sys.argv[1] if len(sys.argv) > 1 else "ffmpeg"
result = subprocess.run([
    ffmpeg, "-v", "error", "-i", str(assets / "orbit-source.mp4"),
    "-vf", "crop=640:280:0:40,fps=10", "-f", "rawvideo", "-pix_fmt", "rgb24", "pipe:1"
], check=True, capture_output=True)
frame_bytes = 640 * 280 * 3
assert len(result.stdout) % frame_bytes == 0
frames = [Image.frombytes("RGB", (640, 280), result.stdout[i:i + frame_bytes])
          for i in range(0, len(result.stdout), frame_bytes)]
assert len(frames) == 100, "Expected the supplied ten-second source at 10 fps"
# Overlap the final eight frames with the beginning for a continuous seam.
loop = frames[8:-8] + [Image.blend(frames[-8+i], frames[i], i / 7) for i in range(8)]
assert len(loop) == 92
fonts = Path("C:/Windows/Fonts")
if fonts.exists():
    regular, bold = fonts / "segoeui.ttf", fonts / "segoeuib.ttf"
else:
    fonts = Path("/usr/share/fonts/truetype/dejavu")
    regular, bold = fonts / "DejaVuSans.ttf", fonts / "DejaVuSans-Bold.ttf"


def font(size, heavy=False):
    return ImageFont.truetype(str(bold if heavy else regular), size)


def stage(frame, height, scene_width=660, x=330):
    image = Image.new("RGB", (960, height), "#080E16")
    scene = frame.resize((scene_width, round(scene_width * 280 / 640)), Image.Resampling.LANCZOS)
    mask = Image.new("L", scene.size, 255)
    gradient = ImageDraw.Draw(mask)
    for column in range(110):
        gradient.line((column, 0, column, scene.height), fill=round(column / 109 * 255))
    image.paste(scene, (x, (height - scene.height) // 2), mask)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((1, 1, 958, height - 2), radius=16, outline="#394B5C", width=1)
    draw.line((24, height - 4, 936, height - 4), fill="#02060A", width=3)
    return image


def hero(frame):
    image = stage(frame, 324)
    draw = ImageDraw.Draw(image)
    draw.line((40, 85, 104, 85), fill="#DDF4FF", width=2)
    draw.text((40, 104), "LOKTRISHAL K", font=font(43, True), fill="#F8FAFC")
    draw.text((42, 171), "AI / DATA SCIENCE / FULL STACK", font=font(16), fill="#C6D9E6")
    draw.text((42, 224), "Intelligence, engineered with purpose.", font=font(15), fill="#8EACBF")
    return image


def footer(frame):
    image = stage(frame, 230, 540, 430)
    draw = ImageDraw.Draw(image)
    draw.line((40, 42, 104, 42), fill="#DDF4FF", width=2)
    draw.text((40, 59), "Curiosity into code.", font=font(34), fill="#F8FAFC")
    draw.text((40, 104), "Data into decisions.", font=font(34), fill="#BDCFDC")
    draw.text((42, 177), "EXPLORE / BUILD / REFINE", font=font(14), fill="#8EACBF")
    return image


def save_loop(name, composition):
    rendered = [composition(frame) for frame in loop]
    sample = Image.new("RGB", (960, rendered[0].height * 3))
    for row, index in enumerate((0, 30, 60)):
        sample.paste(rendered[index], (0, row * rendered[0].height))
    palette = sample.quantize(colors=192)
    indexed = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in rendered]
    indexed[0].save(assets / name, save_all=True, append_images=indexed[1:],
                    duration=100, loop=0, optimize=True)
    with Image.open(assets / name) as animation:
        assert animation.n_frames == 92 and animation.info["loop"] == 0
    assert (assets / name).stat().st_size < 8_000_000, "README animation exceeds the size budget"


save_loop("hero-cinematic.gif", hero)
hero(loop[25]).save(assets / "hero-cinematic.jpg", quality=95, optimize=True)
save_loop("footer-cinematic.gif", footer)
footer(loop[25]).save(assets / "footer-cinematic.jpg", quality=95, optimize=True)
projects = [
    ("kinsight", "01 / HEALTHCARE INTELLIGENCE", "KinSight", "Multilingual risk education / Human-guided decisions"),
    ("solarda", "02 / AGENTIC AGRICULTURE", "Solarda", "Safety-gated agents / Vision / Sensor forecasting"),
    ("exodetect", "03 / SCIENTIFIC MACHINE LEARNING", "ExoDetect", "Kepler light curves / Calibrated classification"),
    ("legal", "04 / DOCUMENT INTELLIGENCE", "Legal Assurance", "Contracts / Regulatory change / Evidence"),
    ("nwis", "05 / GEOSPATIAL DECISION SUPPORT", "eRTMAC-NWIS", "Nearby-well intelligence / Advisory workflows"),
    ("edunova", "06 / IMMERSIVE EDUCATION", "EduNova", "Science worlds / 3D learning / Interactive quests"),
]
for index, (slug, category, title, subtitle) in enumerate(projects):
    image = stage(frames[index * 15 + 5], 210, 510, 460)
    draw = ImageDraw.Draw(image)
    draw.text((38, 26), category, font=font(14), fill="#A0BED1")
    draw.text((36, 65), title, font=font(46, True), fill="#F8FAFC")
    draw.text((38, 145), subtitle, font=font(16), fill="#C6D9E6")
    image.save(assets / f"project-{slug}.jpg", quality=95, optimize=True)

identity = Image.new("RGB", (960, 240), "#080E16")
draw = ImageDraw.Draw(identity)
draw.rounded_rectangle((1, 1, 958, 238), radius=16, outline="#394B5C")
draw.polygon([(28, 20), (224, 20), (236, 32), (236, 226), (40, 226), (28, 214)], fill="#203346")
draw.rectangle((28, 20, 224, 216), fill="#E6EEF3")
photo = Image.open(assets / "portrait.png").convert("RGB").resize((184, 184), Image.Resampling.LANCZOS)
identity.paste(photo, (34, 26))
draw.text((270, 43), "Loktrishal K", font=font(39, True), fill="#F5FAFF")
draw.text((272, 111), "AI & Data Science Engineer", font=font(23), fill="#C6D9E6")
draw.text((272, 148), "Full Stack Developer", font=font(23), fill="#C6D9E6")
draw.text((274, 198), "CHENNAI, INDIA", font=font(15), fill="#8EACBF")
identity.save(assets / "identity-cinematic.jpg", quality=96, optimize=True)
mobile_identity = Image.new("RGB", (520, 240), "#080E16")
draw = ImageDraw.Draw(mobile_identity)
draw.rounded_rectangle((1, 1, 518, 238), radius=14, outline="#394B5C")
draw.polygon([(22,40),(178,40),(186,48),(186,204),(30,204),(22,196)],fill="#294156")
draw.rectangle((22,40,178,196),fill="#E6EEF3")
mobile_identity.paste(photo.resize((144,144),Image.Resampling.LANCZOS),(28,46))
draw.text((202,43),"Loktrishal K",font=font(29,True),fill="#F5FAFF")
draw.text((202,101),"AI & Data Science Engineer",font=font(17),fill="#C6D9E6")
draw.text((202,133),"Full Stack Developer",font=font(17),fill="#C6D9E6")
draw.text((203,182),"CHENNAI, INDIA",font=font(13),fill="#8EACBF")
mobile_identity.save(assets / "identity-mobile.jpg",quality=96,optimize=True)

logos = Image.open(assets / "toolbox-logos.png").convert("RGB")
assert logos.size == (600, 180)
tools = Image.new("RGB", (960, 315), "#080E16")
draw = ImageDraw.Draw(tools)
draw.rounded_rectangle((1, 1, 958, 313), radius=16, outline="#394B5C")
for row in range(3):
    for column in range(10):
        x, y, size = 19+column*92, 14+row*96, 77
        draw.rounded_rectangle((x+6,y+9,x+size+7,y+size+10),radius=13,fill="#010408")
        draw.polygon([(x+size,y+9),(x+size+6,y+15),(x+size+6,y+size),(x+size,y+size-4)],fill="#294156")
        draw.polygon([(x+9,y+size),(x+size-4,y+size),(x+size+3,y+size+6),(x+15,y+size+6)],fill="#182A3A")
        draw.rounded_rectangle((x,y,x+size,y+size),radius=13,fill="#152333",outline="#476074")
        icon = logos.crop((column*60,row*60,(column+1)*60,(row+1)*60))
        icon_mask = Image.new("L", (60,60), 0)
        ImageDraw.Draw(icon_mask).rounded_rectangle((0,0,59,59),radius=12,fill=255)
        tools.paste(icon,(x+8,y+8),icon_mask)
        draw.line((x+15,y+1,x+size-15,y+1),fill="#819BAB")
tools.save(assets / "toolbox-depth.png", optimize=True)
print("Verified: six project panels and two 92-frame seamless motion banners")
