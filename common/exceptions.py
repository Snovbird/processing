class ImageNotFoundError(Exception):
    """When no image is found."""
    pass

class FileDialogExit(Exception): # won't be used for now since currently loops use "None" returned to break out → we don't want program to end prematurely
    """User exitted the file explorer, so stop program"""
    pass