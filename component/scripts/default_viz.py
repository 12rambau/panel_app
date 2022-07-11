import time

import numpy as np
import pandas as pd
import ee
import ipyvuetify as v
from matplotlib import pyplot as plt
from sepal_ui import color as sc
from sepal_ui import get_theme
from sepal_ui.scripts import decorator as sd

from component.message import cm
from component import parameter as cp



def default_csv(output, pcnt, name):

    # write the file in a tmp directory
    pathname = cp.tmp_dir / f"fake_csv_{name}_{pcnt}.csv"

    # create a fake dataframe and save it in tmp
    df = pd.DataFrame(np.random.randint(0, pcnt, size=(pcnt, 4)), columns=list("ABCD"))
    df.to_csv(pathname, index=False)

    # fake the loading of something so that the user see the btn spining
    time.sleep(3)

    # let the user know that you managed to do something
    output.add_live_msg(cm.default_process.end_computation, "success")

    return pathname


def default_hist(fig_hist):

    # generate some fake data
    np.random.seed(0)
    n = 2000
    x = np.linspace(0.0, 10.0, n)
    y = np.cumsum(np.random.randn(n) * 10).astype(int)

    # create a pyplot figure
    # to be displayed, the figure need to be written in an Output widget
    with fig_hist:
        context = "dark_background" if get_theme() == "dark" else "default"
        with plt.style.context(context):
            fig, ax = plt.subplots(figsize=(10, 10))
            fig.patch.set_alpha(0.0)
            ax.hist(x=y, bins=25, color=[sc.primary], histtype="bar", stacked=True, edgecolor="black", rwidth=0.8)
            ax.set_title(cm.default_process.hist_title, fontweight="bold")
            ax.patch.set_alpha(0.0)
            plt.show()

    return fig_hist

@sd.need_ee
def default_maps(ee_aoi, m):

    # set up the map on the aoi
    m.zoom_ee_object(ee_aoi.geometry())

    # add the object borders in blue
    empty = ee.Image().byte()
    outline = empty.paint(featureCollection=ee_aoi, color=1, width=3)
    m.addLayer(outline, {"palette": sc.info}, "aoi")
    m.zoom_ee_object(ee_aoi.geometry())

    # here I will only clip and display a the result of this tutorial : https://developers.google.com/earth-engine/tutorials/tutorial_forest_02
    # you can do whatever GEE process to produce you image before displaying it
    # fmt: off
    dataset = ee.Image("UMD/hansen/global_forest_change_2015")
    GainAndLoss = dataset.select("gain").And(dataset.select("loss"))
    m.addLayer(dataset.clip(ee_aoi), {"bands": "treecover2000"}, cm.default_process.treecover2000)  # printing the forest coverage in 2000
    m.addLayer(dataset.clip(ee_aoi), {"bands": ["last_b50", "last_b40", "last_b30"]}, cm.default_process.healthy_veg,)  # mapping the forest in 2015
    m.addLayer(dataset.clip(ee_aoi), {"bands": ["loss", "treecover2000", "gain"]}, cm.default_process.green)  # map the gain and losses
    m.addLayer(dataset.clip(ee_aoi), {"bands": ["loss", "treecover2000", "gain"], max: [1, 255, 1]}, cm.default_process.green_update,) # map the gain and losses with bright colors
    m.addLayer(GainAndLoss.updateMask(GainAndLoss), {"palette": "FF00FF"},cm.default_process.gain_loss) # map the place where gain and loss happened
    # fmt: on
    
    return dataset
