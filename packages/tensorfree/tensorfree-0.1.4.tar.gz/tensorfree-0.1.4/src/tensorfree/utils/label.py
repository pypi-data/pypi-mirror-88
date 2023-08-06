import hashlib
from pathlib import Path


def label_generator(predictions, processor, filename):
    """Generates a unique label for the image based on the predicted class, a hash,
    and the existing file extension.

    Parameters
    ----------
    predictions : np.array
        Output from model showing each target probability
    processor : keras.util
        Prediction utility unique to each model
    filename : str
        Path to image or image name

    Returns
    -------
    new_label : str
        New label consisting of predicted class plus a hash
    """
    # Hash predictions for always unique filename
    hashed = hashlib.sha1(predictions).hexdigest()

    # Get label from keras predictor
    label = processor(predictions, top=1)[0][0][1]

    # Capture original image suffix
    suffix = "".join(Path(filename).suffixes)

    new_label = f"{label}_{hashed}{suffix}"

    return new_label
