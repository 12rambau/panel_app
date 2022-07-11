from sepal_ui.model import Model
from traitlets import Any

class DefaultVizModel(Model):

    # set up your inputs
    slider_value = Any(None).tag(sync=True)
    text_value = Any(None).tag(sync=True)

    # set up your output
    link = Any(None).tag(sync=True)
    dataset = Any(None).tag(sync=True)
