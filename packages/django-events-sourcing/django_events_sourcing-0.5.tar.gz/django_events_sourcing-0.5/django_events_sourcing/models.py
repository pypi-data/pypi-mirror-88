from django.db import models


class ModelDispatcher(models.Model):
    """
    Detects any change in the model and dispatches events about it
    """

