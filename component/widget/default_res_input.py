from sepal_ui import sepalwidgets as sw


class DefaultResInput(sw.TextField):
  
    def __init__(self, min_res, max_res, **kwargs):

        # set up some vuetify parameters
        kwargs["min_"] = min_res
        kwargs["max_"] = max_res
        kwargs["type"] = "number"
        kwargs["hint"] = f"Need to be an integer in [{min_res}, {max_res}]"

        # create the widget
        super().__init__(**kwargs)

        # bind the custom number check
        self.on_event("focusout", self._is_number)

    def _is_number(self, *args):
        """display an error essage if the value is not a number between min and max value"""

        # clear error
        self.error_messages = None

        # get out if v_model is none
        if not self.v_model:
            return self

        # check if it's a number
        valid = True
        try:

            value = int(self.v_model)

            if value < self.min_ or value > self.max_:
                valid = False

        except ValueError:
            valid = False

        if valid is False:
            self.v_model = None
            self.error_messages = [self.hint]

        return self
