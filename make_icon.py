"""Generate app_icon.ico — a friendly green snake on a sunny badge.
Run once:  python make_icon.py
"""
from PIL import Image, ImageDraw

SZ = 256
img = Image.new("RGBA", (SZ, SZ), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# Rounded purple background badge
d.rounded_rectangle([8, 8, SZ - 8, SZ - 8], radius=54, fill=(123, 92, 255, 255))
# Sunny inner circle
d.ellipse([34, 34, SZ - 34, SZ - 34], fill=(255, 207, 86, 255))

# Snake body: a fat green 'S' made of overlapping circles
green, dark = (61, 220, 151, 255), (44, 160, 110, 255)
body = [(96, 92), (128, 104), (156, 128), (150, 160),
        (120, 176), (100, 196), (128, 210), (160, 208)]
for i, (x, y) in enumerate(body):
    r = 30 - i * 1
    d.ellipse([x - r, y - r, x + r, y + r], fill=dark)
    d.ellipse([x - r + 4, y - r + 4, x + r - 4, y + r - 4], fill=green)

# Head
hx, hy = 96, 92
d.ellipse([hx - 34, hy - 30, hx + 30, hy + 30], fill=green, outline=dark, width=4)
# Eyes
for ex in (hx - 12, hx + 12):
    d.ellipse([ex - 8, hy - 12, ex + 8, hy + 4], fill=(255, 255, 255, 255))
    d.ellipse([ex - 3, hy - 6, ex + 3, hy + 2], fill=(30, 24, 48, 255))
# Little red tongue
d.line([hx - 30, hy + 14, hx - 46, hy + 20], fill=(255, 90, 120, 255), width=5)
d.line([hx - 46, hy + 20, hx - 54, hy + 14], fill=(255, 90, 120, 255), width=5)
d.line([hx - 46, hy + 20, hx - 54, hy + 26], fill=(255, 90, 120, 255), width=5)

img.save("app_icon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64),
                                 (128, 128), (256, 256)])
print("Wrote app_icon.ico")
