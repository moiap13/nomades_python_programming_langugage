import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# from functions_312 import (  # type: ignore
#     extract_red,
#     extract_green,
#     extract_blue,
#     grayscale,
#     negative,
#     color_reduced,
#     photomaton,
#     crop,
# )

from functions import (
    extract_red,
    extract_green,
    extract_blue,
    grayscale,
    negative,
    color_reduced,
    photomaton,
)

from PIL import Image


def main():
    st.title("Image manipulation app")
    st.markdown(
        "Upload any `jpeg` image with a shape of (225, 400, 3) and use the manipulation function you want to see the result"
    )
    image_functions: list[str] = [
        "extract_red",
        "extract_green",
        "extract_blue",
        "grayscale",
        "negative",
        "color_reduced",
        "photomaton",
    ]

    st.sidebar.title("Image manipulation functions")
    alg: str = ...  # TODO: add the selectbox

    if alg == "color_reduced":
        threshold: int = ...  # TODO: add the selectbox

    file = ...  # TODO: add the file uploader

    compute = st.button("Compute", key="compute_button")

    if compute and file != None and (alg or (alg == "color_reduced" and threshold)):
        image = Image.open(file)
        image = np.array(image)

        if alg == "extract_red":
            image = extract_red(image)
        elif alg == "extract_green":
            image = extract_green(image)
        elif alg == "extract_blue":
            image = extract_blue(image)
        elif alg == "grayscale":
            image = grayscale(image)
        elif alg == "negative":
            image = negative(image)
        elif alg == "color_reduced":
            image = color_reduced(image, threshold)
        elif alg == "photomaton":
            image = photomaton(image)

        st.image(image, width="stretch")
    else:
        st.write("You have not uploaded an image yet")
