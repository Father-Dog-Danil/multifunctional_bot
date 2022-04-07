from PIL import Image, ImageDraw


def inversion(name):
    image = Image.open(name)
    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    for x in range(width):
        for y in range(height):
            r = 255 - pix[x, y][0]
            g = 255 - pix[x, y][1]
            b = 255 - pix[x, y][2]
            draw.point((x, y), (r, g, b))
    image.save(name)


def black_white(name):
    image = Image.open(name)
    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    for x in range(width):
        for y in range(height):
            r = pix[x, y][0]
            g = pix[x, y][1]
            b = pix[x, y][2]
            sr = (r + g + b) // 3
            r, g, b = sr, sr, sr
            draw.point((x, y), (r, g, b))
    image.save(name)


def sepia(name):
    depth = 32
    image = Image.open(name)
    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    for x in range(width):
        for y in range(height):
            r = pix[x, y][0]
            g = pix[x, y][1]
            b = pix[x, y][2]
            S = (r + g + b) // 3
            r = S + depth * 2
            g = S + depth
            b = S
            r = max(0, min(255, r))
            g = max(0, min(255, g))
            b = max(0, min(255, b))
            draw.point((x, y), (r, g, b))
    image.save(name)


def red(name):
    depth = 32
    image = Image.open(name)
    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    for x in range(width):
        for y in range(height):
            r = max(0, min(255, pix[x, y][0] + depth))
            g = max(0, min(255, pix[x, y][1] - depth // 2))
            b = max(0, min(255, pix[x, y][2] - depth // 2))
            draw.point((x, y), (r, g, b))
    image.save(name)


def orange(name):
    depth = 32
    image = Image.open(name)
    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    for x in range(width):
        for y in range(height):
            r = max(0, min(255, pix[x, y][0] + depth * 2))
            g = max(0, min(255, pix[x, y][1] + depth + 2))
            b = max(0, min(255, pix[x, y][2] - depth // 2))
            draw.point((x, y), (r, g, b))
    image.save(name)


def yellow(name):
    depth = 32
    image = Image.open(name)
    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    for x in range(width):
        for y in range(height):
            r = max(0, min(255, pix[x, y][0] + depth))
            g = max(0, min(255, pix[x, y][1] + depth))
            b = max(0, min(255, pix[x, y][2] - depth // 2))
            draw.point((x, y), (r, g, b))
    image.save(name)


def green(name):
    depth = 32
    image = Image.open(name)
    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    for x in range(width):
        for y in range(height):
            r = max(0, min(255, pix[x, y][0] - depth // 2))
            g = max(0, min(255, pix[x, y][1] + depth))
            b = max(0, min(255, pix[x, y][2] - depth // 2))
            draw.point((x, y), (r, g, b))
    image.save(name)


def blue(name):
    depth = 32
    image = Image.open(name)
    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    for x in range(width):
        for y in range(height):
            r = max(0, min(255, pix[x, y][0] - depth // 2))
            g = max(0, min(255, pix[x, y][1] - depth // 2))
            b = max(0, min(255, pix[x, y][2] + depth))
            draw.point((x, y), (r, g, b))
    image.save(name)


def purple(name):
    depth = 32
    image = Image.open(name)
    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()
    for x in range(width):
        for y in range(height):
            r = max(0, min(255, pix[x, y][0] + depth))
            g = max(0, min(255, pix[x, y][1] - depth // 2))
            b = max(0, min(255, pix[x, y][2] + depth))
            draw.point((x, y), (r, g, b))
    image.save(name)