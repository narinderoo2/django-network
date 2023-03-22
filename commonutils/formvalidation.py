


def checkfiled_is_empty(input):
    if input is None or "" or not input:
        raise ValueError(f"Name is not empty")
    