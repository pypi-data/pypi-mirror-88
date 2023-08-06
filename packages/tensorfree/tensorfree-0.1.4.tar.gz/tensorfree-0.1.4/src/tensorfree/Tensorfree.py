from tensorfree.model import pretrain


def build(model_name):
    """
    This function is used to construct a new model.

        Example use case:

        `from tensorfree import Tensorfree
        model = Tensorfree.build('NASNetLarge')`

    Parameters
    ----------
    model_name : str
        Name of available models

    Returns
    -------
    tensorfree model object
    """
    return pretrain.factory.create(model_name)
