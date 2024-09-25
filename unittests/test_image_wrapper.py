import unittest
import os
from image_wrapper import Image_wrapper
from PIL import Image

class TestImageWrapper(unittest.TestCase):
    def setUp(self):
        # Assumes 'slalom.jpg' image-file is in cwd.
        self.image = Image_wrapper("slalom.jpg", None, 50, 1.3, 1.3)
        self.test_render_to_filename = "test_render_file"

    def tearDown(self):
        # Delete temporary file if exist.
        if os.path.exists("./ascii_images/" + self.test_render_to_filename + ".txt"):
            os.remove("./ascii_images/" + self.test_render_to_filename + ".txt")

    def test_initialization(self):
        self.assertIsInstance(self.image.image, Image.Image)
        self.assertEqual(self.image.filename, "slalom.jpg")
        self.assertEqual(self.image.alias, None)
        self.assertEqual(self.image.target_size[0], 50)
        self.assertEqual(self.image.brightness, 1.3)
        self.assertEqual(self.image.contrast, 1.3)

    def test_set_target_width_error(self):
        with self.assertRaises(ValueError):
            # Test width < 1
            self.image.set_target_width("0")
        with self.assertRaises(ValueError):
            # Test width != int
            self.image.set_target_width("invalid width")
    
    def test_set_target_height_error(self):
        with self.assertRaises(ValueError):
            # Test height < 1
            self.image.set_target_height("0")
        with self.assertRaises(ValueError):
            # Test height != int
            self.image.set_target_height("invalid height")

    def test_brightness_enhancement(self):
        original_image = self.image.image
        enhanced_image = self.image._enhance_image_brightness(self.image.image)
        self.assertNotEqual(enhanced_image, original_image)
    
    def test_contrast_enhancement(self):
        original_image = self.image.image
        enhanced_image = self.image._enhance_image_contrast(self.image.image)
        self.assertNotEqual(enhanced_image, original_image)

    def test_image_adjustments_for_render(self):
        original_image = self.image.image
        adjusted_image = self.image._adjust_image_for_render()
        self.assertNotEqual(adjusted_image, original_image)

    def test_render_ascii_art_to_file(self):
        self.image.render_ascii_art_to_file(self.test_render_to_filename)
        self.assertTrue(os.path.exists("./ascii_images/" 
                                       + self.test_render_to_filename
                                       + ".txt"))

if __name__ == '__main__':
    unittest.main()