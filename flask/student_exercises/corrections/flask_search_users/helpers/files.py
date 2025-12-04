import uuid


def generate_pp_filename(pp_filename: str) -> str:
    """
    Generate a unique filename for the profile picture using *UUID* standard

    Args:
        pp_filename (str): The profile picture filename

    Returns:
        str: The unique filename
    """
    return f"{str(uuid.uuid4())}.{pp_filename.split('.')[-1]}"
