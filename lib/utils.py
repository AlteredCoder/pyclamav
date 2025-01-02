from pathlib import Path


def create_file_folder(filepath):
    """
    Ensure that the directory for the given filepath exists.

    Args:
        filepath (str): The path to the file.

    Example:
        >>> create_file_folder('/path/to/file.txt')
        >>> Path('/path/to/file.txt').parent.exists()
        True
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)


def iterate_folder(folder):
    path = Path(folder)
    for file in path.rglob("*"):
        if not file.is_file():
            continue
        yield file
