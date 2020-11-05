from PIL import ImageFont, ImageDraw, Image, ImageChops

def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

def draw_ascii(string):
    image = Image.new("RGB", (2000, 2000), (255,255,255))
    font = ImageFont.truetype("mona.ttf", 12)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), string, fill=(0, 0, 0), font=font)
    image = trim(image)
    return image

def doimage(filepath):
    with open(filepath, "r") as f:
        AA = f.read()
    img = draw_ascii(AA)
    img.save("ascii.png")
