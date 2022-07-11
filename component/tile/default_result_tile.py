from ipywidgets import Output
from sepal_ui import mapping as sm
from sepal_ui import sepalwidgets as sw

from component.message import cm


class DefaultResultTile(sw.Tile):
    def __init__(self, **kwargs):

        # the result widgets that will be used by the process tile
        self.down_btn = sw.DownloadBtn(cm.default_process.csv_btn)
        self.fig = Output()
        self.m = sm.SepalMap()

        # organise them in a layout
        figs = sw.Layout(
            Row=True,
            align_center=True,
            children=[
                sw.Flex(xs6=True, children=[self.fig]),
                sw.Flex(xs6=True, children=[self.m]),
            ],
        )

        # create the widget
        super().__init__(
            id_="default_result_tile",
            title=cm.default_result.title,
            inputs=[self.down_btn, figs],
        )
