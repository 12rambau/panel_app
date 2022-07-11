from sepal_ui import sepalwidgets as sw
from sepal_ui.scripts import utils as su 
from sepal_ui.scripts import decorator as sd

from component import scripts as cs
from component.message import cm
from component import widget as cw


class DefaultExportTile(sw.Tile):
    def __init__(self, model, aoi_model, **kwargs):

        # save the models as member of the class
        self.model = model
        self.aoi_model = aoi_model

        # create the widgets 
        self.scale = cw.DefaultResInput(label=cm.default_process.scale, min_res=10, max_res=300)

        # construct the Tile with the widget we have initialized
        super().__init__(
            id_="default_export_tile",
            title=cm.default_process.export,
            inputs=[self.scale],
            btn=sw.Btn(cm.default_process.export),
            alert=sw.Alert(),
        )

        # now that the Tile is created we can link it to a specific function
        self.btn.on_event("click", self._export_to_asset)

    @sd.loading_button(debug=False)
    def _export_to_asset(self, *args):

        # check that the input that you're gonna use are set
        su.check_input(self.model.dataset, cm.default_process.no_dataset)

        # execute the script
        asset_name = cs.export_dataset(self.aoi_model, self.scale.v_model, self.model.dataset)

        # conclude the computation with a message
        self.alert.add_live_msg(cm.default_gee.task_launched.format(asset_name), "success")

        return
