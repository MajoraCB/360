from PIL import Image
import math
import io
import uuid
from django.core.files.images import ImageFile

MAX_IMAGE_WIDTH = 1500
MAX_IMAGE_HEIGHT = 750

MAX_NAV_IMAGE_WIDTH = 700
MAX_NAV_IMAGE_HEIGHT = 375


def generate_sprite_nav_image(request_file):
    img = Image.open(request_file)
    image_width, image_height = img.size
    image_extension = img.format

    scale_ratio = min(MAX_NAV_IMAGE_WIDTH / image_width, MAX_NAV_IMAGE_HEIGHT / image_height)

    scaled_image_width = int(image_width * scale_ratio)
    scaled_image_height = int(image_height * scale_ratio)
    scaled_img = img.resize((scaled_image_width, scaled_image_height), Image.ANTIALIAS)
    print("Scaling nav image by %d X %d" % (scaled_image_width, scaled_image_height))

    output = io.BytesIO()
    scaled_img.save(output, format='jpeg' if image_extension == 'JPEG' else 'png', quality=100)
    output.seek(0)

    return ImageFile(output, str(uuid.uuid4()) + '.jpeg' if image_extension else '.png')


def generate_sprite_image(request_files):
    original_images = [Image.open(image_file) for image_file in request_files]

    image_width, image_height = original_images[0].size
    image_extension = original_images[0].format

    print("all images assumed to be %d by %d and %s format." % (image_width, image_height, image_extension))

    scale_ratio = min(MAX_IMAGE_WIDTH / image_width, MAX_IMAGE_HEIGHT / image_height)

    scaled_image_width = int(image_width * scale_ratio)
    scaled_image_height = int(image_height * scale_ratio)
    scaled_images = []

    index = 0
    for original_image in original_images:
        print("Scaling image %d by %d X %d" % (index, scaled_image_width, scaled_image_height))
        scaled_images.append(
            original_image.resize((scaled_image_width, scaled_image_height), Image.ANTIALIAS))
        index += 1

    image_count = len(scaled_images)

    col_count = math.floor(math.sqrt(image_count))
    row_count = math.floor(image_count / col_count)  # + (1 if image_count % col_count > 0 else 0)

    sprite_width = scaled_image_width * col_count
    sprite_height = scaled_image_height * row_count
    print(
        "creating the sprite image by %d by %d with %d X %d grid" % (sprite_width, sprite_height, col_count, row_count))

    if image_extension == 'JPEG':
        master = Image.new(mode='RGB', size=(sprite_width, sprite_height),
                           color=(0, 0, 0))
    else:
        master = Image.new(mode='RGBA', size=(sprite_width, sprite_height),
                           color=(0, 0, 0, 0))  # fully transparent

    index = 0
    for image in scaled_images:
        location_x = scaled_image_width * (index % col_count)
        location_y = scaled_image_height * math.floor(index / col_count)

        # Remove black images on last row
        if math.floor(index / col_count) > row_count:
            break

        print("adding %s at %d %d grid..." % (request_files[index], location_x, location_y),
              master.paste(image, (location_x, location_y)))

        index += 1

    output = io.BytesIO()
    master.save(output, format='jpeg' if image_extension == 'JPEG' else 'png', quality=100)
    output.seek(0)

    return ImageFile(output, str(uuid.uuid4()) + '.jpeg' if image_extension else '.png'), col_count, row_count


def generate_panoviewer_nav_image(request_file):
    import py360convert
    import numpy as np
    img = Image.open(request_file)
    img_array = np.array(img)

    image_width, image_height = img.size
    image_extension = img.format

    scale_ratio = min(MAX_NAV_IMAGE_WIDTH / image_width, MAX_NAV_IMAGE_HEIGHT / image_height)

    scaled_image_width = int(image_width * scale_ratio)
    scaled_image_height = int(image_height * scale_ratio)

    output_convert = py360convert.e2p(img_array, (75, 75), 0, 0, (scaled_image_height, scaled_image_width))
    output_img = Image.fromarray(output_convert)

    output = io.BytesIO()
    output_img.save(output, format='jpeg' if image_extension == 'JPEG' else 'png', quality=100)
    output.seek(0)

    return ImageFile(output, str(uuid.uuid4()) + '.jpeg' if image_extension else '.png')
