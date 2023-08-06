# Colab setup ------------------
import os, sys, subprocess
if "google.colab" in sys.modules:
    cmd = "pip install --upgrade xarray arviz cmdstanpy bebi103 watermark"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    data_path = "https://s3.amazonaws.com/bebi103.caltech.edu/data/"
else:
    data_path = "../data/"
# ------------------------------

import numpy as np
import pandas as pd

import holoviews as hv
hv.extension('bokeh')

import bebi103
bebi103.hv.set_defaults()

import ECDF

import bokeh.io
bokeh.io.output_notebook()

def label_vs_non_labeled_ecdf():
    df = pd.read_csv(os.path.join(data_path, 'gardner_time_to_catastrophe_dic_tidy.csv'))

    # Compute x and y values for ECDFs
    x_labeled, y_labeled = ecdf_vals(df.loc[df["labeled"], "time to catastrophe (s)"] / 60)
    x_unlabeled, y_unlabeled = ecdf_vals(
        df.loc[~df["labeled"], "time to catastrophe (s)"] / 60
    )

    # Make the plot
    p = bokeh.plotting.figure(
        plot_width=450,
        plot_height=300,
        x_axis_label="time to catastrophe (min)",
        y_axis_label="ECDF",
    )
    p.circle(x=x_labeled, y=y_labeled, legend_label="labeled")
    p.circle(x=x_unlabeled, y=y_unlabeled, color="orange", legend_label="unlabeled")
    p.legend.location = "bottom_right"

    return p