import numpy as np


def extract_red(image: np.ndarray):
    """
    Extract the red channel from the image
    Args:
      image: ndarray: The image as an numpy array
    Returns:
      The red channel of the image
    """

    red_image = np.zeros_like(image)
    # TODO: Implement the function

    return red_image


def extract_green(image: np.ndarray):
    """
    Extract the green channel from the image
    Args:
      image: ndarray: The image as an numpy array
    Returns:
      The green channel of the image
    """

    green_image = np.zeros_like(image)
    # TODO: Implement the function

    return green_image


def extract_blue(image: np.ndarray):
    """
    Extract the blue channel from the image
    Args:
      image: ndarray: The image as an numpy array
    Returns:
      The blue channel of the image
    """

    blue_image = np.zeros_like(image)
    # TODO: Implement the function

    return blue_image


def grayscale(image: np.ndarray):
    """
    Convert the image to grayscale
    Args:
    image: ndarray: The image as an numpy array
    Returns:
    ndarray: The grayscale image
    """
    grayscale_image = np.zeros_like(image)
    # TODO: Implement the function
    return grayscale_image


def negative(image: np.ndarray):
    """
    Convert the image to its negative
    Args:
    image: ndarray: The image as an numpy array
    Returns:
    ndarray: The negative of the image
    """
    # TODO: Implement the function
    return image


def color_reduced(image: np.ndarray, threshold: int = 128):
    """
    Reduce the number of colors in the image
    Args:
    image: ndarray: The image as an numpy array
    Returns:
    list: three colors image reduced
    """
    # TODO: Implement the function
    return image


def photomaton(image: np.ndarray):
    """
    Apply the photomaton effect to the image

    Args:
    image: ndarray: The image as an numpy array
    Returns:
    ndarray: The image with the photomaton effect
    """
    assert image.shape[1] % 2 == 0, "Image width must be even"
    _, width, _ = image.shape
    # TODO: Implement the function
    return image
