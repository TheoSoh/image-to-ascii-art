import os, os.path
from PIL import Image, ImageEnhance
import exceptions

class Image_wrapper:
    """A class that represents an image"""
    def __init__(self, 
                 filename: str, 
                 alias: str|None, 
                 target_width: int=50, 
                 brightness: float=1.0, 
                 contrast: float=1.0):
        """Constructs necessary attributes of an Image_wrapper object."""
        with Image.open(filename) as image:
            self._image =  image.copy()  # Enable later handling of certain attributes (e.g. resizing).
        self._filename = filename
        self._alias = alias
        self._target_size = self._calculate_target_height(target_width)
        self._brightness = brightness
        self._contrast = contrast

    @property
    def image(self):
        """Returns an Image object"""
        return self._image

    @property
    def filename(self):
        """Returns a string containing the object's filename, suffix included."""
        return self._filename

    @property
    def alias(self) -> str|None:
        """Returns None or a string containing the object's alias."""
        return self._alias  # Either a string or None.

    @property
    def size(self):
        """Returns a tuple containing the Image object's actual size."""
        return self._image.size
    
    @property
    def target_size(self):
        """Returns a tuple containing the object's target size."""
        return self._target_size
    
    @property
    def brightness(self):
        """Returns a float value that represents the image's brightness"""
        return self._brightness

    @brightness.setter
    def brightness(self, new_brightness: str):
        """Assumes new_brightness is a string that is convertable
        to float. Sets the brightness ratio to new_brightness.
        """
        new_brightness = float(new_brightness)
        if new_brightness < 0:
            raise exceptions.InvalidInputError("-- Invalid brightness ratio:"
                                                + " brightness ratio must be a"
                                                + " positive float or int --\n"
                                                + " (Original image has "
                                                + " brightness ratio 1.0)")
        self._brightness = new_brightness

    @property
    def contrast(self):
        """Returns a float value representing the image's contrast."""
        return self._contrast

    @contrast.setter
    def contrast(self, new_contrast: str):
        """Assumes new_contrast is a string that is convertable
        to float. Sets the contrast ratio to new_contrast.
        """
        new_contrast = float(new_contrast)
        if new_contrast < 0:
            raise exceptions.InvalidInputError("-- Invalid contrast ratio:"
                                                + " contrast ratio must be a"
                                                + " positive int --\n"
                                                + " (Original image has "
                                                + " contrast ratio 1.0)")
        self._contrast = new_contrast

    def set_target_width(self, new_width: str):
        """Assumes new_width is a string and sets the _target_size
        attribute to a new target size calculated based on specified
        new width.
        """
        new_width = int(new_width)
        if new_width < 1:
            raise ValueError()
        new_target_size = self._calculate_target_height(new_width)
        self._target_size = new_target_size

    def set_target_height(self, new_height: str):
        """Assumes new_height is a string and sets the _target_size
        attribute to a new target size calculated based on specified
        new height.
        """
        new_height = int(new_height)
        if new_height < 1:
            raise ValueError()
        new_target_size = self._calculate_target_width(new_height)
        self._target_size = new_target_size
    
    def _calculate_target_height(self, target_width: int):
        '''Assumes target_width is a positive int. Calculates
        correct target height based on aspect ratio and target
        width input. Original target width is 50 pixels. Returns
        a tuple containing the final target size (width, height).
        '''
        image_width, image_height = self._image.size
        aspect_ratio = image_height/image_width
        target_height = int(aspect_ratio * target_width * 0.55)
        if target_height < 1:
            target_height = 1
        return (target_width, target_height)
    
    def _calculate_target_width(self, target_height: int):
        '''Assumes target_height is a positive int. Calculates
        correct target width based on aspect ratio and target
        height input. Returns a tuple containing the final 
        target size (width, height).
        '''
        image_width, image_height = self._image.size
        aspect_ratio = image_height/image_width
        target_width = int(target_height / (aspect_ratio * 0.55))
        if target_width < 1:
            target_width = 1
        return (target_width, target_height)

    def render_ascii_art_to_file(self, to_filename: str):
        """Assumes to_filename is a string. Renders image as
        ascii-art to txt-file named after the value in to_filename.
        """
        ascii_art = self._convert_to_ascii_art()
        with self._make_directory_and_open_w(to_filename + ".txt") as text_file:
            print(ascii_art, file=text_file)

    def render_ascii_art_to_console(self):
        """Renders image as ascii-art to display in console/terminal."""
        ascii_art = self._convert_to_ascii_art()
        print(ascii_art)

    def _convert_to_ascii_art(self) -> str:
        """Converts pixels to ascii-characters and returns a string containing ascii-art."""
        ascii_art = ""
        ascii_chars = " `.-:+=*#%@"
        adjusted_image = self._adjust_image_for_render()
        width, height = adjusted_image.size
        # convert each pixel to ascii-character and add to the ascii-art-string.
        for y in range(height):
            for x in range(width):
                pos = (x, y)  # x and y together form coordinates for the image's pixels.
                grayscale = adjusted_image.getpixel(pos)
                ascii_char = ascii_chars[grayscale //
                                        (256 // (len(ascii_chars) -1))]  # Map pixel's brightness to the indices of the chars.
                ascii_art += ascii_char
            if y < height - 1:
                # Insert new line in the end of each complete line except for the last line.
                ascii_art += "\n"
        return ascii_art

    def _adjust_image_for_render(self) -> Image:
        """Assumes image is an Image object. Resizes original
        image, Fetches enhanced copies of the image object
        (enhanced brightness and contrast), converts it's mode
        to grayscale. Returns Image object that is fully
        adjusted and ready for conversion to ascii-art.
        """
        resized_image = self._image.resize(self._target_size)  # Enables access to a resized copy of the original image.
        enhanced_image = self._enhance_image_brightness(resized_image)
        fully_enhanced_image = self._enhance_image_contrast(enhanced_image)
        grayscale_image = fully_enhanced_image.convert(mode="L")  # Enables access to pixel's brightness
        return grayscale_image
    
    def _enhance_image_brightness(self, image: Image):
        """Assumes image is an Image object. Adjusts the image
        brightness and returns enhanced Image object.
        """
        enhancer = ImageEnhance.Brightness(image)
        enhanced_image = enhancer.enhance(self._brightness)
        return enhanced_image  # A copy of image, but with altered brightness
    
    def _enhance_image_contrast(self, image: Image):
        """Assumes image is an Image object. Adjusts the image
        contrast and returns enhanced Image object.
        """
        enhancer = ImageEnhance.Contrast(image)
        enhanced_image = enhancer.enhance(self._contrast)
        return enhanced_image  # A copy of image, but with altered contrast

    def _make_directory_and_open_w(self, filename: str):
        """Creates a directory named 'ascii_images' if it doesn't
        already exist. Returns an open stream to path with
        write mode.
        """
        path = "./ascii_images/" + filename
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return open(path, "w")