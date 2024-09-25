from PIL import Image
from image_wrapper import Image_wrapper
import exceptions

class Image_collection:
    """A class representing a collection of images"""
    def __init__(self):
        """Constructs an objects necessary attributes."""
        self._images = []
        self._current_image = None

    @property
    def images(self):
        """Returns a list containing current session's loaded images."""
        return self._images
    
    @property
    def current_image(self):
        """Returns an Image_wrapper object that represent latest touched image."""
        return self._current_image
    
    @current_image.setter
    def current_image(self, image_wrapper: Image_wrapper):
        """Sets the _current_image property of the Image_collection object."""
        self._current_image = image_wrapper
    
    def load_image(self, filename: str, alias: str|None):
        """Loads an image into current session. Assumes filename is a
        string and alias is a string or None. Displays relevant
        message if load succeds.
        """
        self._check_filename_existance(filename)
        self._validate_alias(alias)
        image_wrapper = Image_wrapper(filename, alias)
    
        # Adding instance to the collection and set it to current image.
        self._images.append(image_wrapper)
        self._current_image = image_wrapper

    def _check_filename_existance(self, filename: str):
        """Throws exception if given filename is already loaded."""
        loaded_filenames = [image_wrapper.filename for image_wrapper in self.images]
        if filename in loaded_filenames:
            raise exceptions.InvalidInputError("-- Load failed: "
                                               + f"'{filename}'"
                                               + f" is already "
                                               + "loaded --")

    def _validate_alias(self, alias: str|None):
        """Validates given alias and throws exception if it already exist
        or is 'current'.
        """
        if not alias:
            # Alias is optional and None is therefore valid.
            return
        elif alias.casefold() == "current":
            # 'current' is an invalid alias.
            raise exceptions.InvalidInputError("-- Load failed: "
                                               + "An alias cannot "
                                               + f"be '{alias}' --")
        loaded_aliases = [image_wrapper.alias for image_wrapper in self.images]
        if alias in loaded_aliases:
            # Specified alias already exist.
            raise exceptions.InvalidInputError("-- Load failed:"
                                               f" '{alias}' "
                                               + "is already in"
                                               + " use --")
                
    def display_info(self):
        """Outputs information about the current session's loaded images."""
        self.check_empty_image_collection()
        
        print("=== Current session ===", "Images:", sep="\n")
        # Display info about every image in the collection.
        for image_wrapper in self._images:
            image_alias = image_wrapper.alias
            image_filename = image_wrapper.filename
            if image_alias:
                print(image_alias)
            else:
                print(image_filename)
            print(f"{"filename: ":>13}{image_filename}")
            print(f"{"size: ":>9}{image_wrapper.size}")
            print(f"{"target size: ":>16}{image_wrapper.target_size}")
            print(f"{"brightness: ":>15}{image_wrapper.brightness}")
            print(f"{"contrast: ":>13}{image_wrapper.contrast}\n")

        # Display alias or filename of the current image.
        print("Current image: ", end="")
        if image_alias:
            print(image_alias)
        else:
            print(image_filename)
    
    def render_ascii_art(self, image_name: str|None,
                         to_filename: str|None):
        """Assumes image_name and to_filename is None or string.
        Outputs either a string containing relevant ascii-art or 
        a text-file containing relevant ascii-art.
        """
        self.check_empty_image_collection()
        
        if not image_name or (image_name.lower() == "current" 
                              and not to_filename):
            # User input == "render" or "render current"
            self._current_image.render_ascii_art_to_console()
            return
        elif image_name.lower() == "current" and to_filename:
            self._current_image.render_ascii_art_to_file(to_filename)
            return
        
        # Enable access to relevant object.
        image_wrapper = self._find_image_wrapper(image_name)
        # Call correct function.
        if to_filename:
            image_wrapper.render_ascii_art_to_file(to_filename)
        else:
            image_wrapper.render_ascii_art_to_console()
        self._current_image = image_wrapper

    # Set attribute functionality:
    def set_image_attribute(self, image_name: str,
                            attribute: str, value: str):
        """Assumes image_name is a string, attribute is a string and value is
        a string. Checks which function is correct based on attribute and
        finally calls that function for given image. Catches potential ValueError
        exceptions if thrown and then raises an InvalidInputError exception.
        """
        self.check_empty_image_collection()
        image_wrapper = self._find_image_wrapper(image_name)
        if attribute == "width":
            try:
                image_wrapper.set_target_width(value)
            except ValueError:
                # Catch exception to throw a more descriptive one.
                raise exceptions.InvalidInputError("-- Invalid value: Width must"
                                                   + " be a positive number --\n"
                                                   + "(Original width: 50)")
        elif attribute == "height":
            try:
                image_wrapper.set_target_height(value)
            except ValueError:
                # Catch exception to throw a more descriptive one.
                raise exceptions.InvalidInputError("-- Invalid value: Height must"
                                                        + " be a positive number --\n"
                                                        + "(e.g. 19)")
        elif attribute == "brightness":
            image_wrapper.brightness = value  # can't throw ValueError because of regex pattern.
        elif attribute == "contrast":
            image_wrapper.contrast = value  # can't throw ValueError because of regex pattern.
        self._current_image = image_wrapper

    def add_image_to_collection(self, image: Image):
        """Assumes image is an Image object and adds it to the list of loaded images."""
        self._images.append(image)

    def _find_image_wrapper(self, image_name: str) -> Image_wrapper:
        """Assumes image_name is a string containing a potential filename
        or alias. Looks through the image collection (currently loaded
        images). Returns the sought after Image_wrapper object with
        filename or alias equal to image_name.
        """
        for image_wrapper in self._images:
            if (image_wrapper.filename == image_name 
                    or image_wrapper.alias == image_name):
                # Image_wrapper found.
                return image_wrapper
        raise exceptions.ImageNotFoundError(f"-- Image is not loaded: '{image_name}'"
                                            + " cannot be found --")
    
    def check_empty_image_collection(self):
        """Checks if list (image collection) is empty and throws exception if it is."""
        if not self._images:
            # no images are loaded in current session.
            raise exceptions.EmptyImageCollectionError(f"-- Empty collection: No images are "
                                                       + "loaded in the current session --")