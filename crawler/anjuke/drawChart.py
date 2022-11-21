"""
@author kingfish
读取excel数据，画柱状图
"""

import pandas as pd

from pyecharts import options as opts
from pyecharts.charts import Bar

def draw_bar_chart():
    fpath = "data_visual/drawBarChart/商家销售数据.xlsx"

    excel = pd.read_excel(fpath)

    bar = (
        Bar()
        .add_xaxis(excel["商品"].tolist())
        .add_yaxis("商家A",excel["商家A"].tolist())
        .add_yaxis("商家B",excel["商家B"].tolist())
        .set_global_opts(title_opts=opts.TitleOpts(title="商品销量对比图"))
    )

    return bar.render_embed()