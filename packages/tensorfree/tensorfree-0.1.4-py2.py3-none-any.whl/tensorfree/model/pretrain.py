import shutil
import os
import numpy as np
import tensorflow.keras.applications as kapps
from tensorfree.model.pretrain_factory import PreTrainFactory
from tensorfree.utils.preprocess import image_sizing
from tensorfree.utils.label import label_generator
from tensorfree.utils.wrappers import run_logger


class PredictiveModel:
    """Base Tensorfree Model Object"""

    def __init__(self):
        self._photo_store = None
        self._photo_save = None
        self._pretrained = None
        self._process_predictions = None
        self._image_size = None

    def get_photos(self, path):
        """Depending on defined location, this will grab the required data
        method to access the photos and save it to instance photo_store.

        Parameters
        ----------
        path : str
            Path to directory of photos
        """
        self._photo_store = path

    def save_photos(self, path):
        """This maps the correct photo save location to instance photo_save.

        Parameters
        ----------
        path : str
            Location where photos should be saved
        """
        self._photo_save = path

    def label(self) -> None:
        """Method for running the program to the end user. This will label all files in the set directory
        and save them in the new location.
        """
        if self._photo_store is None:
            raise ValueError(
                "Path to photos is not set, please use model.get_photos('path') before trying to label."
            )
        elif self._photo_save is None:
            raise ValueError(
                "Path to where labeled photos should be saved is not set. Please use model.save_photos('path') \
                before trying to label."
            )
        else:
            # Handle file paths, first item to update in v0.1.1
            for file in os.listdir(self._photo_store):
                file = os.path.join(self._photo_store, file)
                if os.path.isfile(file):
                    self._run_tensorfree(file, self._photo_save)

    def _predict(self, image):
        """A call to the object with an image will generate predications
        based on the specific model type created.

        Parameters
        ----------
        image : np.array
            An (w x h x 3) array representing an image

        Returns
        -------
        predictions : np.array
            Flat probability array representing softmax output for each class
        """
        if len(image.shape) == 3:
            image = np.expand_dims(image, axis=0)

        predictions = self.get_pretrained(image)
        return predictions

    @run_logger
    def _run_tensorfree(self, image_path, save_location) -> None:
        """This method will take a single image, preprocess it, get the predicted class,
        generate a new label, and then copy it to the requested directory.

        Parameters
        ----------
        image_path : str
            Path to single image
        save_location :
            Directory where processed image will be saved
        """
        # Preprocess, predict class, and generate label
        img_tensor = image_sizing(image_path, self._image_size)
        prediction = np.array(self._predict(img_tensor))
        label = label_generator(prediction, self._process_predictions, image_path)

        # Copy to new location
        new_path = os.path.join(save_location, label)
        shutil.copy(image_path, new_path)


# Builders for specific models, designed using a factory so that it is easy to add new SOTA models.
class NASNetBuilder(PredictiveModel):
    """Builder class to set pretrained model to NASNetLarge"""

    def __init__(self):
        super().__init__()
        self._image_size = 331

    @property
    def get_pretrained(self):
        """Only download layers and predictions if model is instantiated, not registered"""
        if self._pretrained is None:
            self._pretrained = kapps.nasnet.NASNetLarge(weights="imagenet")
            self._process_predictions = kapps.nasnet.decode_predictions
        return self._pretrained


class DenseNetBuilder(PredictiveModel):
    """Builder class to set pretrained model to DenseNet201"""

    def __init__(self):
        super().__init__()
        self._image_size = 224

    @property
    def get_pretrained(self):
        """Only download layers and predictions if model is instantiated, not registered"""
        if self._pretrained is None:
            self._pretrained = kapps.densenet.DenseNet201(weights="imagenet")
            self._process_predictions = kapps.densenet.decode_predictions
        return self._pretrained


class MobileNetBuilder(PredictiveModel):
    """Builder class to set pretrained model to MobileNetV2"""

    def __init__(self):
        super().__init__()
        self._image_size = 224

    @property
    def get_pretrained(self):
        """Only download layers and predictions if model is instantiated, not registered"""
        if self._pretrained is None:
            self._pretrained = kapps.mobilenet_v2.MobileNetV2(weights="imagenet")
            self._process_predictions = kapps.mobilenet_v2.decode_predictions
        return self._pretrained


class InceptionBuilder(PredictiveModel):
    """Builder class to set pretrained model to InceptionResNetV2"""

    def __init__(self):
        super().__init__()
        self._image_size = 299

    @property
    def get_pretrained(self):
        """Only download layers and predictions if model is instantiated, not registered"""
        if self._pretrained is None:
            self._pretrained = kapps.inception_resnet_v2.InceptionResNetV2(
                weights="imagenet"
            )
            self._process_predictions = kapps.inception_resnet_v2.decode_predictions
        return self._pretrained


class VGGBuilder(PredictiveModel):
    """Builder class to set pretrained model to VGG19"""

    def __init__(self):
        super().__init__()
        self._image_size = 224

    @property
    def get_pretrained(self):
        """Only download layers and predictions if model is instantiated, not registered"""
        if self._pretrained is None:
            self._pretrained = kapps.vgg19.VGG19(weights="imagenet")
            self._process_predictions = kapps.vgg19.decode_predictions
        return self._pretrained


# Register Model w/ Factory
# Usage model = pretrain.factory.create('Model_name')
factory = PreTrainFactory()
factory.register_pretrain_builders("NASNetLarge", NASNetBuilder())
factory.register_pretrain_builders("DenseNet", DenseNetBuilder())
factory.register_pretrain_builders("MobileNetV2", MobileNetBuilder())
factory.register_pretrain_builders("InceptionResNetV2", InceptionBuilder())
factory.register_pretrain_builders("VGG19", VGGBuilder())
