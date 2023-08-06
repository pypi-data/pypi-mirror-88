from PIL import Image
import numpy as np


def image_sizing(image_path, size):
    """Crops and/or scales an image to a needed size.

    Parameters
    ----------
    image_path : str
        Location of file
    size : int
        The h, w of square image required

    Returns
    -------
    scaled_image : np.array
        An array representing the processed file
    """
    try:
        img = Image.open(image_path, mode="r")
        img = img.convert("RGB")
    except FileNotFoundError:
        raise FileNotFoundError(f"Image not found: {image_path}")
    except:
        raise TypeError(f"File provided is not readable image: {image_path}")

    width, height = img.size

    # Keep the most image information by scaling the shortest edge
    if width < height:
        scalar = (size + 1) / width
    else:
        scalar = (size + 1) / height

    new_width = int(width * scalar)
    new_height = int(height * scalar)
    scaled_image = np.array(img.resize((new_width, new_height)))

    # Crop scaled image to desired size
    cropped_image = scaled_image[:size, :size]

    return cropped_image
