class PreTrainFactory:
    """The model factory used to assign and construct different models.
    Thanks to Real Python's Factory Method tutorial for guidance on
    getting this to work.

    https://realpython.com/factory-method-python/
    """
    def __init__(self):
        self._model_builders = {}

    def register_pretrain_builders(self, key, builder):
        """This allows the library to quickly add or remove new models, through
        registering them to the _model_builders dictionary.

        Parameters
        ----------
        key : str
            Name of builder model that end user can call
        builder : Tensorfree obj
            The builder object the creates a model
        """
        self._model_builders[key] = builder

    def create(self, key):
        """Once a model is in the factory registry, a user can use .create
        to build a specific model registered.

        Parameters
        ----------
        key : str
            Name of model to return to user

        Returns
        -------
        model : tensorfree obj
            The requested model
        """
        model = self._model_builders.get(key)
        if not model:
            raise ValueError(f"Model Not Available: {model}")

        return model
