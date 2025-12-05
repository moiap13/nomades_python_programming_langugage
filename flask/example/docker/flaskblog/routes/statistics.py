import sys
import os

CURR_DIR: str = os.path.dirname(__file__)
ROOT_DIR: str = os.path.dirname(CURR_DIR)
PLOTS_DIR: str = os.path.join(ROOT_DIR, "static", "plots")
sys.path.append(ROOT_DIR)

import random

from flask import Blueprint, render_template
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


statistics_bp = Blueprint("statistics", __name__, url_prefix="/statistics")


@statistics_bp.route("/")
def display_plots() -> str:
    df = pd.DataFrame(
        {
            "2025 sales": [random.random() * 1000 for _ in range(12)],
            "2024 sales": [random.random() * 1000 for _ in range(12)],
        }
    )

    _2025_line = px.line(df, df.index, "2025 sales")

    return render_template(
        "statistics/stats.html", plot=_2025_line.to_html(full_html=False)
    )
