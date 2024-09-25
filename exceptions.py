class InvalidCommandInputError(Exception):
    """Custom exception for invalid command input."""
    pass

class EmptyImageCollectionError(Exception):
    """Custom exception for empty image collection."""
    pass

class FilenameExistsError(Exception):
    """Custom exception for input of an already existing filename."""
    pass

class InvalidInputError(Exception):
    """Custom exception for invalid input."""
    pass

class ImageNotFoundError(Exception):
    """Custom exception for when an image cannot be found."""
    pass 

class SessionLoadError(Exception):
    """Custom exception for json-files that are unable to load."""