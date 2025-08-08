import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import tensorflow as tf

from PIL import Image


def main():
    st.title("Cifar 10 web classification")
    st.write(
        "Upload any image that you think fit into one of the classes and see if the prediction is correct"
    )

    file = st.file_uploader("Upload the image", type=["jpg", "png", "jpeg"])
    if file != None:
        image = Image.open(file)
        st.image(image, use_container_width=True)

        resized_image = image.resize((32, 32))
        image_arr = np.array(resized_image) / 255
        image_arr = image_arr.reshape(1, 32, 32, 3)

        model = tf.keras.models.load_model("cifar10_model.h5")
        prediction = model.predict(image_arr)
        cifar10_classes = [
            "airplane",
            "automobile",
            "bird",
            "cat",
            "deer",
            "dog",
            "frog",
            "horse",
            "ship",
            "truck",
        ]

        prediction_text = cifar10_classes[np.argmax(prediction)]

        fig, ax = plt.subplots()
        y_pos = np.arange(len(cifar10_classes))
        ax.barh(y_pos, prediction[0], align="center")
        ax.set_yticks(y_pos)
        ax.set_yticklabels(cifar10_classes)
        ax.invert_yaxis()
        ax.set_xlabel("Probability")
        ax.set_title("Cifar 10 Prediction")
        st.pyplot(fig)
        st.write(
            f"The model predicts that the image is a {prediction_text} with a probability of {np.max(prediction):.2f}"
        )
    else:
        st.write("You have not uploaded an image yet")


main()
