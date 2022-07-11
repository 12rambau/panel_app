from sepal_ui import sepalwidgets as sw
from sepal_ui.scripts import decorator as sd
from sepal_ui.scripts import utils as su

from component import scripts
from component.message import cm


class DefaultVizTile(sw.Tile):
    def __init__(self, model, aoi_model, result_tile):

        # define the models
        self.model = model
        self.aoi_model = aoi_model

        # gather extra tile as member for display
        self.result_tile = result_tile

        # create widgets
        self.slider = sw.Slider(
            label=cm.default_process.slider, class_="mt-5", thumb_label=True, v_model=0
        )
        self.text = sw.TextField(label=cm.default_process.textfield, v_model=None)

        # link the widgets to the model
        model.bind(self.slider, "slider_value").bind(self.text, "text_value")

        # construct the Tile with the widget we have initialized
        super().__init__(
            id_="default_viz_tile",
            title=cm.default_process.title,
            inputs=[self.slider, self.text],
            btn=sw.Btn(),
            alert=sw.Alert(),
        )

        # now that the Tile is created we can link it to a specific function
        self.btn.on_event("click", self._on_run)

    @sd.loading_button(debug=False)
    def _on_run(self, widget, data, event):

        # check inputs
        su.check_input(self.aoi_model.name, cm.default_process.no_aoi)
        su.check_input(self.model.slider_value, cm.default_process.no_slider)
        su.check_input(self.model.text_value, cm.default_process.no_textfield)

        # launch the process
        csv_path = scripts.default_csv(
            output=self.alert,
            pcnt=self.model.slider_value,
            name=self.model.text_value,
        )

        # save the file to the dwn file
        self.result_tile.down_btn.set_url(csv_path)

        # create a fake pyplot
        scripts.default_hist(self.result_tile.fig)

        # create maps
        dataset = scripts.default_maps(
            self.aoi_model.feature_collection, self.result_tile.m
        )

        # update model
        self.model.csv_path = csv_path
        self.model.dataset = dataset

        # conclude the computation with a message
        self.alert.add_live_msg(cm.default_process.end_computation, "success")

        return
